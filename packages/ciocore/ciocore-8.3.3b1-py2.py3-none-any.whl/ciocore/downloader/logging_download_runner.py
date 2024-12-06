"""
Logging Download runner

This module contains the LoggingDownloadRunner class. 

The LoggingDownloadRunner is a derived class of DownloadRunnerBase.

It registers callbacks that are called when certain events occur during the download. 
It uses these callbacks to display progress via the logging module.

"""

import logging
from ciocore.downloader.download_runner_base import DownloadRunnerBase
from ciocore.downloader.log import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class LoggingDownloadRunner(DownloadRunnerBase):
    CLIENT_NAME = "LoggingDownloadRunner"

    def __init__(self, jobids=None, location=None, **kwargs):

        super().__init__(jobids, location, **kwargs)

        logger.debug("Assigning callbacks")
        self.downloader.on("start", self.on_start)
        self.downloader.on("start_task", self.on_start_task)
        self.downloader.on("progress", self.on_progress)
        self.downloader.on("file_done", self.on_file_done)
        self.downloader.on("task_done", self.on_task_done)
        self.downloader.on("done", self.on_done)

    def on_start(self, evt):
        logger.info("Starting download")

    def on_start_task(self, evt):
        logger.info("Starting task %s:%s", evt["job_id"], evt["task_id"])

    def on_progress(self, evt):
        percent = 0
        if evt["size"] and evt["progress_bytes"]:
            percent = round(evt["progress_bytes"] / evt["size"] * 100, 2)
        logger.info("Progress: %s %.2f%%", evt["filepath"], percent)

    def on_file_done(self, evt):
        if evt["error"]:
            logger.warning(
                "File done with error: %s:%s:%s %s",
                evt["job_id"],
                evt["task_id"],
                evt["filepath"],
                evt["error"],
            )
        else:
            logger.info(
                "File done %s:%s:%s", evt["job_id"], evt["task_id"], evt["filepath"]
            )

    def on_task_done(self, evt):
        if evt["preexisting"]:
            logger.info(
                "Task already existed locally %s:%s", evt["job_id"], evt["task_id"]
            )
        else:
            logger.info("Task done %s:%s", evt["job_id"], evt["task_id"])

    def on_done(self, evt):
        """
        When the job is done, check to see if any tasks were not completed.
        """
        logger.info("Download finished")
        empty = True
        for job_id, task_id, task in evt["registry"].each():
            if task["completed_files"] < task["filecount"]:
                logger.warning(
                    "Task not fully downloaded %s:%s: %s/%s files.",
                    job_id,
                    task_id,
                    task["completed_files"],
                    task["filecount"],
                )
                empty = False

        if empty:
            logger.info("No failed tasks.")
