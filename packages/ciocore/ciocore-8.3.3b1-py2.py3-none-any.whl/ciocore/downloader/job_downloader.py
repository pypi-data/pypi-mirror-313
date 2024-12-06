"""
Job Downloader

Download output files from a Conductor job.

ENDPOINT
The outputs of a Conductor job are described in the response from the /jobs/{job_id}/downloads endpoint. The response is a list of tasks. Each task has a list of files. Each file (dict) has a signed URL plus other fields such as the md5 and fields describing the original path, size, and more.

PAGING
A job may contain thousands of tasks, each with several files. To reduce the time it takes to get started, this downloader makes requests for download information in batches, or pages. The number of tasks in each page is controlled by the page_size parameter. As soon as the first page of tasks is retrieved, we start downloading the files in threads. While the files are downloading, we fetch the next page of tasks. When the current page of tasks is exhausted, we start downloading the files in the next page of tasks. We continue until all tasks have been downloaded.

The get_some_tasks method is responsible for fetching the next page of tasks. It is called by the base class. It returns a list of tasks, and a locator. For this implementation, the locator is a dictionary containing the index of the current job, and the cursor for the next page of tasks for the job. A new locator is returned to the calling method so that it can be passed back to this method the next time it is called. When the calling method receives a falsey value for the locator, it knows that there are no more tasks to download.

See the documentation for the base downloader for more information about the locator and other behavior.
"""

import json
import logging
from cioseq.sequence import Sequence
from ciocore.downloader.base_downloader import BaseDownloader
from ciocore.downloader.log import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)


class JobDownloader(BaseDownloader):
    CLIENT_NAME = "JobDownloader"

    def __init__(self, jobs, *args, **kwargs):

        super().__init__(*args, **kwargs)
        """Initialize the downloader."""
        logger.debug("Initializing paged job downloader")
        self.jobs = flatten(jobs)
        self.location = None # location is not used in this downloader

    def get_some_tasks(self, locator):
        """Fetch the next page of tasks from the server.

        locator: a dictionary containing the index of the current job, and the cursor for the next page of tasks for the job.
 

        # What is a locator? It's the information needed to request the next page of tasks. It consists of the index of the current job, and the cursor for the next page of tasks. It is provided to this method as a parameter, and when we're done, a new locator is returned to the run loop. The run loop passes it back to us the next time it is called.

        # On the first call, the provided locator is None. In that case, we start with the first job, and no cursor.

        # We return the locator to the run loop in the base class, along with any tasks to be downloaded. If we return a falsy locator, the run loop is exited, since it means we downloaded everything OR there was an error fetching tasks.

        # If we got to the end of the current job, we increment the job index and reset the cursor to None. The next time this method is called, we'll start with the next job.

        # If we got a next_cursor from the request, we return it in the locator along with the current job index. This is what we'll be given on the next call.
        """
        
        if not locator:
            locator = {}

        job_index = locator.get("job_index", 0)
        cursor = locator.get("cursor", None)
        if job_index >= len(self.jobs):
            # return no tasks and no locator. Ends the download.
            return [], None

        # we have a job to download
        job_info = self.jobs[job_index]
        job_id = job_info["job_id"]
        task_ids = job_info["task_ids"]
        url = f"/jobs/{job_id}/downloads"
        data = json.dumps({"tids": task_ids})
        params = {"limit": self.page_size, "start_cursor": cursor}
        try:
            response, code = self.client.make_request(
                url, verb="POST", params=params, data=data, use_api_key=True
            )
            if code != 201:
                # we have an error. Return null locator to end the download
                raise Exception(f"Code: {code}")
        except Exception as exc:
            logger.error("Error fetching download info for job ID: %s : %s : %s", job_id, url, exc)
            return [], None
        page = json.loads(response)
        tasks = page.get("downloads", [])

        tasks = self.filter(tasks)
        
        next_cursor = page.get("next_cursor")

        if not next_cursor:
            # we're done with this job
            job_index += 1

        return tasks, {"job_index": job_index, "cursor": next_cursor}


def flatten(job_specs):
    """Create a list of job objects with keys: job_id and tasks.

    See tests/test_downloader.py for examples.

    Example input:  ["1234", "1235:12-15"]

    Example result:
    [
        {"job_id": "01234", "task_ids":None},
        {"job_id": "01235", "task_ids":["012","013","014","015"]}
    ]
    """
    result = []
    for job_spec in job_specs:
        if ":" in job_spec:
            job_id, range_spec = job_spec.split(":")
            try:
                seq = Sequence.create(range_spec)
                task_ids = seq.expand("###")
            except (ValueError, TypeError):
                task_ids = None
        else:
            job_id, task_ids = job_spec, None
            task_ids = None
        result.append({"job_id": job_id.zfill(5), "task_ids": task_ids})
    return result
