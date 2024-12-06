"""
The api_client module is used to make requests to the Conductor API.
"""

import base64
import collections
import datetime
import hashlib
import importlib
import json
import jwt
import logging
import os
import platform
import requests
import socket
import time
import sys
import platform

from urllib import parse

import ciocore

from ciocore import config
from ciocore import common, auth

logger = logging.getLogger(__name__)

# A convenience tuple of network exceptions that can/should likely be retried by the retry decorator
try:
    CONNECTION_EXCEPTIONS = (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
    )
except AttributeError:
    CONNECTION_EXCEPTIONS = (
        requests.HTTPError,
        requests.ConnectionError,
        requests.Timeout,
    )


def truncate_middle(s, max_length):
    """
    Truncate the string `s` to `max_length` by removing characters from the middle.

    :param s: The original string to be truncated.
    :type s: str
    :param max_length: The maximum allowed length of the string after truncation.
    :type max_length: int
    :return: The truncated string.
    :rtype: str
    """

    if len(s) <= max_length:
        # String is already at or below the maximum length, return it as is
        return s

    # Calculate the number of characters to keep from the start and end of the string
    num_keep_front = (max_length // 2)
    num_keep_end = max_length - num_keep_front - 1  # -1 for the ellipsis
    
    # Construct the truncated string
    return s[:num_keep_front] + '~' + s[-num_keep_end:]


# TODO: appspot_dot_com_cert = os.path.join(common.base_dir(),'auth','appspot_dot_com_cert2') load
# appspot.com cert into requests lib verify = appspot_dot_com_cert

class ApiClient:
    """
    The ApiClient class is a wrapper around the requests library that handles authentication and retries.
    """

    http_verbs = ["PUT", "POST", "GET", "DELETE", "HEAD", "PATCH"]

    USER_AGENT_TEMPLATE = "client {client_name}/{client_version} (ciocore {ciocore_version}; {runtime} {runtime_version}; {platform} {platform_details}; {hostname} {pid}; {python_path})"
    USER_AGENT_MAX_PATH_LENGTH = 1024

    user_agent_header = None

    def __init__(self):
        logger.debug("")

    def _make_request(self, verb, conductor_url, headers, params, data, raise_on_error=True):
        response = requests.request(
            method=verb, url=conductor_url, headers=headers, params=params, data=data
        )

        logger.debug(f"verb: {verb}")
        logger.debug(f"conductor_url: {conductor_url}")
        logger.debug(f"headers: {headers}")
        logger.debug(f"params: {params}")
        logger.debug(f"data: {data}")

        # If we get 300s/400s debug out the response. TODO(lws): REMOVE THIS
        if 300 <= response.status_code < 500:
            logger.debug("*****  ERROR!!  *****")
            logger.debug(f"Reason: {response.reason}")
            logger.debug(f"Text: {response.text}")

        # trigger an exception to be raised for 4XX or 5XX http responses
        if raise_on_error:
            response.raise_for_status()

        return response

    def make_prepared_request(
        self,
        verb,
        url,
        headers=None,
        params=None,
        json_payload=None,
        data=None,
        stream=False,
        remove_headers_list=None,
        raise_on_error=True,
        tries=5,
    ):
        """
        Make a request to the Conductor API.

        Deprecated:
            Primarily used to removed enforced headers by requests.Request. Requests 2.x will add
            Transfer-Encoding: chunked with file like object that is 0 bytes, causing s3 failures (501)
            - https://github.com/psf/requests/issues/4215#issuecomment-319521235

            To get around this bug make_prepared_request has functionality to remove the enforced header
            that would occur when using requests.request(...). Requests 3.x resolves this issue, when
            client is built to use Requests 3.x this function can be removed.

        Returns:
            requests.Response: The response object.

        Args:
            verb (str): The HTTP verb to use.
            url (str): The URL to make the request to.
            headers (dict): A dictionary of headers to send with the request.
            params (dict): A dictionary of query parameters to send with the request.
            json (dict): A JSON payload to send with the request.
            stream (bool): Whether or not to stream the response.
            remove_headers_list (list): A list of headers to remove from the request.
            raise_on_error (bool): Whether or not to raise an exception if the request fails.
            tries (int): The number of times to retry the request.
        """

        req = requests.Request(
            method=verb,
            url=url,
            headers=headers,
            params=params,
            json=json_payload,
            data=data,
        )
        prepped = req.prepare()

        if remove_headers_list:
            for header in remove_headers_list:
                prepped.headers.pop(header, None)

        # Create a retry wrapper function
        retry_wrapper = common.DecRetry(
            retry_exceptions=CONNECTION_EXCEPTIONS, tries=tries
        )

        # requests sessions potentially not thread-safe, but need to removed enforced
        # headers by using a prepared request.create which can only be done through an
        # request.Session object. Create Session object per call of make_prepared_request, it will
        # not benefit from connection pooling reuse. https://github.com/psf/requests/issues/1871
        session = requests.Session()

        # wrap the request function with the retry wrapper
        wrapped_func = retry_wrapper(session.send)

        # call the wrapped request function
        response = wrapped_func(prepped, stream=stream)

        logger.debug("verb: %s", prepped.method)
        logger.debug("url: %s", prepped.url)
        logger.debug("headers: %s", prepped.headers)
        logger.debug("params: %s", req.params)
        logger.debug("response: %s", response)

        # trigger an exception to be raised for 4XX or 5XX http responses
        if raise_on_error:
            response.raise_for_status()

        return response

    def make_request(
        self,
        uri_path="/",
        headers=None,
        params=None,
        data=None,
        verb=None,
        conductor_url=None,
        raise_on_error=True,
        tries=5,
        use_api_key=False,
    ):
        """
        Make a request to the Conductor API.

        Args:
            uri_path (str): The path to the resource to request.
            headers (dict): A dictionary of headers to send with the request.
            params (dict): A dictionary of query parameters to send with the request.
            data (dict): A dictionary of data to send with the request.
            verb (str): The HTTP verb to use.
            conductor_url (str): The Conductor URL.
            raise_on_error (bool): Whether or not to raise an exception if the request fails.
            tries (int): The number of times to retry the request.
            use`_api_key (bool): Whether or not to use the API key for authentication.

        Returns:
            tuple(str, int): The response text and status code.
        """
        cfg = config.get()
        # TODO: set Content Content-Type to json if data arg
        if not headers:
            headers = {"Content-Type": "application/json", "Accept": "application/json"}

        logger.debug("read_conductor_credentials({})".format(use_api_key))
        bearer_token = read_conductor_credentials(use_api_key)
        if not bearer_token:
            raise Exception("Error: Could not get conductor credentials!")

        headers["Authorization"] = "Bearer %s" % bearer_token

        if not ApiClient.user_agent_header:
            self.register_client("ciocore")

        headers["User-Agent"] = ApiClient.user_agent_header

        # Construct URL
        if not conductor_url:
            conductor_url = parse.urljoin(cfg["url"], uri_path)

        if not verb:
            if data:
                verb = "POST"
            else:
                verb = "GET"

        assert verb in self.http_verbs, "Invalid http verb: %s" % verb

        # Create a retry wrapper function
        retry_wrapper = common.DecRetry(
            retry_exceptions=CONNECTION_EXCEPTIONS, tries=tries
        )

        # wrap the request function with the retry wrapper
        wrapped_func = retry_wrapper(self._make_request)

        # call the wrapped request function
        response = wrapped_func(
            verb, conductor_url, headers, params, data, raise_on_error=raise_on_error
        )

        return response.text, response.status_code

    @classmethod
    def register_client(cls, client_name, client_version=None):
        """
        Generates the http User Agent header that includes helpful debug info.
        """

        # Use the provided client_version.
        if not client_version:
            client_version = 'unknown'

        python_version = platform.python_version()
        system_info = platform.system()
        release_info = platform.release()
        

        # Get the MD5 hex digest of the path to the python executable
        python_executable_path = truncate_middle(sys.executable.encode('utf-8'), cls.USER_AGENT_MAX_PATH_LENGTH)
        md5_hash = hashlib.md5(python_executable_path).hexdigest()

        user_agent = (
            f"{client_name}/{client_version} "
            f"(python {python_version}; {system_info} {release_info}; {md5_hash})"
        )
        cls.user_agent_header = user_agent
        
        return user_agent
    

def read_conductor_credentials(use_api_key=False):
    """
    Read the conductor credentials file.
    
    If the credentials file exists, it will contain a bearer token from either
    the user or the API key.
    
    If the credentials file doesn't exist, or is
    expired, or is from a different domain, we try to fetch a new one in the API key scenario or
    prompt the user to log in. 
    
    Args: 
        use_api_key (bool): Whether or not to try to use the API key

    Returns: 
        A Bearer token in the event of a success or None

    """

    cfg = config.get()

    logger.debug("Reading conductor credentials...")
    if use_api_key:
        if not cfg.get("api_key"):
            use_api_key = False
        if use_api_key and not cfg["api_key"].get("client_id"):
            use_api_key = False
    logger.debug("use_api_key = %s" % use_api_key)
    creds_file = get_creds_path(use_api_key)

    logger.debug("Creds file is %s" % creds_file)
    logger.debug("Auth url is %s" % cfg["url"])
    if not os.path.exists(creds_file):
        if use_api_key:
            if not cfg["api_key"]:
                logger.debug("Attempted to use API key, but no api key in in config!")
                return None

            #  Exchange the API key for a bearer token
            logger.debug("Attempting to get API key bearer token")
            get_api_key_bearer_token(creds_file)

        else:
            auth.run(creds_file, cfg["url"])
    if not os.path.exists(creds_file):
        return None

    logger.debug("Reading credentials file...")
    with open(creds_file, "r", encoding="utf-8") as fp:
        file_contents = json.loads(fp.read())
    expiration = file_contents.get("expiration")
    same_domain = creds_same_domain(file_contents)
    if same_domain and expiration and expiration >= int(time.time()):
        return file_contents["access_token"]
    logger.debug("Credentials have expired or are from a different domain")
    if use_api_key:
        logger.debug("Refreshing API key bearer token!")
        get_api_key_bearer_token(creds_file)
    else:
        logger.debug("Sending to auth page...")
        auth.run(creds_file, cfg["url"])
    #  Re-read the creds file, since it has been re-upped
    with open(creds_file, "r", encoding="utf-8") as fp:
        file_contents = json.loads(fp.read())
        return file_contents["access_token"]


def get_api_key_bearer_token(creds_file=None):
    """
    Get a bearer token from the API key.
    
    Args:
        creds_file (str): The path to the credentials file. If not provided, the bearer token will not be written to disk.
        
    Returns:
        A dictionary containing the bearer token and other information.
    """
    cfg = config.get()
    url = "{}/api/oauth_jwt".format(cfg["url"])
    response = requests.get(
        url,
        params={
            "grant_type": "client_credentials",
            "scope": "owner admin user",
            "client_id": cfg["api_key"]["client_id"],
            "client_secret": cfg["api_key"]["private_key"],
        },
    )
    if response.status_code == 200:
        response_dict = json.loads(response.text)
        credentials_dict = {
            "access_token": response_dict["access_token"],
            "token_type": "Bearer",
            "expiration": int(time.time()) + int(response_dict["expires_in"]),
            "scope": "user admin owner",
        }

        if not creds_file:
            return credentials_dict

        if not os.path.exists(os.path.dirname(creds_file)):
            os.makedirs(os.path.dirname(creds_file))

        with open(creds_file, "w") as fp:
            fp.write(json.dumps(credentials_dict))
    return


def get_creds_path(api_key=False):
    """
    Get the path to the credentials file.
    
    Args:
        api_key (bool): Whether or not to use the API key.
        
    Returns:
        str: The path to the credentials file.
    """
    creds_dir = os.path.join(os.path.expanduser("~"), ".config", "conductor")
    if api_key:
        creds_file = os.path.join(creds_dir, "api_key_credentials")
    else:
        creds_file = os.path.join(creds_dir, "credentials")
    return creds_file


def get_bearer_token(refresh=False):
    """
    Return the bearer token.

    Args:
        refresh (bool): Whether or not to refresh the token.
        
    TODO: Thread safe multiproc caching, like it used to be pre-python3.7.
    """
    return read_conductor_credentials(True)


def creds_same_domain(creds):
    """
    Check if the creds are for the same domain as the config.
    
    Args:
        creds (dict): The credentials dictionary.
        
    Returns:
        bool: Whether or not the creds are for the same domain as the config.
    """
    cfg = config.get()
    """Ensure the creds file refers to the domain in config"""
    token = creds.get("access_token")
    if not token:
        return False

    decoded = jwt.decode(creds["access_token"], verify=False)
    audience_domain = decoded.get("aud")
    return (
        audience_domain
        and audience_domain.rpartition("/")[-1] == cfg["api_url"].rpartition("/")[-1]
    )


def account_id_from_jwt(token):
    """
    Fetch the accounts id from a jwt token value.
    
    Args:
        token (str): The jwt token.
    
    Returns:
        str: The account id.
    """
    payload = jwt.decode(token, verify=False)
    return payload.get("account")


def account_name_from_jwt(token):
    """
    Fetch the accounts name from a jwt token value.
    
    Args:
        token (str): The jwt token.
        
    Returns:
        str: The account name.
    """
    account_id = account_id_from_jwt(token)
    cfg = config.get()
    if account_id:
        url = "%s/api/v1/accounts/%s" % (cfg["api_url"], account_id)
        response = requests.get(url, headers={"authorization": "Bearer %s" % token})
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            return response_dict["data"]["name"]
    return None


def request_instance_types(as_dict=False, filter_param=""):
    """
    Get the list of available instances types.
    
    Args:
        as_dict (bool): Whether or not to return the instance types as a dictionary.
        filter_param (string): complex RHS string query ex:
          "cpu=gte:8:int,operating_system=ne:windows,gpu.gpu_count=eq:1:int"
    
    Returns:
        list: The list of instance types.
    """
    api = ApiClient()
    response, response_code = api.make_request(
        "api/v1/instance-types", use_api_key=True, raise_on_error=False,
        params={"filter":filter_param}
    )
    if response_code not in (200,):
        msg = "Failed to get instance types"
        msg += "\nError %s ...\n%s" % (response_code, response)
        raise Exception(msg)

    instance_types = json.loads(response).get("data", [])
    logger.debug("Found available instance types: %s", instance_types)

    if as_dict:
        return dict(
            [(instance["description"], instance) for instance in instance_types]
        )
    return instance_types


def request_projects(statuses=("active",)):
    """
    Query Conductor for all client Projects that are in the given status(es).
    
    Args:
        statuses (tuple): The statuses to filter for.
    
    Returns:
        list: The list of project names.
    """
    api = ApiClient()

    logger.debug("statuses: %s", statuses)

    uri = "api/v1/projects/"

    response, response_code = api.make_request(
        uri_path=uri, verb="GET", raise_on_error=False, use_api_key=True
    )
    logger.debug("response: %s", response)
    logger.debug("response: %s", response_code)
    if response_code not in [200]:
        msg = "Failed to get available projects from Conductor"
        msg += "\nError %s ...\n%s" % (response_code, response)
        raise Exception(msg)
    projects = []

    # Filter for only projects of the proper status
    for project in json.loads(response).get("data") or []:
        if not statuses or project.get("status") in statuses:
            projects.append(project["name"])
    return projects


def request_software_packages():
    """
    Query Conductor for all software packages for the currently available sidecar.

    Returns:
        list: The list of software packages.
    """
    api = ApiClient()

    uri = "api/v1/ee/packages?all=true,"
    response, response_code = api.make_request(
        uri_path=uri, verb="GET", raise_on_error=False, use_api_key=True
    )

    if response_code not in [200]:
        msg = "Failed to get software packages for latest sidecar"
        msg += "\nError %s ...\n%s" % (response_code, response)
        raise Exception(msg)
    
    software = json.loads(response).get("data", [])
    software = [sw for sw in software if not ("3dsmax" in sw["product"] and sw["platform"] == "linux")]
    return software

def request_extra_environment():
    """
    Query Conductor for extra environment.
    """
    api = ApiClient()

    uri = "api/v1/integrations/env-vars-configs"
    response, response_code = api.make_request(
        uri_path=uri, verb="GET", raise_on_error=False, use_api_key=True
    )

    if response_code not in [200]:
        msg = "Failed to get extra environment"
        msg += "\nError %s ...\n%s" % (response_code, response)
        raise Exception(msg)

    all_accounts = json.loads(response).get("data", [])

    token = read_conductor_credentials(True)
    if not token:
        raise Exception("Error: Could not get conductor credentials!")
    account_id =  str(account_id_from_jwt(token))

    if not account_id:
        raise Exception("Error: Could not get account id from jwt!")
    account_env = next((account for account in all_accounts if account["account_id"] == account_id), None)
    if not account_env:
        raise Exception("Error: Could not get account environment!")
    return account_env.get("env", [])




def get_jobs(first_jid, last_jid=None):
    """
    Query Conductor for all jobs between the given job ids.

    Returns:
        list: The list of jobs.

    Raises:
        Exception: If the request fails.

    Examples:
        >>> from ciocore import api_client
        >>> jobs = api_client.get_jobs(1959)
        >>> len(jobs)
        1
        >>> jobs[0]["jid"]
        '01959'
        >>> jobs = api_client.get_jobs(1959, 1961)
        >>> len(jobs)
        3
    """
    if last_jid is None:
        last_jid = first_jid
    low = str(int(first_jid) - 1).zfill(5)
    high = str(int(last_jid) + 1).zfill(5)
    api = ApiClient()
    uri = "api/v1/jobs"

    response, response_code = api.make_request(
        uri_path=uri,
        verb="GET",
        raise_on_error=False,
        use_api_key=True,
        params={"filter": f"jid_gt_{low},jid_lt_{high}"},
    )

    if response_code not in [200]:
        msg = f"Failed to get jobs {first_jid}-{last_jid}"
        msg += "\nError %s ...\n%s" % (response_code, response)
        raise Exception(msg)
    jobs = json.loads(response).get("data")
    return jobs


def get_log(job_id, task_id):
    """
    Get the log for the given job and task.

    Args:
        job_id (str): The job id.
        task_id (str): The task id.

    Returns:
        list: A list of logs.

    Raises:
        Exception: If the request fails.

    Examples:
        >>> from ciocore import api_client
        >>> logs = api_client.get_log(1959, 0)
        {
            "logs": [
                {
                    "container_id": "j-5669544198668288-5619559933149184-5095331660038144-stde",
                    "instance_name": "renderer-5669544198668288-170062309438-62994",
                    "log": [
                        "Blender 2.93.0 (hash 84da05a8b806 built 2021-06-02 11:29:24)",
                        ...
                        ...
                        "Saved: '/var/folders/8r/46lmjdmj50x_0swd9klwptzm0000gq/T/blender_bmw/renders/render_0001.png'",
                        " Time: 00:29.22 (Saving: 00:00.32)",
                        "",
                        "",
                        "Blender quit"
                ],
                "timestamp": "1.700623521101516E9"
                }
            ],
            "new_num_lines": [
                144
            ],
            "status_description": "",
            "task_status": "success"
        }
    """
    job_id = str(job_id).zfill(5)
    task_id = str(task_id).zfill(3)

    api = ApiClient()
    uri = f"get_log_file?job={job_id}&task={task_id}&num_lines[]=0"

    response, response_code = api.make_request(
        uri_path=uri, verb="GET", raise_on_error=False, use_api_key=True
    )

    if response_code not in [200]:
        msg = f"Failed to get log for job {job_id} task {task_id}"
        msg += "\nError %s ...\n%s" % (response_code, response)
        raise Exception(msg)

    return response


def kill_jobs(*job_ids):
    """
    Kill the given jobs.
    
    Args:
        job_ids (list): The list of job ids.
    
    Returns:
        dict: The response.
    
    Examples:
        >>> from ciocore import api_client
        >>> api_client.kill_jobs("03095","03094")
        {'body': 'success', 'message': "Jobs [u'03095', u'03094'] have been kill."}

    """
    job_ids = [str(job_id).zfill(5) for job_id in job_ids]
    api = ApiClient()
    payload = {
        "action": "kill",
        "jobids": job_ids,
    }
    response, response_code = api.make_request(
        uri_path="jobs_multi", 
        verb="PUT", 
        raise_on_error=False, 
        use_api_key=True, 
        data=json.dumps(payload)
    )
    
    if response_code not in [200]:
        msg = f"Failed to kill jobs {job_ids}"
        msg += "\nError %s ...\n%s" % (response_code, response)
        raise Exception(msg)
    
    return json.loads(response)


def kill_tasks(job_id, *task_ids):
    """
    Kill the given tasks.
    
    Args:
        job_id (str): The job id.
        task_ids (list): The list of task ids.
        
    Returns:
        dict: The response.
        
    Examples:
        >>> from ciocore import api_client
        >>> api_client.kill_tasks("03096", *range(50,56))
        {'body': 'success', 'message': ' 6 Tasks set to "kill"\n\t050\n\t051\n\t052\n\t053\n\t054\n\t055'}
    """
    
    job_id = str(job_id).zfill(5)
    task_ids = [str(task_id).zfill(3) for task_id in task_ids]
    api = ApiClient()
    payload = {
        "action": "kill",
        "jobid": job_id,
        "taskids": task_ids,
    }
    response, response_code = api.make_request(
        uri_path="tasks_multi", 
        verb="PUT", 
        raise_on_error=False, 
        use_api_key=True, 
        data=json.dumps(payload)
    )
    
    if response_code not in [200]:
        msg = f"Failed to kill tasks {task_ids} of job {job_id}"
        msg += "\nError %s ...\n%s" % (response_code, response)
        raise Exception(msg)
    
    return json.loads(response)

def _get_compute_usage(start_time, end_time):
    """
    Query the account usage to get the raw compute data. Private method.
    
    Compute includes licenses, instances and Conductor cost. Everything involved
    with running a job.
    
    Please use the public method api_client.get_compute_usage() instead.
    
    Args:
        start_time (datetime.datetime): The first day to include in the report. Only the date is considered and it's assumed to be in UTC.
        end_time (datetime.datetime): The last day to include in the report. Only the date is considered and it's assumed to be in UTC.
        
    Returns:
        list: A list of billing entries
        
    Examples:
        >>> from ciocore import api_client
        >>> api_client._get_compute_usage(start_time, end_time)
            [
                {
                    "cores": 0.5, 
                    "instance_cost": 0.019999999552965164, 
                    "license_cost": 0.019999999552965164, 
                    "minutes": 6.9700000286102295, 
                    "self_link": 0, 
                    "start_time": "Tue, 09 Jan 2024 18:00:00 GMT"
                }, 
                {
                    "cores": 0.4, 
                    "instance_cost": 0.019999999552965164, 
                    "license_cost": 0.019999999552965164, 
                    "minutes": 6.960000038146973, 
                    "self_link": 1, 
                    "start_time": "Tue, 09 Jan 2024 19:00:00 GMT"
                }] 
    """

    api = ApiClient()

    payload = {
        "filter": json.dumps(
            [{"field": "start_time", "op": ">=", "value": start_time.date().isoformat()},
             {"field": "start_time", "op": "<", "value": end_time.date().isoformat()}]),
        "group_by": json.dumps(["start_time"]),
        "order_by": "start_time"
    }

    response, response_code = api.make_request(
        uri_path="billing/get_usage", 
        verb="GET",
        raise_on_error=False,
        use_api_key=True,
        params=payload
    )

    if response_code not in [200]:
        msg = f"Failed to query compute usage"
        msg += "\nError %s ...\n%s" % (response_code, response)
        raise Exception(msg)

    return json.loads(response)['data']

def _get_storage_usage(start_time, end_time):
    """
    Query the account usage to get the raw storage data. Private method.
    
    Please use the public method api_client.get_storage_usage() instead.
    
    Args:
        start_time (datetime.datetime): The first day to include in the report. Only the date is considered and it's assumed to be in UTC.
        end_time (datetime.datetime): The last day to include in the report. Only the date is considered and it's assumed to be in UTC.
        
    Returns:
        dict: A dict of billing details related to storage
        
    Examples:
        >>> from ciocore import api_client
        >>> api_client._get_storage_usage(start_time, end_time)
           {
                "cost": "28.96", 
                "cost_per_day": [
                    4.022,
                    4.502, 
                    4.502, 
                    5.102, 
                    5.102, 
                    5.732
                ], 
                "currency": "USD", 
                "daily_price": "0.006", 
                "end_date": "2024-01-07", 
                "gibs_per_day": [
                    679.714,
                    750.34, 
                    750.34, 
                    850.36, 
                    850.35, 
                    955.32
                ], 
                "gibs_used": "806.07", 
                "monthly_price": "0.18", 
                "start_date": "2024-01-01", 
                "storage_unit": "GiB"
                }
            ]
            } 
    """

    api = ApiClient()
    
    # Add one day to the end time as the query is exclusive of the last day but
    # we want consistency with _get_compute_usage()    
    payload = {
        "start": start_time.date().isoformat(),
        "end": (end_time.date() + datetime.timedelta(days=1)).isoformat()
    }

    response, response_code = api.make_request(
        uri_path="billing/get_storage_usage", 
        verb="GET",
        raise_on_error=False,
        use_api_key=True,
        params=payload
    )

    if response_code not in [200]:
        msg = f"Failed to query storage usage"
        msg += "\nError %s ...\n%s" % (response_code, response)
        raise Exception(msg)

    return json.loads(response)['data'][0]

def get_compute_usage(start_time, end_time):
    '''
    Query the compute usage for an account.
    
    Compute includes licenses, instances and Conductor cost. Everything involved
    with running a job.    
    
    Args:
        start_time (datetime.datetime): The first day to include in the report. Only the date is considered and it's assumed to be in UTC.
        end_time (datetime.datetime): The last day to include in the report. Only the date is considered and it's assumed to be in UTC.
        
    Returns:
        dict: Each key is a date (UTC). The value is a dict with values for:
                - cost: The total accumulated compute cost for the day
                - corehours: The total accumulated core hours for the day
                - walltime: The number of minutes that instances (regardless of type) were running
        
    Examples:
        >>> from ciocore import api_client
        >>> api_client.get_compute_usage(start_time, end_time)
        {  '2024-01-09': {  'cost': 0.08,
                            'corehours': 0.9, 
                            'walltime': 13.93},
            '2024-01-16': { 'cost': 0.12,
                            'corehours': 0.9613, 
                            'walltime': 7.21}}
    '''
    date_format = "%a, %d %b %Y %H:%M:%S %Z"
    data = _get_compute_usage(start_time, end_time)

    # Create a nested default dictionary with initial float values of 0.0
    results =  collections.defaultdict(lambda: collections.defaultdict(float))

    for entry in data:
        entry_start_date = datetime.datetime.strptime(entry['start_time'], date_format).date().isoformat()

        results[entry_start_date]['walltime'] += entry['minutes']
        results[entry_start_date]['corehours'] += entry['cores']
        results[entry_start_date]['cost'] += entry['license_cost'] + entry['instance_cost']

    # Round the data to avoid FP errors
    results[entry_start_date]['walltime'] = round(results[entry_start_date]['walltime'], 4)
    results[entry_start_date]['corehours'] = round(results[entry_start_date]['corehours'], 4)
    results[entry_start_date]['cost'] = round(results[entry_start_date]['cost'], 4)
    
    return results

def get_storage_usage(start_time, end_time):
    '''
    Query the storage usage for an account.
    
    Storage is calculated twice a day (UTC) and the average is used.
    
    Args:
        start_time (datetime.datetime): The first day to include in the report. Only the date is considered and it's assumed to be in UTC.
        end_time (datetime.datetime): The last day to include in the report. Only the date is considered and it's assumed to be in UTC.
        
    Returns:
        dict: Each key is a date (UTC). The value is a dict with values for:
                - cost: The cost of accumulated storage for that one day
                - GiB: The total amount of storage used on that day
        
    Examples:
        >>> from ciocore import api_client
        >>> api_client.get_storage_usage(start_time, end_time)
        { '2024-01-01': {'cost': 4.022, 'GiB': 679.714},
          '2024-01-02': {'cost': 4.502, 'GiB': 750.34},
          '2024-01-03': {'cost': 4.502, 'GiB': 750.34}}
    '''
    one_day = datetime.timedelta(days=1)
    
    data = _get_storage_usage(start_time, end_time)

    results =  {}

    entry_date = datetime.date.fromisoformat(data['start_date'])

    for cnt, entry in enumerate(data["cost_per_day"]):

        entry_start_date = entry_date.isoformat()
        results[entry_start_date] = {'cost': float(entry), 'GiB': float(data['gibs_per_day'][cnt])}
        entry_date += one_day

    return results


