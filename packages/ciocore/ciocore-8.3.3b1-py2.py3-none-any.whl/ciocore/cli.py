import os
import logging
import click
import webbrowser
import http.server
import socketserver

from ciocore import loggeria, config, api_client, package_query

from ciocore import version as VERSION
 
from ciocore.uploader import Uploader
from ciocore.downloader.legacy_downloader import Downloader
from ciocore.downloader.logging_download_runner import LoggingDownloadRunner
from ciocore.downloader.log import LOGGER_NAME, LEVEL_MAP


LOG_LEVEL_HELP = """The logging level to display"""

LOG_DIR_HELP = """
Write a log file to the given directory. The log rotates, creating a new log file every day, while
storing logs for the last 7 days.
"""
LOG_TO_CONSOLE_HELP = """
If set, logging will be output to the console as well as the logging file."""

THREADS_HELP = """The number of threads that should download simultaneously"""

UPLOADER_DATABASE_FILEPATH_HELP = (
    "Specify a filepath to the local md5 caching database."
)
LOCATION_HELP = """
Specify a location tag to associate with uploads, downloads, and submissions. A location tag allows
you to limit the scope of your uploads and downloads to jobs sharing the same location tag. This is
useful while using the uploader or downloader in daemon mode.
"""
UPLOADER_MD5_CACHING_HELP = """
Use cached md5s. This can dramatically improve the uploading times, as md5 checking can be very
time consuming. Caching md5s allows subsequent uploads (of the same files) to skip the md5
generation process (if the files appear to not have been modified since the last time they were
submitted). The cache is stored locally and uses a file's modification time and file size to
intelligently guess whether the file has changed. Set this flag to False if there is concern that
files may not be getting re-uploaded properly
"""

UPLOADER_PATHS_HELP = """
A list of paths to upload. Use quotes if paths contain spaces or special characters"""

DOWNLOADER_JOB_ID_HELP = """
The job id(s) to download. When specified will only download those jobs and terminate afterwards
"""

DOWNLOADER_OUTPUT_PATH_HELP = """
Override the output directory"""

PACKAGES_FORMAT_OPTIONS = ["text", "markdown", "html"]
PACKAGES_FORMAT_HELP = """
text: The output is a simple list of software names and versions, with nesting to indicate plugin
compatibility. Output is sent to stdout.

markdown: Designed for use in other markdown documentation systems where it benefits from consistent
styling. Output is sent to stdout and can be piped to a file.

html: Opens a browser window and displays the output in a simple html page.
"""

DOCS_PORT_HELP = """
The port to serve the documentation on. Defaults to 8025.
"""

DOWNLOADER_PAGE_SIZE_HELP = """
The number of files to request from the Conductor API at a time. Defaults to 50.
"""

PROGRESS_INTERVAL_HELP = """
The number of milliseconds to pass before printing a emitting a progress message. Defaults to 500.
"""
DEFAULT_PROGRESS_INTERVAL = 500

DOWNLOADER_FORCE_DOWNLOAD_HELP = """
Force download of files even if they already locally. MD5s will not be calculated or checked for this mode. The default is False.
"""

DOWNLOAD_REGEX_HELP = """
A regular expression to filter the files to download. Only files whose names match the regex are downloaded. If a task has multiple files and the regex matches only a subset of them, that subset is considered to be the entire task. This means that by default, tasks are reported to the server as downloaded, even though they weren't all downloaded.
"""

DOWNLOAD_DISABLE_REPORTING_HELP = """
Decide whether to report back to the server with the status of the download. If you use this flag the state of tasks on the server remains unaffected, whether it is downloaded or pernding.
"""

SEQ_FORMAT_HELP = """
The format of the graph to display. The default is text.
"""


DEFAULT_DOCS_PORT = 8025

LOG_FORMATTER = logging.Formatter(
    "%(asctime)s  %(name)s%(levelname)9s  %(threadName)s:  %(message)s"
)

logger = logging.getLogger("conductor.cli")


cfg = config.get()
DEFAULT_CONFIG_MD5_CACHING = cfg["md5_caching"]
DEFAULT_CONFIG_THREAD_COUNT = cfg["thread_count"]
DEFAULT_CONFIG_LOG_LEVEL = cfg["log_level"]
DEFAULT_DOWNLOADER_PAGE_SIZE = cfg["downloader_page_size"]


def _set_logging(log_level, log_to_console=True, log_dir=None, log_filename=None):
    level = loggeria.LEVEL_MAP.get(log_level)
    loggeria.setup_conductor_logging(
        logger_level=level,
        log_dirpath=log_dir,
        log_filename=log_filename,
        console_formatter=loggeria.FORMATTER_VERBOSE,
        disable_console_logging= not log_to_console,
        use_system_log=True,
    )

    print("Logging to %s" % loggeria.LOG_PATH)

def _register(client):
    api_client.ApiClient.register_client(
        client_name=client.CLIENT_NAME, client_version=VERSION
    )

########################### MAIN #################################
@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-v", "--version", is_flag=True, help="Print the version and exit.")
def main(ctx, version):
    """
    Conductor Command-line interface.
    
    To get help on subcommands, use the --help flag after the subcommand.
    
    Example:
    conductor download --help
    
    """
    if not ctx.invoked_subcommand:
        if version:
            click.echo(VERSION)
            ctx.exit()
        click.echo(ctx.get_help())
        ctx.exit()

############################# UPLOAD #############################
@main.command()
@click.option("-db", "--database_filepath", help=UPLOADER_DATABASE_FILEPATH_HELP)
@click.option(
    "-md5",
    "--md5_caching",
    help=UPLOADER_MD5_CACHING_HELP,
    type=bool,
    default=DEFAULT_CONFIG_MD5_CACHING,
)
@click.option(
    "-lv",
    "--log_level",
    help=LOG_LEVEL_HELP,
    type=click.Choice(choices=loggeria.LEVELS, case_sensitive=False),
    show_choices=True,
    default=DEFAULT_CONFIG_LOG_LEVEL,
)
@click.option("-ld", "--log_dir", help=LOG_DIR_HELP)
@click.option("-lcl", "--log_to_console", is_flag=True, help=LOG_TO_CONSOLE_HELP, default=False)
@click.option(
    "-tc",
    "--thread_count",
    type=int,
    help=THREADS_HELP,
    default=DEFAULT_CONFIG_THREAD_COUNT,
)
@click.option("-lc", "--location", help=LOCATION_HELP)
@click.argument("paths", nargs=-1, type=click.Path(exists=True, resolve_path=True))
def upload(
    database_filepath, location, md5_caching, log_level, log_to_console, log_dir, thread_count, paths
):
    """Upload files to Conductor.

    With no arguments, the uploader runs in daemon mode, watching for files to upload for submitted
    jobs.

    Alternatively, specify a list of paths to upload.

    Example:
    conductor upload file1 file2 file3
    """

    _set_logging(log_level, log_to_console=log_to_console,  log_dir=log_dir, log_filename="conductor_uploader.log")

    args_dict = {
        "database_filepath": database_filepath,
        "location": location,
        "md5_caching": md5_caching,
        "thread_count": thread_count,
    }

    up = Uploader(args_dict)

    if paths:
        up.assets_only(*paths)
        return

    up.main()


########################### PACKAGES #############################
@main.command()
@click.option(
    "-f",
    "--fmt",
    "--format",
    default="text",
    help=PACKAGES_FORMAT_HELP,
    type=click.Choice(choices=PACKAGES_FORMAT_OPTIONS, case_sensitive=False),
)
def packages(fmt):
    """List the software packages available on the render nodes in the cloud."""
    package_query.pq(format=fmt)


########################### DOCS #############################
@main.command()
@click.option(
    "-p",
    "--port",
    help=DOCS_PORT_HELP,
    type=int,
    default=DEFAULT_DOCS_PORT,
)
def docs(port):
    """Open the Conductor Core documentation in a web browser."""

    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Server started at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")

        # Change to the directory containing your site
        current_dir = os.path.dirname(os.path.abspath(__file__))
        site_dir = os.path.join(current_dir, "docsite")
        os.chdir(site_dir)

        # Start the server
        localhost_url = f"http://localhost:{port}"
        webbrowser.open(localhost_url)
        httpd.serve_forever()


########################### DEPRECATIONS #############################
############################# UPLOADER #############################
DEPRECATED_PATHS_HELP = "Specify a list of paths to upload."


@main.command(deprecated=True)
@click.option("-db", "--database_filepath", help=UPLOADER_DATABASE_FILEPATH_HELP)
@click.option(
    "-md5",
    "--md5_caching",
    help=UPLOADER_MD5_CACHING_HELP,
    type=bool,
    default=DEFAULT_CONFIG_MD5_CACHING,
)
@click.option(
    "-lv",
    "--log_level",
    help=LOG_LEVEL_HELP,
    type=click.Choice(choices=loggeria.LEVELS, case_sensitive=False),
    show_choices=True,
    default=DEFAULT_CONFIG_LOG_LEVEL,
)
@click.option("-ld", "--log_dir", help=LOG_DIR_HELP)
@click.option(
    "-tc",
    "--thread_count",
    type=int,
    help=THREADS_HELP,
    default=DEFAULT_CONFIG_THREAD_COUNT,
)
@click.option("-lcl", "--log_to_console", is_flag=True, help=LOG_TO_CONSOLE_HELP, default=False)
@click.option("-lc", "--location", help=LOCATION_HELP)
@click.option(
    "-p",
    "--paths",
    help=DEPRECATED_PATHS_HELP,
    multiple=True,
    type=click.Path(exists=True, resolve_path=True),
)
def uploader(
    database_filepath, location, md5_caching, log_level, log_dir, log_to_console, thread_count, paths
):
    """Upload files to Conductor.

    With no arguments, the uploader runs in daemon mode, watching for files to upload for submitted
    jobs.

    Alternatively, specify a list of paths to upload with the --paths option.

    Example:
    conductor upload file1 file2 file3
    """
    _set_logging(log_level, log_to_console=log_to_console,  log_dir=log_dir, log_filename="conductor_uploader.log")

    args_dict = {
        "database_filepath": database_filepath,
        "location": location,
        "md5_caching": md5_caching,
        "thread_count": thread_count,
    }

    up = Uploader(args_dict)

    if paths:
        up.assets_only(*paths)
        return

    up.main()


########################### DOWNLOADER #############################
DEPRECATED_JOBID_HELP = (
    "Download all the files from completed tasks for the given jobs."
)
DEPRECATED_TASKID_HELP = "Download the files from the given tasks in the specified job."


@main.command(deprecated=True)
@click.option("-o", "--output", help=DOWNLOADER_OUTPUT_PATH_HELP)
@click.option("-j", "--job_id", help=DEPRECATED_JOBID_HELP)
@click.option("-t", "--task_id", help=DEPRECATED_TASKID_HELP)
@click.option(
    "-lv",
    "--log_level",
    help=LOG_LEVEL_HELP,
    type=click.Choice(choices=loggeria.LEVELS, case_sensitive=False),
    show_choices=True,
    default=DEFAULT_CONFIG_LOG_LEVEL,
)
@click.option("-ld", "--log_dir", help=LOG_DIR_HELP)
@click.option(
    "-tc",
    "--thread_count",
    type=int,
    help=THREADS_HELP,
    default=DEFAULT_CONFIG_THREAD_COUNT,
)
@click.option("-lc", "--location", help=LOCATION_HELP)
@click.pass_context
def downloader(
    ctx, job_id, task_id, output, location, log_level, log_dir, thread_count
):
    """
    Download renders and other output files from Conductor. You can specify a job id and optional task id to
    download, or you can omit all options and the downloader will run in daemon mode.

    In daemon mode, the downloader polls for new jobs to download. You can specify a location tag to
    limit the scope of the downloader to only download jobs that were submitted with the same
    location tag.

    Examples:
    conductor downloader # daemon mode
    conductor downloader --job_id --task_id 01234
    conductor downloader --task_id --task_id 123
    """
    click.secho("This command has been deprecated. Please use conductor download instead.", fg='red')
    logfile = log_dir and os.path.join(log_dir, "conductor_dl.log")
    _set_logging(log_level, logfile)
    _register(Downloader)

    if not job_id and not task_id:
        Downloader.start_daemon(
            thread_count=thread_count, location=location, output_dir=output
        )
        ctx.exit(0)

    Downloader.download_jobs(
        (job_id,),
        task_id=task_id,
        thread_count=thread_count,
        output_dir=output,
    )


########################### PAGED DOWNLOAD #############################
@main.command()
@click.option("-f", "--force", is_flag=True, help=DOWNLOADER_FORCE_DOWNLOAD_HELP)
@click.option(
    "-ps",
    "--page_size",
    type=int,
    help=DOWNLOADER_PAGE_SIZE_HELP,
    default=DEFAULT_DOWNLOADER_PAGE_SIZE,
)
@click.option(
    "-o", "--output-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help=DOWNLOADER_OUTPUT_PATH_HELP,
)
@click.option(
    "-pi",
    "--progress_interval",
    type=int,
    help=PROGRESS_INTERVAL_HELP,
    default=DEFAULT_PROGRESS_INTERVAL,
)
@click.option(
    "-lv",
    "--log_level",
    help=LOG_LEVEL_HELP,
    type=click.Choice(choices=loggeria.LEVELS, case_sensitive=False),
    show_choices=True,
    default=DEFAULT_CONFIG_LOG_LEVEL,
)
@click.option(
    "-tc",
    "--thread_count",
    type=int,
    help=THREADS_HELP,
    default=DEFAULT_CONFIG_THREAD_COUNT,
)
@click.option(
    "-dr", 
    "--disable-reporting",
    help=DOWNLOAD_DISABLE_REPORTING_HELP,
    is_flag=True,
    default=False,
)
@click.option("-r", "--regex", help=DOWNLOAD_REGEX_HELP)
@click.option("-lc", "--location", help=LOCATION_HELP)
@click.argument("jobids", nargs=-1)
def download(
    jobids,
    page_size,
    output_path,
    location,
    progress_interval,
    log_level,
    thread_count,
    force,
    regex, 
    disable_reporting,
):

    """
    Download renders and other output files from Conductor. You can give a list of job ids to
    download, or you can omit jobids and the downloader will run in daemon mode.

    If you provide jobids, the default behavior is to download all the files from completed tasks
    for those jobs. You can however specify an explicit set of tasks to downloade by providing a
    task range spec after each job id. To do so, append a colon to the job id and then a compact
    task specification. See the examples.

    In daemon mode, the downloader polls for new jobs to download. You can specify a location tag to
    limit the scope of the downloader to only download jobs that were submitted with the same
    location tag.

    Examples:

    conductor download # daemon mode

    conductor download 1234 1235

    conductor download 1234:1-10

    conductor download 1234:1-5x2,10,12-14

    conductor download 1234:1-5 1235:5-10

    """
 
    _register(LoggingDownloadRunner)

    # No longer uses Loggeria. 
    # Instead, it gets the logger with broken-pipe handling from the downloader.log module.
    logging.getLogger(LOGGER_NAME).setLevel(LEVEL_MAP[log_level])

    kwargs = {
        "output_path": output_path,
        "num_threads": thread_count,
        "progress_interval": progress_interval,
        "page_size": page_size,
        "force": force,
        "regex": regex,
        "disable_reporting": disable_reporting,
    }

    dl = LoggingDownloadRunner(
        jobids,
        location,
        **kwargs
    )

    dl.run()

