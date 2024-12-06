""" test data

   isort:skip_file
"""
import datetime
import json
import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from ciocore import api_client

from ciocore.api_client import request_extra_environment
from ciocore.api_client import _get_compute_usage, get_compute_usage
from ciocore.api_client import _get_storage_usage, get_storage_usage

class ApiClientTest(unittest.TestCase):
    @staticmethod
    def path_exists_side_effect(arg):
        if "missing" in arg:
            return False
        else:
            return True

    def setUp(self):
        self.env = {"USERPROFILE": "/users/joebloggs", "HOME": "/users/joebloggs"}

        self.api_key_dict = {"api_key": {"client_id": "123", "private_key": "secret123"}}

        patcher = mock.patch("os.path.exists")
        self.mock_exists = patcher.start()
        self.mock_exists.side_effect = ApiClientTest.path_exists_side_effect
        self.addCleanup(patcher.stop)

    def test_create(self):
        ac = api_client.ApiClient()
        self.assertEqual(ac.__class__.__name__, "ApiClient")

    def test_get_standard_creds_path(self):
        with mock.patch.dict("os.environ", self.env):
            fn = api_client.get_creds_path(api_key=False).replace("\\", "/")
            self.assertEqual(fn, "/users/joebloggs/.config/conductor/credentials")

    def test_get_api_key_creds_path(self):
        with mock.patch.dict("os.environ", self.env):
            fn = api_client.get_creds_path(api_key=True).replace("\\", "/")
            self.assertEqual(fn, "/users/joebloggs/.config/conductor/api_key_credentials")


class TestTruncateMiddle(unittest.TestCase):

    def test_truncation_not_needed(self):
        self.assertEqual(api_client.truncate_middle("short", 10), "short")

    def test_truncation_with_even_max_length(self):
        self.assertEqual(api_client.truncate_middle("1234567890ABCDEF", 8), "1234~DEF")

    def test_truncation_with_odd_max_length(self):
        self.assertEqual(api_client.truncate_middle("1234567890ABCDEF", 9), "1234~CDEF")

    def test_empty_string(self):
        self.assertEqual(api_client.truncate_middle("", 5), "")

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            api_client.truncate_middle(12345, 5)

class TestRegisterClient(unittest.TestCase):
    USER_AGENT_MAX_PATH_LENGTH = 10  # Example max length for testing

    @classmethod
    def setUpClass(cls):
        cls.original_executable = sys.executable
        sys.executable = '/usr/bin/python3'  # Example path for testing

    @classmethod
    def tearDownClass(cls):
        sys.executable = cls.original_executable

    def test_register_client_with_version(self):
        client_name = 'ApiClient'
        client_version = '1.0'

        with mock.patch('platform.python_version', return_value='3.8.2'), \
             mock.patch('platform.system', return_value='Linux'), \
             mock.patch('platform.release', return_value='5.4.0-42-generic'):
            user_agent = api_client.ApiClient.register_client(client_name, client_version)

        expected_user_agent = (
            f"ApiClient/1.0 (python 3.8.2; Linux 5.4.0-42-generic; "
        )
        self.assertTrue(user_agent.startswith(expected_user_agent))

    def test_register_client_without_version(self):
        client_name = 'ApiClient'

        with mock.patch('platform.python_version', return_value='3.8.2'), \
             mock.patch('platform.system', return_value='Linux'), \
             mock.patch('platform.release', return_value='5.4.0-42-generic'):
            user_agent =  api_client.ApiClient.register_client(client_name)


        expected_user_agent = (
            f"ApiClient/unknown (python 3.8.2; Linux 5.4.0-42-generic; "
        )

        self.assertTrue(user_agent.startswith(expected_user_agent))


class TestRequestExtraEnvironment(unittest.TestCase):

    def setUp(self):
        self.api_response_data = {
            "data": [
                {"account_id": "123", "env": ["VAR1=value1", "VAR2=value2"]},
                {"account_id": "456", "env": ["VAR3=value3", "VAR4=value4"]}
            ]
        }
        self.response_ok = mock.MagicMock(status_code=200, text=json.dumps(self.api_response_data))
        self.response_error = mock.MagicMock(status_code=500, text=json.dumps({"error": "Internal Server Error"}))

    @mock.patch("ciocore.api_client.ApiClient")
    @mock.patch("ciocore.api_client.read_conductor_credentials")
    @mock.patch("ciocore.api_client.account_id_from_jwt")
    def test_request_extra_environment_success(self, mock_account_id_from_jwt, mock_read_conductor_credentials, mock_ApiClient):
        # Set up mocks for successful execution
        mock_read_conductor_credentials.return_value = "valid_token"
        mock_account_id_from_jwt.return_value = "123"
        mock_api_instance = mock_ApiClient.return_value
        mock_api_instance.make_request.return_value = (self.response_ok.text, self.response_ok.status_code)

        result = request_extra_environment()

        self.assertEqual(result, ["VAR1=value1", "VAR2=value2"])
        mock_ApiClient.assert_called_once()
        mock_read_conductor_credentials.assert_called_once_with(True)
        mock_account_id_from_jwt.assert_called_once_with("valid_token")

    @mock.patch("ciocore.api_client.ApiClient")
    def test_request_extra_environment_api_failure(self, mock_ApiClient):
        # Set up mock for API failure
        mock_api_instance = mock_ApiClient.return_value
        mock_api_instance.make_request.return_value = (self.response_error.text, self.response_error.status_code)

        # Assert exception raised when the API call fails
        with self.assertRaises(Exception) as context:
            request_extra_environment()

        self.assertIn('Failed to get extra environment', str(context.exception))
        mock_ApiClient.assert_called_once()

    @mock.patch("ciocore.api_client.ApiClient")
    @mock.patch("ciocore.api_client.read_conductor_credentials")
    @mock.patch("ciocore.api_client.account_id_from_jwt")
    def test_request_extra_environment_no_account_env(self, mock_account_id_from_jwt, mock_read_conductor_credentials, mock_ApiClient):
        # Set up mocks to simulate valid token and account ID but no matching environment
        mock_read_conductor_credentials.return_value = "valid_token"
        mock_account_id_from_jwt.return_value = "invalid_id"  # This won't match any 'account_id' in response
        mock_api_instance = mock_ApiClient.return_value
        mock_api_instance.make_request.return_value = (self.response_ok.text, self.response_ok.status_code)

        with self.assertRaises(Exception) as context:
            request_extra_environment()

        self.assertEqual("Error: Could not get account environment!", str(context.exception))
        mock_ApiClient.assert_called_once()

class TestGetComputeUsage(unittest.TestCase):

    def setUp(self):
        
        # Precison is rounded to 4 places to avoid FP issues.
        self.compute_response_data = {
            "data": [
                {
                    "cores": 0.5, 
                    "instance_cost": 0.0200, 
                    "license_cost": 0.0200, 
                    "minutes": 6.9700, 
                    "self_link": 0, 
                    "start_time": "Tue, 09 Jan 2024 18:00:00 GMT"
                }, 
                {
                    "cores": 0.4, 
                    "instance_cost": 0.0200, 
                    "license_cost": 0.0200, 
                    "minutes": 6.9600, 
                    "self_link": 1, 
                    "start_time": "Tue, 09 Jan 2024 19:00:00 GMT"
                }, 
                {
                    "cores": 0.9613, 
                    "instance_cost": 0.0400, 
                    "license_cost": 0.0800, 
                    "minutes": 7.2100, 
                    "self_link": 2, 
                    "start_time": "Tue, 16 Jan 2024 17:00:00 GMT"
                }, 
            ]
        }
     
        self.response_ok = mock.MagicMock(status_code=200, text=json.dumps(self.compute_response_data))
        self.response_error = mock.MagicMock(status_code=500, text=json.dumps({"error": "Internal Server Error"}))

    @mock.patch("ciocore.api_client.ApiClient")
    @mock.patch("ciocore.api_client.read_conductor_credentials")
    @mock.patch("ciocore.api_client.account_id_from_jwt")
    def test_query_raw_compute_usage(self, mock_account_id_from_jwt, mock_read_conductor_credentials, mock_ApiClient):
        # Set up mocks for successful execution
        mock_read_conductor_credentials.return_value = "valid_token"
        mock_account_id_from_jwt.return_value = "123"
        mock_api_instance = mock_ApiClient.return_value
        mock_api_instance.make_request.return_value = (self.response_ok.text, self.response_ok.status_code)

        start_time = datetime.datetime(2024, 1, 1)
        end_time = datetime.datetime(2024, 3, 20)

        result = _get_compute_usage(start_time, end_time)

        self.assertEqual(result, self.compute_response_data['data'])
        
    @mock.patch("ciocore.api_client.ApiClient")
    @mock.patch("ciocore.api_client.read_conductor_credentials")
    @mock.patch("ciocore.api_client.account_id_from_jwt")
    def test_compute_usage(self, mock_account_id_from_jwt, mock_read_conductor_credentials, mock_ApiClient):
        # Set up mocks for successful execution
        mock_read_conductor_credentials.return_value = "valid_token"
        mock_account_id_from_jwt.return_value = "123"
        mock_api_instance = mock_ApiClient.return_value
        mock_api_instance.make_request.return_value = (self.response_ok.text, self.response_ok.status_code)

        start_time = datetime.datetime(2024, 1, 1)
        end_time = datetime.datetime(2024, 3, 20)

        result = get_compute_usage(start_time=start_time, end_time=end_time)

        self.assertEqual(result, {  '2024-01-09': {'cost': 0.08,
                                                 'corehours': 0.9, 
                                                 'walltime': 13.93},
                                    '2024-01-16': { 'cost': 0.12,
                                                    'corehours': 0.9613, 
                                                    'walltime': 7.21}})
        
    @mock.patch("ciocore.api_client.ApiClient")
    def test_get_compute_usage_api_failure(self, mock_ApiClient):
        # Set up mock for API failure
        mock_api_instance = mock_ApiClient.return_value
        mock_api_instance.make_request.return_value = (self.response_error.text, self.response_error.status_code)

        start_time = datetime.datetime(2024, 1, 1)
        end_time = datetime.datetime(2024, 3, 20)
        
        # Assert exception raised when the API call fails
        with self.assertRaises(Exception) as context:
            get_compute_usage(start_time, end_time)

        self.assertIn('Failed to query compute usage', str(context.exception))
        mock_ApiClient.assert_called_once()    
class TestGetStorageUsage(unittest.TestCase):

    def setUp(self):
               
        self.storage_response_data = {
            "data": [
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
        
        self.response_ok = mock.MagicMock(status_code=200, text=json.dumps(self.storage_response_data))
        self.response_error = mock.MagicMock(status_code=500, text=json.dumps({"error": "Internal Server Error"}))
        
    @mock.patch("ciocore.api_client.ApiClient")
    @mock.patch("ciocore.api_client.read_conductor_credentials")
    @mock.patch("ciocore.api_client.account_id_from_jwt")
    def test_query_raw_storage_usage(self, mock_account_id_from_jwt, mock_read_conductor_credentials, mock_ApiClient):
        # Set up mocks for successful execution
        mock_read_conductor_credentials.return_value = "valid_token"
        mock_account_id_from_jwt.return_value = "123"
        mock_api_instance = mock_ApiClient.return_value
        mock_api_instance.make_request.return_value = (self.response_ok.text, self.response_ok.status_code)

        start_time = datetime.datetime(2024, 5, 1)
        end_time = datetime.datetime(2024, 5, 17)

        result = _get_storage_usage(start_time, end_time)

        self.assertEqual(result, self.storage_response_data['data'][0])

    @mock.patch("ciocore.api_client.ApiClient")
    @mock.patch("ciocore.api_client.read_conductor_credentials")
    @mock.patch("ciocore.api_client.account_id_from_jwt")
    def test_storage_usage(self, mock_account_id_from_jwt, mock_read_conductor_credentials, mock_ApiClient):
        # Set up mocks for successful execution
        mock_read_conductor_credentials.return_value = "valid_token"
        mock_account_id_from_jwt.return_value = "123"
        mock_api_instance = mock_ApiClient.return_value
        mock_api_instance.make_request.return_value = (self.response_ok.text, self.response_ok.status_code)

        start_time = datetime.datetime(2024, 1, 1)
        end_time = datetime.datetime(2024, 1, 7)

        result = get_storage_usage(start_time=start_time, end_time=end_time)
        
        self.assertEqual(result, {  '2024-01-01': {'cost': 4.022, 'GiB': 679.714},
                                    '2024-01-02': {'cost': 4.502, 'GiB': 750.34},
                                    '2024-01-03': {'cost': 4.502, 'GiB': 750.34},
                                    '2024-01-04': {'cost': 5.102, 'GiB': 850.36},
                                    '2024-01-05': {'cost': 5.102, 'GiB': 850.35},
                                    '2024-01-06': {'cost': 5.732, 'GiB': 955.32}
                                  })