
from ciocore.downloader.job_downloader import JobDownloader, flatten
import unittest
from unittest import mock
from ciocore.downloader.base_downloader import temp_file
import tempfile
import shutil
import os
import stat
import contextlib

class TempFileTests(unittest.TestCase):

    def test_temp_file_creation(self):
        # Create a temporary file and test if it exists
        with temp_file("tests/files/file.txt") as temp_path:
            self.assertTrue(os.path.exists(temp_path))
            self.assertTrue(os.access(temp_path, os.W_OK & os.R_OK))

    def test_temp_file_overwrite_existing(self):
        # Test if existing file is overwritten by the temporary file
        # Create a dummy file at the specified path
        os.makedirs("tests/files", exist_ok=True)
        with open("tests/files/file.txt", "w") as f:
            f.write("dummy content")

        # Replace the file with a temporary file and check the content
        with temp_file("tests/files/file.txt") as temp_path:
            with open(temp_path, "r") as tf:
                content = tf.read()
            self.assertEqual(content, "")

    def test_temp_file_cleanup(self):
        with temp_file("tests/files/file.txt") as temp_path:
            pass  # Do nothing
        self.assertFalse(os.path.exists(temp_path))
        
class TestJobDownloaderFlatten(unittest.TestCase):

    def test_pad_job_id(self):
        input = ("1234",)
        result = flatten(input)
        self.assertEqual(result, [{"job_id": "01234", "task_ids":None}])

    def test_several_job_ids(self):
        input = ("1234","1235","1236")
        result = flatten(input)
        self.assertEqual(result, [
            {"job_id": "01234", "task_ids":None},
            {"job_id": "01235", "task_ids":None},
            {"job_id": "01236", "task_ids":None}
            ])

    def test_job_and_tasks(self):
        input = ("1234:1-7x2,10",)
        result = flatten(input)
        self.assertEqual(result, [{"job_id": "01234", "task_ids":["001","003","005","007","010"]}])

    def test_several_job_and_tasks(self):
        input = ("1234:1-7x2,10","1235:12-15")
        result = flatten(input)
        self.assertEqual(result, [
            {"job_id": "01234", "task_ids":["001","003","005","007","010"]},
            {"job_id": "01235", "task_ids":["012","013","014","015"]}
            ])

    def test_mix_job_and_job_with_tasks(self):
        input = ("1234","1235:12-15")
        result = flatten(input)
        self.assertEqual(result, [
            {"job_id": "01234", "task_ids":None},
            {"job_id": "01235", "task_ids":["012","013","014","015"]}
            ])

    def test_invalid_range_downloads_whole_job(self):
        # Someone might have a bunch of stuff queued up and made a mistake and left for the night.
        # We should download the whole job in this case so they don't have to restart the dl in the
        # morning.
        input = ("1234:badrange",)
        result = flatten(input)
        self.assertEqual(result, [
            {"job_id": "01234", "task_ids":None}
            ])

class TestJobDownloaderGetSomeTasks(unittest.TestCase):
    def setUp(self):
        # Create a mock instance of JobDownloader
        self.obj = JobDownloader(jobs=["00000"])

    @mock.patch("ciocore.downloader.job_downloader.logger.error")
    def test_get_some_tasks_error(self, mock_error):
        # Mock the api client to return an error
        mock_api_client = mock.Mock()
        response = '{"error": "some error message"}'
        code = 404
        mock_api_client.make_request.return_value = (response, code)
        self.obj.client = mock_api_client
        # call get_some_tasks
        tasks, locator = self.obj.get_some_tasks({})

        self.assertEqual(tasks, [])
        self.assertIsNone(locator)
        mock_error.assert_called_with(
            'Error fetching download info for job ID: %s : %s : %s', '00000', '/jobs/00000/downloads', mock.ANY)

    def test_get_some_tasks_success(self):
        mock_api_client = mock.Mock()
        # Mock the api client to return a batch of tasks and a next cursor
        response = '{"downloads": [{"id": 1, "name": "task1"}, {"id": 2, "name": "task2"}], "next_cursor": "1234"}'
        code = 201
        mock_api_client.make_request.return_value = (response, code)
        self.obj.client = mock_api_client
        self.obj.jobs = [{"job_id": "00000", "task_ids": [1, 2]}]
        # call get_some_tasks with a locator
        tasks, locator = self.obj.get_some_tasks({"job_index": 0, "cursor": None})

        self.assertEqual(tasks, [{"id": 1, "name": "task1"}, {"id": 2, "name": "task2"}])
        self.assertEqual(locator, {"job_index": 0, "cursor": "1234"})
