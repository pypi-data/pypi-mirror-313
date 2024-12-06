"""
Perpetual Downloader

Not yet tested
"""
import json
import logging
import time
import sys
from ciocore.downloader.base_downloader import BaseDownloader
from ciocore.downloader.log import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

class PerpetualDownloader(BaseDownloader):
    CLIENT_NAME = "PerpetualDownloader"
    POLL_INTERVAL = 15
    URL = "/downloads/next"
    spinner = spinning_cursor()

    def __init__(self, location, *args, **kwargs):
        """Initialize the downloader."""
        super().__init__(*args, **kwargs)
        self.location = location
        logger.debug("Initializing perpetual downloader")

    def get_some_tasks(self, _):
        """Fetch the next batch of tasks from the server.

        Always set the return locator to True to signal that we should keep running this function.

        This function never throws an error. If something goes wrong, it just sets the task array to be empty.

        If tasks array is empty for any reason (error, filter, no tasks ready, etc.), it waits for POLL_INTERVAL seconds before trying again.
        """
        logger.debug("Fetching the next page of tasks")
        params = {"count": self.page_size, "location": self.location}
        tasks = []
        try:
            response, code = self.client.make_request(
                self.URL, params=params, use_api_key=True
            )
            if code <= 201:
                tasks = json.loads(response).get("data", [])
                tasks = self.filter(tasks)
        except Exception as exc:
            logger.error("Error fetching download info from: %s : %s", self.URL, exc)

        if not tasks:
            for _ in range(self.POLL_INTERVAL):
                spin_char = next(self.spinner)
                line = f"Listening for files to download... ({spin_char})"
                sys.stdout.write(line)
                sys.stdout.flush()
                sys.stdout.write('\b' * len(line))
                time.sleep(1)

        return tasks, True
