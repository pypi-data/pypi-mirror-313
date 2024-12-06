from click.testing import CliRunner
from ciocore.cli import upload as cli_upload
from ciocore.cli import download as cli_download
import unittest
import os
from unittest import mock


class CliTestUploaderOptions(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.default_args = {
            "database_filepath": None,
            "location": None,
            "md5_caching": True,
            "thread_count": mock.ANY,
        }
        init_patcher = mock.patch("ciocore.cli.Uploader.__init__", autospec=True)
        self.mock_init = init_patcher.start()
        self.addCleanup(init_patcher.stop)

    def test_receives_full_args_dict_with_defaults_when_no_args_given(self):
        self.runner.invoke(cli_upload, [])
        self.mock_init.assert_called_once_with(mock.ANY, self.default_args)

    def test_database_filepath_arg(self):
        self.runner.invoke(cli_upload, ["--database_filepath", "foo"])
        expected = self.default_args
        expected.update({"database_filepath": "foo"})
        self.mock_init.assert_called_once_with(mock.ANY, expected)

    def test_location_arg(self):
        self.runner.invoke(cli_upload, ["--location", "foo"])
        expected = self.default_args
        expected.update({"location": "foo"})
        self.mock_init.assert_called_once_with(mock.ANY, expected)

    def test_md5_caching_arg(self):
        self.runner.invoke(cli_upload, ["--md5_caching", False])
        expected = self.default_args
        expected.update({"md5_caching": False})
        self.mock_init.assert_called_once_with(mock.ANY, expected)

    def test_thread_count_arg(self):
        self.runner.invoke(cli_upload, ["--thread_count", 4])
        expected = self.default_args
        expected.update({"thread_count": 4})
        self.mock_init.assert_called_once_with(mock.ANY, expected)


class CliTestUploaderArguments(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

        uploader_patcher = mock.patch("ciocore.cli.Uploader", autospec=True)
        self.mock_uploader = uploader_patcher.start()
        self.mock_inst = self.mock_uploader.return_value
        self.addCleanup(uploader_patcher.stop)

    def test_path_only_branch_if_paths(self):
        with self.runner.isolated_filesystem():
            filenames = ["foo.txt", "bar.txt", "baz.txt", "qux.txt"]
            filenames = [os.path.join(os.getcwd(), filename) for filename in filenames]
            for filename in filenames:
                with open(filename, "w") as f:
                    f.write("hello world")
            self.runner.invoke(cli_upload, filenames)
            self.mock_inst.assets_only.assert_called_once_with(
                mock.ANY, mock.ANY, mock.ANY, mock.ANY
            )
            self.mock_inst.main.assert_not_called()

    def test_main_branch_if_no_paths(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli_upload)
            self.mock_inst.main.assert_called_once()
            self.mock_inst.assets_only.assert_not_called()


class CliTestDownloader(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

        dl_patcher_runner = mock.patch(
            "ciocore.cli.LoggingDownloadRunner.__init__", autospec=True
        )
        self.mock_runner = dl_patcher_runner.start()
        self.addCleanup(dl_patcher_runner.stop)

        start_daemon_patcher = mock.patch(
            "ciocore.cli.Downloader.start_daemon", autospec=True
        )
        self.mock_start_daemon = start_daemon_patcher.start()
        self.addCleanup(start_daemon_patcher.stop)

 
    def test_jobid_branch_if_job_id(self):
        jid = "00000"
        # self.assertTrue(True)
        self.runner.invoke(cli_download, [jid])
        self.mock_runner.assert_called_once( )
        self.mock_start_daemon.assert_not_called()

    # def test_job_id_only(self):
    #     jid = "00000"
    #     self.runner.invoke(cli_download, [jid])
    #     self.mock_dljobs.assert_called_once_with(
    #         (jid,), thread_count=mock.ANY, output_dir=mock.ANY
        # )

    # def test_several_job_ids(self):
    #     jid1 = "00000"
    #     jid2 = "11111"
    #     self.runner.invoke(cli_download, [jid1, jid2])
    #     self.mock_dljobs.assert_called_once_with(
    #         (jid1,jid2),  thread_count=mock.ANY, output_dir=mock.ANY
    #     )

    # def test_job_ids_and_others(self):
    #     jid1 = "00000"
    #     jid2 = "11111"
    #     tc = 4
    #     od = "foo"
    #     self.runner.invoke(
    #         cli_download,
    #         ["--thread_count", tc, "--destination", od, jid1, jid2 ],
    #     )
    #     self.mock_dljobs.assert_called_once_with(
    #         (jid1,jid2), thread_count=tc, output_dir=od
    #     )

    # def test_daemon_branch_if_no_job_id(self):
    #     self.runner.invoke(cli_download, [])
    #     self.mock_start_daemon.assert_called_once()
    #     self.mock_dljobs.assert_not_called()

    # def test_daemon_branch_args_present(self):
    #     tc = 4
    #     od = "foo"
    #     self.runner.invoke(cli_download)
    #     self.mock_start_daemon.assert_called_once_with(thread_count=mock.ANY, location=mock.ANY, output_dir=mock.ANY)
 
    # def test_daemon_branch_args(self):
    #     tc = 4
    #     od = "/foo"
    #     loc = "bar"
    #     self.runner.invoke(cli_download, ["--thread_count", tc, "--location", loc])
    #     self.mock_start_daemon.assert_called_once_with(thread_count=tc, location="bar", output_dir=None)
 
