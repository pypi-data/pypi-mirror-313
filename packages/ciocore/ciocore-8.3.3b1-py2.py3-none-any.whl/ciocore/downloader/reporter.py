"""
This module contains the Reporter class. 

It registers callbacks with the with the provided downloader instance that allow it to report "downloaded" or "pending" status back to the server.

It is set up in the download_runner_base module. Classes that derive from DownloadRunnerBase, such as LoggingDownloadRunner, do not need to be concerned with the details of the Reporter class.
"""

import json
import logging
from concurrent.futures import ThreadPoolExecutor

from ciocore import api_client
from ciocore.downloader.log import LOGGER_NAME

STATUS_ENDPOINT = "/downloads/status"
STATUS_DOWNLOADED = "downloaded"
STATUS_PENDING = "pending"

logger = logging.getLogger(LOGGER_NAME)
 
class Reporter(object):

    def __init__(self, downloader, client=api_client.ApiClient(), num_threads=1):

        self.downloader = downloader

        self.num_threads = num_threads
        self.client = client
        self.executor = None

        logger.debug("Assigning reporter callbacks")
        self.downloader.on("task_done", self.on_task_done)
        self.downloader.on("done", self.on_done)

    def __enter__(self):
        self.executor = ThreadPoolExecutor(max_workers=self.num_threads)
        return self  # Optionally return this reporter

    def __exit__(self, exc_type, exc_value, traceback):
        self.executor.shutdown()
        # Handle exceptions, from inside the with block
        if exc_type:
            logger.exception("Error running downloader: %s", exc_value)
            # return False to propagate the exception
            return False
            


    def report_task_status(
        self, download_id, status=STATUS_DOWNLOADED, bytes_in_task=0
    ):
        """
        Make a request to the server to report the status of a task.

        If the user interrupted the download, then we set the task status to pending to be safe.
        """
        if self.downloader.interrupt_flag.is_set():
            status = STATUS_PENDING

        bytes_to_download = 0 if status == STATUS_DOWNLOADED else bytes_in_task

        data = {
            "download_id": download_id,
            "status": status,
            "bytes_downloaded": 0,
            "bytes_to_download": bytes_to_download,
        }
        json_data = json.dumps(data)
        try:
            self.client.make_request(STATUS_ENDPOINT, data=json_data, use_api_key=True)
        except Exception as exc:
            data["error"] = str(exc)
        return data

    def on_task_done(self, evt):
        """
        Callback to run on a task-done event. Report status back to the server.
        
        Note, the task may consist entirely of preexisting files. Nevertheless, we report the task as downloaded.
        """

        future = self.executor.submit(
            self.report_task_status,
            evt["download_id"],
            status=STATUS_DOWNLOADED,
            bytes_in_task=evt["size"],
        )
        future.add_done_callback(
            lambda f, job_id=evt["job_id"], task_id=evt["task_id"]: log_report_result(
                f.result(), job_id, task_id
            )
        )

    def on_done(self, evt):
        """
        When the job is done, check to see if any tasks were not completed.

        If we find any, then report them back to the server as pending.
        """
        logger.debug("Download done. Reporting remaining task statuses to server")
        for job_id, task_id, task in evt["registry"].each():
            if task["completed_files"] < task["filecount"]:

                future = self.executor.submit(
                    self.report_task_status,
                    task["download_id"],
                    status=STATUS_PENDING,
                    bytes_in_task=task["size"],
                )
                future.add_done_callback(
                    lambda f, job_id=job_id, task_id=task_id: log_report_result(
                        f.result(), job_id, task_id
                    )
                )


def log_report_result(report_result, job_id, task_id):
    """Log the report result."""
    if report_result.get("error"):
        logger.error(
            "Error reporting task to server:  %s:%s (%s) %s",
            job_id,
            task_id,
            report_result["download_id"],
            report_result["error"],
        )
        return
    logger.debug(
        "Reported task to server: %s:%s (%s) %s",
        job_id,
        task_id,
        report_result["download_id"],
        report_result["status"],
    )
