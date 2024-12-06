"""
Contains the base class for both the JobDownloader and the PerpetualDownloader.


PAGING
Both the job downloader and the perpetual downloader get their lists of tasks to download in batches. In both cases they implement the get_some_tasks() method. This method is called repeatedly until it is interrupted or until it returns a falsy locator. The locator, if not falsy, is whatever the derived class finds useful. See the documentation for the derived classes for detailed information.

CALLBACKS
The intention is to keep the downloader simple and flexible. As such, some functionality is intentionally left out. For example, we do not report back to the Conductor API when tasks are complete. We do not format output, other than that provided by standard logging. We do not provide a GUI. Instead, we emit lifecycle events that can be used to do all of these things and more. The LoggingDownloadRunner class demonstrates this.

Callbacks are called with an 'evt' argument, which is a dictionary containing information about the event. The events are listed in the VALID_EVENTS list. To register a callback you use the `on` method - for example: `downloader.on("start", my_callback)`. The callback must be a function that accepts one argument named 'evt'. The callback can be a method of another class. Several callbacks may be registered for the same event type.

Since the downloader is multithreaded, the events are generated in different threads. We use a Queue to pass the events from the downloader threads to the main thread. The method, dispatch_events is responsible for reading events from the queue and calling the appropriate callbacks. 

Most event types are emitted unchanged as they are received from the queue. However, if one or more callbacks are registered to handle the EVENT_TYPE_TASK_DONE event, then the dispatch_events method will also generate a TASK_DONE event when all files for a task have been downloaded. In order to do this, we make use of a registry of tasks and the number of files downloaded for each task. See the documentation for the Registry class for more information.

RETRIES
If an error occurs during download, the file will be retried with exponential backoff and jitter. We do not retry when the download is interrupted by the user.

MD5 HASHES
If force is False, and a file already exists on disk, the md5 hash of the file is compared to the md5 hash of the file on the server. If the hashes match, the file is skipped.
If force is True, then the file is downloaded regardless.

FILTERING
The regex parameter can be used to filter the files that are downloaded. If the regex parameter is provided, only files whose relative path matches the regex using `re.search` will be downloaded. This means users can give a literal string and the downloader will download all files whose relative path contains that string.
"""

import base64
import contextlib
import hashlib
import logging
import os
import random
import re
import stat
import tempfile
import threading
import time
import traceback
import signal

from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import requests
from ciocore import api_client
from ciocore.downloader.log import LOGGER_NAME
from ciocore.downloader.registry import Registry
from pathlib import Path

logger = logging.getLogger(LOGGER_NAME)

DEFAULT_PAGE_SIZE = 50
DEFAULT_NUM_THREADS = 4
DEFAULT_PROGRESS_INTERVAL = 0.5
CHUNK_SIZE = 1024
DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_DELAY = 1
DEFAULT_JITTER = 0.1

EVENT_TYPE_START = "start"
EVENT_TYPE_START_TASK = "start_task"
EVENT_TYPE_FILE_DONE = "file_done"
EVENT_TYPE_TASK_DONE = "task_done"
EVENT_TYPE_DONE = "done"
EVENT_TYPE_PROGRESS = "progress"

FALLBACK_DOWNLOADS_FOLDER = "CONDUCTOR_DOWNLOADS"

class UserInterrupted(Exception):
    pass

@contextlib.contextmanager
def temp_file(filepath):
    """
    Create a temporary file to use instead of the input filepath.

    The input doesn't have to exist. If it does exist, it will ultimately be overwritten.
    This context manager yields a path to a temporary file which will replace the original
    file when the context is exited.
    """
    target_path = Path(filepath)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # Create temporary file in the same directory as the target.
    # Descriptor is automatically closed on exiting the `with`.
    with tempfile.NamedTemporaryFile(
        prefix=target_path.name, dir=str(target_path.parent), delete=False
    ) as tmp:
        temp_file_path = Path(tmp.name)  # Save the temporary file path to move it later

    try:
        yield temp_file_path  # Yield control back to the caller, with the temp file path

        # Move the temporary file to the target location, effectively overwriting it
        temp_file_path.replace(target_path)

        # Set permissions to 664
        target_path.chmod(
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH
        )
    finally:
        # Clean up temporary file if it still exists
        if temp_file_path and temp_file_path.exists():
            temp_file_path.unlink()

class BaseDownloader(object):

    WORK_QUEUE_THROTTLE = 0.1
    EVENT_DISPATCHER_PAUSE = 0.1

    VALID_EVENTS = [
        EVENT_TYPE_START,
        EVENT_TYPE_START_TASK,
        EVENT_TYPE_PROGRESS,
        EVENT_TYPE_TASK_DONE,
        EVENT_TYPE_FILE_DONE,
        EVENT_TYPE_DONE,
    ]

    @contextlib.contextmanager
    def start_end_events(self):
        """Send start and end events to the event queue."""
        self.emit_start_event()
        try:
            yield
        finally:
            self.emit_end_event()


    @contextlib.contextmanager
    def event_queue_context(self):
        """Send start and end events to the event queue."""
        self.event_queue = Queue()
        event_dispatcher_thread = threading.Thread(target=self.dispatch_events)
        event_dispatcher_thread.start()
        try:
            yield
        finally:
            logger.debug("Waiting for event dispatcher thread to finish")
            event_dispatcher_thread.join()


    def __init__(
        self,
        output_path=None,
        num_threads=DEFAULT_NUM_THREADS,
        progress_interval=DEFAULT_PROGRESS_INTERVAL,
        page_size=DEFAULT_PAGE_SIZE,
        force=False,
        regex=None,
        max_attempts=DEFAULT_MAX_ATTEMPTS,
        delay=DEFAULT_DELAY,
        jitter=DEFAULT_JITTER,
        client=api_client.ApiClient(),
    ):
        """Initialize the downloader."""
        self.output_path = output_path
        self.force = force
        self.num_threads = num_threads
        self.max_queue_size = num_threads * 2
        self.progress_interval = progress_interval / 1000.0
        self.page_size = page_size if page_size > 1 else None
        self.client = client
        self.max_attempts = max_attempts
        self.delay = delay
        self.jitter = jitter
        self.regex = re.compile(regex) if regex else None
        self.interrupt_flag = threading.Event()
        self.registry_lock = threading.Lock()

        self.event_queue = None

        self.callbacks = {
            EVENT_TYPE_START: [],
            EVENT_TYPE_START_TASK: [],
            EVENT_TYPE_PROGRESS: [],
            EVENT_TYPE_TASK_DONE: [],
            EVENT_TYPE_FILE_DONE: [],
            EVENT_TYPE_DONE: [],
        }

        # A registry of tasks that are in progress.
        self.registry = Registry()

        logger.debug("Output_path: %s", self.output_path)
        logger.debug("Force download: %s", self.force)
        logger.debug("Num threads: %s", self.num_threads)
        logger.debug("Max queue size: %s", self.max_queue_size)
        logger.debug("Progress interval: %s seconds", self.progress_interval)
        logger.debug("Page limit: %s", self.page_size)
        logger.debug("Instantiated client: %s", self.client)
        logger.debug("Max attempts: %s", self.max_attempts)
        logger.debug("Delay: %s", self.delay)
        logger.debug("Jitter: %s", self.jitter)
        logger.debug("Regex: %s", self.regex)


    def filter_task(self, task):
        """Use a regex to Filter out files from a task."""
        if not self.regex:
            return task

        filtered_files = [file for file in task['files'] if self.regex.search(file['relative_path'])]
        new_size = sum(file['size'] for file in filtered_files)
        new_task = {
            'download_id': task['download_id'],
            'files': filtered_files,
            'job_id': task['job_id'],
            'output_dir': task['output_dir'],
            'size': new_size,
            'task_id': task['task_id']
        }
        return new_task

    def filter(self, tasks):
        """Filter out files from tasks."""
        return list(map(self.filter_task, tasks))

    def handle_interrupt(self, *args):
        """
        Handle the first interrupt signal by setting the interrupt flag.
        """
        if not self.interrupt_flag.is_set():
            logger.warning("INTERRUPTED! CLEANING UP. PLEASE BE PATIENT...")
            self.interrupt_flag.set()
            # Ignore further SIGINT signals by setting the handler to a new function that just logs a message
            signal.signal(signal.SIGINT, self.handle_subsequent_interrupts)

    def handle_subsequent_interrupts(self, *args):
        """
        Handle subsequent interrupt signals by logging a less polite message.
        """
        logger.warning(
            " I SAID BE PATIENT. THE DOWNLOAD HAS BEEN CANCELLED BUT I AM STILL CLEANING UP!"
        )

    def run(self):
        """Run the downloader.

        For each job, we request pages of tasks, and then download each file from each task in a
        thread.
        """
        logger.debug("Running the downloader")
        self.interrupt_flag.clear()

        # Set the initial signal handler for (Ctrl+C) so that we can clean up if the user interrupts the download.
        signal.signal(signal.SIGINT, self.handle_interrupt)

        with self.event_queue_context():
            with self.start_end_events():

                # Run a loop that fetches pages of tasks from the server.
                # next_locator can be determined by the implementation of get_some_tasks().
                # It is fed in and returned each loop.
                # If it is returned as None, the loop will end.
                try:
                    with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                        next_locator = None
                        while not self.interrupt_flag.is_set():
                            tasks, next_locator = self.get_some_tasks(next_locator)
                            if tasks:
                                self.download_tasks(tasks, executor)
                            if not next_locator or self.interrupt_flag.is_set():
                                break
                            # To test, we could fake an exception here.
                
                except Exception:  # Catch all exceptions
                    # Let the workers know they should stop
                    self.interrupt_flag.set()
                finally:
                    logger.debug("Shutting down...")
                    executor.shutdown(wait=True)

    def get_some_tasks(self, locator):
        """Get a page of tasks from the server."""
        raise NotImplementedError

    def download_tasks(self, tasks, executor):
        """Run a page of download tasks using a thread pool executor.

        Parameters:
            - tasks (list): A list of task dictionaries to be processed.
            - executor (ThreadPoolExecutor): The executor for running download tasks concurrently.
        """
        logger.debug("Downloading page:")

        for task_info in tasks:
            if not self.registry.register_task(task_info):
                # register_task returns none if the task is already in the registry. 
                continue

            self.emit_start_task_event(task_info)
            for file_info in task_info["files"]:

                file_info["output_dir"] = self.ensure_writable_output_path(file_info, task_info)
                file_info["filepath"] = os.path.join(file_info["output_dir"], file_info["relative_path"])

                future = executor.submit(self.attempt_download, file_info)
                # Upon completion, put the result in the event queue.
                future.add_done_callback(lambda f: self.event_queue.put(f.result()))
                
                # pylint: disable=protected-access
                while executor._work_queue.qsize() > self.max_queue_size:
                    # Throttle to prevent the queue from growing too large.
                    time.sleep(self.WORK_QUEUE_THROTTLE)


    def attempt_download(self, file_info):
        """
        Attempt to download a file with exponential backoff retries.
        
        Parameters:
            - file_info (dict): A dictionary containing information about the file to be downloaded.
        
        Returns:
            - file_done_event: A dictionary indicating the completion status of the download.
        """
        filepath = file_info["filepath"]
        attempts_remaining = self.max_attempts
        retry_delay = self.delay

        while True:
            try:
                # Try to download the file.
                file_done_event = self.download(file_info)
                return file_done_event  # Return the event if download is successful.

            except UserInterrupted as ex:
                # Handle user interruption.
                file_done_event = self.generate_file_done_event(
                    file_info, error=str(ex)
                )
                break

            except Exception as ex:
                # Decrement the remaining attempts.
                attempts_remaining -= 1

                if attempts_remaining <= 0:
                    # If no attempts left, log the error and stop trying.
                    traceback_str = traceback.format_exc()
                    error_str = f"{ex}\nTraceback:\n{traceback_str}"
                    file_done_event = self.generate_file_done_event(
                        file_info, error=error_str
                    )
                    logger.exception(
                        "Failed to download %s after %d attempts.", 
                        filepath, 
                        self.max_attempts
                    )
                    break  # Exit the loop if all attempts are exhausted.

                else:
                    # If there are still attempts left, wait for the retry delay.
                    time.sleep(retry_delay)
                    # Calculate the next delay using exponential backoff with jitter.
                    retry_delay *= 2
                    retry_delay += random.uniform(0, retry_delay * self.jitter)

                    logger.exception(
                        "Failed to download %s. Retrying in %f seconds. %d attempts left.", 
                        filepath, 
                        retry_delay, 
                        attempts_remaining
                    )
 
        # Return the final file done event after all attempts.
        return file_done_event


    def ensure_writable_output_path(self,file_info,task_info):
        """
        Resolve the output directory for the file. 
        If the file's output directory is from a Windows machine, we provisionally use the fallback directory.

        If the output_path is not writable, we try to use a fallback directory. If that fails, we use the temp folder.
        """

        output_path = file_info["output_dir"]
        if os.name == "posix":
            if re.match(r"^[a-zA-Z]:", output_path):
                self.output_path =  os.path.expanduser(os.path.join("~", FALLBACK_DOWNLOADS_FOLDER))

        if self.output_path:
            output_path =  os.path.join(self.output_path, task_info["job_id"])

        try:
            os.makedirs(output_path, exist_ok=True)
            return output_path
        except Exception:
            logger.exception("Can't use specified output directory %s. Trying fallback", output_path) 

        output_path = os.path.expanduser(os.path.join("~", FALLBACK_DOWNLOADS_FOLDER, task_info["job_id"]))
        try:
            os.makedirs(output_path, exist_ok=True)
            return output_path
        except Exception:
            logger.exception("Can't use fallback output directory %s. Trying temp folder", output_path) 
        return os.path.join(tempfile.gettempdir(), FALLBACK_DOWNLOADS_FOLDER, task_info["job_id"])


    def can_skip(self, file_info):
        """Determine if a file download should be skipped.

        It can be skipped if it exists already with the same content. In this case we return a file_done event dict with preexisting=True. The event is put in the event queue by the calling function.
        """

        if self.force:
            return False

        filepath = file_info["filepath"]
        if not os.path.exists(filepath):
            return False

        try:
            existing_md5 = self._generate_base64_md5(filepath)
            download_md5 = file_info.get("md5", "none")
            if existing_md5 != download_md5:
                return False
        except Exception:
            logger.exception("Error checking md5 for %s", filepath)
            return False

        return self.generate_file_done_event(file_info, preexisting=True)

    def download(self, file_info):
        """
        Do the work of downloading a file.

        Use a temp file to avoid corrupting the original file if the download fails.
        """
        skip_result = self.can_skip(file_info)
        if skip_result:
            return skip_result

        size = file_info["size"]
        filepath = os.path.join(file_info["output_dir"], file_info["relative_path"])

        logger.debug("Downloading file: %s", filepath)

        with temp_file(filepath) as safe_filepath:
            response = requests.get(file_info["url"], stream=True, timeout=60)
            size = float(response.headers.get("content-length", 0))
            progress_bytes = 0
            last_poll = time.time()
            with open(safe_filepath, "wb") as file_handle:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    # check if the download has been interrupted
                    if self.interrupt_flag.is_set():

                        raise UserInterrupted("Download interrupted by user.")

                    if not chunk:
                        continue
                    file_handle.write(chunk)

                    progress_bytes += len(chunk)
                    last_poll = self.emit_progress_event(
                        filepath, progress_bytes, size, last_poll
                    )

            response.raise_for_status()

        return self.generate_file_done_event(file_info)

    def dispatch_events(self):
        """
        Pull events from the event queue as they are ready and call the appropriate callbacks.
        """
        while True:
            #  Get the next event from the queue
            evt = self.event_queue.get()
            event_type = evt["type"]

            # Call all registered callbacks for the event
            for callback in self.callbacks[event_type]:
                callback(evt)

            # If there are any callbacks registered for the task_done event, 
            # then we check if the event is a file_done event and if so, determine
            # whether the whole task is done. 
            # If the task is done, call its callbacks.
            if event_type == EVENT_TYPE_FILE_DONE:
                if len(self.callbacks[EVENT_TYPE_TASK_DONE]) > 0:
                    task_done_event = self.generate_task_done_event(evt)
                    if task_done_event:
                        for callback in self.callbacks[EVENT_TYPE_TASK_DONE]:
                            callback(task_done_event)

            if event_type == EVENT_TYPE_DONE:
                break

    def generate_task_done_event(self, evt):
        """
        Build task_done event from file_done event and the registry.
        
        Only do this is the file count for the task is complete.
        """
        event_type = evt["type"]
        # We don't want to update the registry if the file_done event is an error.
        # Ignoring it ensures that it will eventually be reported back to the server as pending.
        if event_type != EVENT_TYPE_FILE_DONE or evt.get("error"):
            return None

        # Increment the number of downloaded files for the task
        updated_task = self.registry.update_task(evt)

        if not updated_task:  # should never happen
            return None

        if updated_task["completed_files"] >= updated_task["filecount"]:
            return {
                "type": EVENT_TYPE_TASK_DONE,
                "job_id": evt["job_id"],
                "task_id": evt["task_id"],
                "download_id": updated_task["download_id"],
                "filecount": updated_task["filecount"],
                "preexisting": updated_task["preexisting_files"]
                == updated_task["filecount"],
                "size": updated_task["size"],
            }

        return None

    ############## METHODS TO CONSTRUCT AND EMIT EVENTS #####################
    def emit_start_task_event(self, task):
        """Send a start_task event to the event queue."""
        self.event_queue.put(
            {
                "type": EVENT_TYPE_START_TASK,
                "download_id": task["download_id"],
                "filecount": len(task["files"]),
                "task_id": task["task_id"],
                "job_id": task["job_id"],
                "size": task["size"],
            }
        )

    def emit_progress_event(self, filepath, progress_bytes, size, last_poll):
        """Send a progress event to the event queue if it's time to do so."""
        now = time.time()
        if now >= last_poll + self.progress_interval:
            last_poll = now
            self.event_queue.put(
                {
                    "type": EVENT_TYPE_PROGRESS,
                    "filepath": filepath,
                    "progress_bytes": progress_bytes,
                    "size": size,
                }
            )
        return last_poll

    def emit_start_event(self):
        """Send start event to the event queue."""
        self.event_queue.put(
            {
                "type": EVENT_TYPE_START,
                "num_threads": self.num_threads,
                "page_size": self.page_size,
            }
        )

    def emit_end_event(self):
        """Send done event to the event queue.

        Send along the registry so that any callbacks can check if any tasks were not completed.
        """
        self.event_queue.put({"type": EVENT_TYPE_DONE, "registry": self.registry})

    @staticmethod
    def generate_file_done_event(file, **kwargs):
        result = {
            "type": EVENT_TYPE_FILE_DONE,
            "job_id": file["job_id"],
            "task_id": file["task_id"],
            "filepath": file["filepath"],
            "md5": file["md5"],
            "size": file["size"],
            "preexisting": False,
            "error": None,
        }
        # If the preexisting key is in kwargs, merge it in the result dict.
        return {**result, **kwargs}

    ################################################################

    def on(self, event_type, callback):
        """Register a callback function.

        Args:
            event_type (str): The name of the callback. Must be one of the values in VALID_EVENTS.
            callback (function): The callback function. Must accept one argument named 'evt'.
        Raises:
            ValueError: If the event_type is not in VALID_EVENTS.

        Examples:
            >>> def my_callback(evt):
            ...     print(evt)

            >>> downloader = BaseDownloader(jobs)
            >>> downloader.on("start", my_callback)

        """
        if event_type not in self.VALID_EVENTS:
            raise ValueError(
                f"Invalid event_type: {event_type}. Allowed values: {self.VALID_EVENTS}"
            )
        self._validate_callback(callback)
        self.callbacks[event_type].append(callback)

    @staticmethod
    def _validate_callback(callback):
        """Make sure the callback is a callable function with one argument named 'evt'.

        The callback could be a method of another class, in which case the first argument will be 'self'. We account for this too.
        """
        if not callable(callback):
            raise ValueError("Callback must be a callable function.")
        num_args = callback.__code__.co_argcount

        arg_names = callback.__code__.co_varnames[:num_args]

        if num_args > 2 or (num_args == 2 and arg_names[0] != "self"):
            raise ValueError(f"Too many args. Found {num_args} arguments: {arg_names}")

        if num_args < 1 or arg_names[-1] != "evt":
            raise ValueError("Callback is missing the named argument 'evt'.")
        return True

    @staticmethod
    def _generate_base64_md5(filename):
        """Generate the base64 md5 hash of a file.
        
        This is used to determine if a file on disk is the same as a file on the server.
        """
        with open(filename, "rb") as file:
            md5_hash = hashlib.md5()
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hash.update(chunk)
            md5_digest = md5_hash.digest()
            md5_base64 = base64.b64encode(md5_digest)
            return md5_base64.decode("utf-8")
