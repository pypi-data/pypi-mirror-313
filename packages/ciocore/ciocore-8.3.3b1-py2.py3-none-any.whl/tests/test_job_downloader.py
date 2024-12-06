from ciocore.downloader.job_downloader import JobDownloader, flatten
import unittest
from unittest import mock
import re
import json

DOWNLOAD_BATCHES = {
    "00000": [
        {
            "next_cursor": "00000_1",
            "downloads": [
                {
                    "download_id": 1,
                    "files": [
                        {"url": "https://example.com/file1", "size": 100},
                        {"url": "https://example.com/file2", "size": 200},
                    ],
                },
                {
                    "download_id": 2,
                    "files": [
                        {"url": "https://example.com/file3", "size": 100},
                        {"url": "https://example.com/file4", "size": 200},
                    ],
                },
            ],
        },
        {
            "next_cursor": "00000_2",
            "downloads": [
                {
                    "download_id": 3,
                    "files": [
                        {"url": "https://example.com/file5", "size": 100},
                        {"url": "https://example.com/file6", "size": 200},
                    ],
                },
                {
                    "download_id": 4,
                    "files": [
                        {"url": "https://example.com/file7", "size": 100},
                        {"url": "https://example.com/file8", "size": 200},
                    ],
                },
            ],
        },
        {
            "next_cursor": None,
            "downloads": [
                {
                    "download_id": 5,
                    "files": [
                        {"url": "https://example.com/file9", "size": 100},
                        {"url": "https://example.com/file10", "size": 200},
                    ],
                }
            ],
        },
    ],
    "00001": [
        {
            "next_cursor": "00001_1",
            "downloads": [
                {
                    "download_id": 101,
                    "files": [
                        {"url": "https://example.com/file101", "size": 100},
                        {"url": "https://example.com/file102", "size": 200},
                    ],
                },
                {
                    "download_id": 102,
                    "files": [
                        {"url": "https://example.com/file103", "size": 100},
                        {"url": "https://example.com/file104", "size": 200},
                    ],
                },
            ],
        },
        {
            "next_cursor": "00001_2",
            "downloads": [
                {
                    "download_id": 103,
                    "files": [
                        {"url": "https://example.com/file105", "size": 100},
                        {"url": "https://example.com/file106", "size": 200},
                    ],
                },
                {
                    "download_id": 104,
                    "files": [
                        {"url": "https://example.com/file107", "size": 100},
                        {"url": "https://example.com/file108", "size": 200},
                    ],
                },
            ],
        },
        {
            "next_cursor": None,
            "downloads": [
                {
                    "download_id": 105,
                    "files": [
                        {"url": "https://example.com/file109", "size": 100},
                        {"url": "https://example.com/file110", "size": 200},
                    ],
                }
            ],
        },
    ],
}

class MockedApiClient:
    def _get_batch(self, cursor):
        if not cursor:
            return json.dumps(DOWNLOAD_BATCHES["00000"][0])
        
        job_id, index = cursor.split("_")
        index = int(index)
        batch = json.dumps(DOWNLOAD_BATCHES[job_id][index])
        return batch

    def make_request(self, url, verb="POST", params=None, data=None, use_api_key=True):
        m = re.match("/jobs/(\d{5})/downloads", url)
        if m:
            job_id = m.group(1)
            # This is a request for a download batch
            if not job_id in DOWNLOAD_BATCHES:
                print(f"Job {job_id} not found")
                return None, 204
            else:
                print(f"Job {job_id} found")
            
            cursor = params.get("start_cursor", None)
            batch = self._get_batch(cursor)
            return batch, 201
        else:
            # This is not a request for a download batch
            raise NotImplementedError("This is not a request for a download batch")


class TestJobDownloader(unittest.TestCase):
    
    
    def setUp(self):
        download_tasks_patcher = mock.patch.object(JobDownloader,"download_tasks")
        self.mock_download_tasks = download_tasks_patcher.start()
        self.addCleanup(download_tasks_patcher.stop)
    

    def test_batch_all_batches(self):
        mocked_jobs = DOWNLOAD_BATCHES.keys()

        # instantiate
        jdl = JobDownloader(mocked_jobs)

        # set the mocked api client
        jdl.client = MockedApiClient()

        jdl.run()
        self.assertEqual(self.mock_download_tasks.call_count, 6)
        
#     def test_no_calls_if_non_existent_job(self):
#         mocked_jobs = ["00002"]
# ``
#         # instantiate
#         jdl = JobDownloader(mocked_jobs)

#         # set the mocked api client
#         jdl.client = MockedApiClient()

#         jdl.run()
#         self.assertEqual(self.mock_download_tasks.call_count, 0)


        # mock_get_some_tasks.side_effect = get_some_tasks_side_effect

        # tasks, locator = jdl.get_some_tasks(None)
        # self.assertEqual(tasks, ["t1,t2,t3"])
        # self.assertEqual(locator, {"job_index": 0, "cursor": "a"})

        # print(jdl.get_some_tasks(2))
        # print(jdl.get_some_tasks(3))

        #  with mock.patch('requests.get') as mock_get:
        #     # Construct the expected JSON response
        #     json_response = {
        #         "next_cursor": "AA",
        #         "downloads": [
        #             {
        #                 "download_id": 1,
        #                 "files": [
        #                     {
        #                         "url": "https://example.com/file1",
        #                         "size": 100
        #                     },
        #                     {
        #                         "url": "https://example.com/file2",
        #                         "size": 200
        #                     }
        #                 ]
        #             }
        #         ],
        #         "job_id": "00000",
        #         "output_dir": "/some/path",
        #         "size": 300,
        #         "task_id": "001"
        #     }
        #     # Create a mock response object
        #     mock_response = mock_get.return_value
        #     # Set the JSON content of the response
        #     mock_response.json.return_value = json_response
