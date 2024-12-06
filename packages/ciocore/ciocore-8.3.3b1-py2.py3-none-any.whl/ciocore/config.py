"""
Config is a configuration object implemented as a module-level singleton.

Configuration variables can be shared by importing the module. If there are changes in environment variables or other sources, the config can be refreshed.
"""

import logging
import os
# import multiprocessing
import base64
import json
import re
import platform

from ciocore.common import CONDUCTOR_LOGGER_NAME

logger = logging.getLogger(CONDUCTOR_LOGGER_NAME)

# https://stackoverflow.com/a/3809435/179412


USER_DIRS = {
    "Linux": os.path.expanduser(os.path.join("~", ".conductor")),
    "Darwin": os.path.expanduser(os.path.join("~",".conductor")),
    "Windows": os.path.expanduser(os.path.join("~", "AppData", "Local", "Conductor")),
}

DEFAULT_USER_DIR = USER_DIRS.get(platform.system(), USER_DIRS["Linux"])

URL_REGEX = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)

__config__ = None


def config(force=False):
    """
    Instantiate a config object if necessary.

    Deprecated:
        Use [get()](#get) instead.

    Args:
        force (bool): Discards any existing config object and instantiate a new one -- Defaults to `False`.

    Returns:
        dict: A dictionary containing configuration values.
    """

    global __config__
    if force or not __config__:
        __config__ = Config()
    return __config__


def get(force=False):
    """
    Instantiate a config object if necessary and return the dictionary.

    Args:
        force (bool): Discards any existing config object and instantiate a new one -- Defaults to `False`.

    Returns:
        dict: A dictionary containing configuration values.

    Example:
        >>> from ciocore import config
        >>> config.get()
        {
          'thread_count': 16,
          'priority': 5,
          'md5_caching': True,
          'log_level': 'INFO',
          'url': 'https://dashboard.conductortech.com',
          'auth_url': 'https://dashboard.conductortech.com',
          'api_url': 'https://api.conductortech.com',
          'api_key': None,
          'downloader_page_size': 50,
        }
    """
    global __config__
    if force or not __config__:
        __config__ = Config()
    return __config__.config


class Config(object):
    def __init__(self):
        """
        Initialize the config object.

        A config object is a dictionary containing configuration values. It is a singleton, so there is only one instance of it. It is instantiated the first time it is needed. It can be refreshed by calling get() with the `force` keyword argument set to `True`.

        A Config object has the following properties:

        * `thread_count` The number of threads to use for downloading files. Defaults to the number of CPUs on the system times 2. It can be overridden by the `CONDUCTOR_THREAD_COUNT` environment variable.
        * `priority` Set the priority for submissions. Defaults to 5. It can be overridden by the `CONDUCTOR_PRIORITY` environment variable.
        * `md5_caching` Whether to cache MD5s. Defaults to `True`. It can be overridden by the `CONDUCTOR_MD5_CACHING` environment variable. Cachine MD5s significantly improves submission performance, but on rare occasions it can cause submissions to fail. If you experience this, set `md5_caching` to `False`.
        * `log_level` The logging level. Defaults to `INFO`. It can be overridden by the `CONDUCTOR_LOG_LEVEL` environment variable.
        * `url` The URL of the Conductor dashboard. Defaults to `https://dashboard.conductortech.com`. It can be overridden by the `CONDUCTOR_URL` environment variable.
        * `auth_url` The URL of the Conductor dashboard. Defaults to `https://dashboard.conductortech.com`. It can be overridden by the `CONDUCTOR_AUTH_URL` environment variable. This is deprecated. Use `url` instead.
        * `api_url` The URL of the Conductor API. Defaults to `https://api.conductortech.com`. It can be overridden by the `CONDUCTOR_API_URL` environment variable.
        * `api_key` The API key. The API key can be acquired from the Conductor dashboard, and can be stored in an environment variable or a file. In both cases the API KEY can be a JSON object or a base64 encoded JSON object. If it is base64 encoded, it can be a string or bytes. If it is a string, it will be decoded as ASCII. If it is bytes, it will be decoded as UTF-8.
            * Environment variable: The `CONDUCTOR_API_KEY` variable can hold the API KEY directly.
            * File: The `CONDUCTOR_API_KEY_PATH` variable can hold the path to a file containing the API KEY.
        * `downloader_page_size` The number of files to request from the Conductor API at a time. Defaults to 50. It can be overridden by the `CONDUCTOR_DOWNLOADER_PAGE_SIZE` environment variable.

        Returns:
            Config: A config object.

        Raises:
            ValueError -- Invalid inputs, such as badly formed URLs.
        """
        default_downloader_page_size = 50

     

        try:
            default_thread_count = min( os.cpu_count() - 1, 15)
        except NotImplementedError:
            default_thread_count = 15

        url = os.environ.get("CONDUCTOR_URL", "https://dashboard.conductortech.com")

        if not URL_REGEX.match(url):
            raise ValueError("CONDUCTOR_URL is not valid '{}'".format(url))

        api_url = os.environ.get("CONDUCTOR_API_URL", url.replace("dashboard", "api"))
        if not URL_REGEX.match(api_url):
            raise ValueError("CONDUCTOR_API_URL is not valid '{}'".format(api_url))

        falsy = ["false", "no", "off", "0"]

        log_level = os.environ.get("CONDUCTOR_LOG_LEVEL", "INFO")
        if log_level not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
            log_level = "INFO"

        self.config = {
            "thread_count": int(
                os.environ.get("CONDUCTOR_THREAD_COUNT", default_thread_count)
            ),
            "downloader_page_size": int(
                os.environ.get(
                    "CONDUCTOR_DOWNLOADER_PAGE_SIZE", default_downloader_page_size
                )
            ),
            "priority": int(os.environ.get("CONDUCTOR_PRIORITY", 5)),
            "md5_caching": False
            if os.environ.get("CONDUCTOR_MD5_CACHING", "True").lower() in falsy
            else True,
            "log_level": log_level,
            "url": url,
            # Keep "auth_url" for backwwards compatibillity only.
            # Clients should use "url" moving forward.
            # Remove "auth_url" on the next major version bump.
            "auth_url": url,
            "api_url": api_url,
            "api_key": self.get_api_key_from_variable() or self.get_api_key_from_file(),
            "user_dir": os.environ.get('CONDUCTOR_USER_DIR', DEFAULT_USER_DIR)
        }

    @staticmethod
    def get_api_key_from_variable():
        """
        Attempt to get an API key from the `CONDUCTOR_API_KEY` environment variable.

        Raises:
            ValueError: An error occurred while reading or loading the key into JSON.

        Returns:
            str: JSON object containing the key - base 64 decoded if necessary.

        """
        api_key = os.environ.get("CONDUCTOR_API_KEY")
        if not api_key:
            return
        logger.info("Attempting to read API key from CONDUCTOR_API_KEY")
        try:
            return json.loads(api_key.replace("\n", "").replace("\r", ""))
        except ValueError:
            try:
                result = base64.b64decode(api_key)
                return Config._to_json(result)
            except BaseException:
                result = base64.b64decode(api_key.encode()).decode("ascii")
                return Config._to_json(result)
        except BaseException:
            message = "An error occurred reading the API key from the CONDUCTOR_API_KEY variable"
            logger.error(message)
            raise ValueError(message)

    @staticmethod
    def get_api_key_from_file():
        """
        Attempt to get an API key from the file in the CONDUCTOR_API_KEY_PATH environment variable.

        Raises:
            ValueError: An error occurred while reading or loading the key into JSON.

        Returns:
            str: JSON object containing the key - base 64 decoded if necessary.

        """
        api_key_path = os.environ.get("CONDUCTOR_API_KEY_PATH")
        if not api_key_path:
            return
        logger.info("Attempting to read API key from CONDUCTOR_API_KEY_PATH")
        try:
            with open(api_key_path, "r") as fp:
                return Config._to_json(fp.read())
        except BaseException:
            message = "An error occurred reading the API key from the path described in the CONDUCTOR_API_KEY_PATH variable"
            logger.error(message)
            raise ValueError(message)

    @staticmethod
    def _to_json(content):
        return json.loads(content.replace("\n", "").replace("\r", ""))
