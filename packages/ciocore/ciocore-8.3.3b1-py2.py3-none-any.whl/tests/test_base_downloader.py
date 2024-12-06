from ciocore.downloader.base_downloader import (
    BaseDownloader,
    DEFAULT_NUM_THREADS,
    DEFAULT_PROGRESS_INTERVAL,
    DEFAULT_MAX_ATTEMPTS,
    DEFAULT_DELAY,
    DEFAULT_JITTER,
    DEFAULT_PAGE_SIZE,
)
import unittest
from unittest import mock

from ciocore import api_client

from unittest.mock import  patch

from concurrent.futures import ThreadPoolExecutor


class TestBaseDownloaderInit(unittest.TestCase):
    def test_default_values(self):
        # Create an instance of the class
        downloader = BaseDownloader()

        # Assertions
        self.assertIsNone(downloader.output_path)
        self.assertFalse(downloader.force)
        self.assertEqual(downloader.num_threads, DEFAULT_NUM_THREADS)
        self.assertEqual(downloader.max_queue_size, DEFAULT_NUM_THREADS * 2)
        self.assertEqual(
            downloader.progress_interval, DEFAULT_PROGRESS_INTERVAL / 1000.0
        )
        self.assertEqual(downloader.page_size, DEFAULT_PAGE_SIZE)
        self.assertIsInstance(downloader.client, api_client.ApiClient)
        self.assertEqual(downloader.max_attempts, DEFAULT_MAX_ATTEMPTS)
        self.assertEqual(downloader.delay, DEFAULT_DELAY)
        self.assertEqual(downloader.jitter, DEFAULT_JITTER)
        self.assertIsNone(downloader.regex)


    def test_custom_values(self):
        output_path = "/path/to/destination"
        num_threads = 4
        progress_interval = 500
        page_size = 10
        force = True
        regex = r"\d+"
        max_attempts = 3
        delay = 2
        jitter = 0.5

        downloader = BaseDownloader(
            output_path=output_path,
            num_threads=num_threads,
            progress_interval=progress_interval,
            page_size=page_size,
            force=force,
            regex=regex,
            max_attempts=max_attempts,
            delay=delay,
            jitter=jitter,
        )

        # Assertions
        self.assertEqual(downloader.output_path, output_path)
        self.assertTrue(downloader.force)
        self.assertEqual(downloader.num_threads, num_threads)
        self.assertEqual(downloader.max_queue_size, num_threads * 2)
        self.assertAlmostEqual(downloader.progress_interval, progress_interval / 1000.0)
        self.assertEqual(downloader.page_size, page_size)
        self.assertIsInstance(downloader.client, api_client.ApiClient)
        self.assertEqual(downloader.max_attempts, max_attempts)
        self.assertEqual(downloader.delay, delay)
        self.assertEqual(downloader.jitter, jitter)
        self.assertIsNotNone(downloader.regex)


class TestBaseDownloaderRun(unittest.TestCase):
    def setUp(self):
        self.downloader = BaseDownloader()

    def tearDown(self):
        pass

    def test_run_method(self):
        with patch(
            "ciocore.downloader.base_downloader.ThreadPoolExecutor"
        ) as mock_executor:
            my_mock_executor = mock.MagicMock(spec=ThreadPoolExecutor)

            mock_executor.return_value.__enter__.return_value = my_mock_executor

            tasks = [{"id": 1, "name": "task1"}, {"id": 2, "name": "task2"}]
            next_locator = False
            mock_get_some_tasks = mock.MagicMock(return_value=(tasks, next_locator))

            self.downloader.get_some_tasks = mock_get_some_tasks
            self.downloader.download_tasks = mock.MagicMock()
            self.downloader.event_queue = mock.MagicMock()

            self.downloader.run()

            mock_get_some_tasks.assert_called_with(None)
            self.downloader.download_tasks.assert_called_with(tasks, my_mock_executor)
