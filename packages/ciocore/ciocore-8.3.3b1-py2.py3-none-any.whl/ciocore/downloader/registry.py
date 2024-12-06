import copy

import threading
import logging
from ciocore.downloader.log import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class Registry(object):

    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def get_copy(self):
        """
        Get a copy of the registry.

        Use a lock to ensure the registry is not modified while we're copying it.
        """
        with self.lock:
            return copy.deepcopy(self.data)

    def each(self):
        """
        Iterate over all tasks in the registry.

        Use a lock to ensure the registry is not modified while we're iterating over it.
        """
        with self.lock:
            for job_id, job in self.data.items():
                for task_id, task in job.items():
                    yield job_id, task_id, task

    def register_task(self, task_info):
        """
        Register a task as active

        The registry is accessed in a thread-safe manner using a lock.
        """
        job_id = task_info["job_id"]
        task_id = task_info["task_id"]
        with self.lock:
            if job_id not in self.data:
                self.data[job_id] = {}

            if task_id in self.data[job_id]:
                logger.debug(
                    "Task %s for job %s is already in registry. Skipping.",
                    task_id,
                    job_id,
                )
                return False

            self.data[job_id][task_id] = {
                "download_id": task_info["download_id"],
                "filecount": len(task_info["files"]),
                "completed_files": 0,
                "preexisting_files": 0,
                "size": task_info["size"],
            }
        return True

    def update_task(self, file_done_event):
        """
        Update the registry each time a file is done.

        Access the registry in a thread-safe manner using a lock.

        Steps:
        1. Get the task from the registry
        2. Increment the completed_files count
        3. If the file was preexisting, increment the preexisting_files count too
        4. If the task is now complete:
            c. Remove the task from the registry
        5. Return the task copy so that the event_dispatcher can let handlers know the task is done.

        """

        job_id = file_done_event["job_id"]
        task_id = file_done_event["task_id"]
        with self.lock:
            task = self.data.get(job_id, {}).get(task_id)
            if  not task:
                return None
            task["completed_files"] += 1
            if file_done_event["preexisting"]:
                task["preexisting_files"] += 1

            task_copy = task.copy()

            # Only really need ==, but I'm paranoid
            if task["completed_files"] >= task["filecount"]:
                del self.data[job_id][task_id]

        return task_copy
