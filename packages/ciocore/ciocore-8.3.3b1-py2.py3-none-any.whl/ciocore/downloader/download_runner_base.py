"""
Base Download runner

This module contains the DownloadRunnerBase class. 

The DownloadRunnerBase is responsible for running one of the downloader classes: JobDownloader or PerpetualDownloader. If there are no jobids, it runs the PerpetualDownloader.

It also sets up a Reporter to report task status back to the server.

By design, derived classes need only be concerned with registering callbacks. See the LoggingDownloadRunner class for an example.

"""

import logging
from ciocore.downloader.job_downloader import JobDownloader
from ciocore.downloader.perpetual_downloader import PerpetualDownloader
from ciocore.downloader.log import LOGGER_NAME
from ciocore.downloader.reporter import Reporter

logger = logging.getLogger(LOGGER_NAME)

class DownloadRunnerBase(object):
    CLIENT_NAME = "DownloadRunnerBase"

    def __init__(self, jobids=None, location=None, **kwargs):
        """
        Initialize the downloader.
        """
        self.disable_reporting = kwargs.pop("disable_reporting")
        self.num_reporter_threads = kwargs.get("num_threads", 1)
        if jobids:
            self.downloader = JobDownloader(jobids, **kwargs)
        else:
            self.downloader = PerpetualDownloader(location, **kwargs)

    def run(self):
        """
        Run the downloader.

        Optionally wrap the downloader in a reporter to report task statuses back to the server.
        """
        if self.disable_reporting:
            self.downloader.run()
        else:
            with Reporter(self.downloader, num_threads=self.num_reporter_threads):
                self.downloader.run()

