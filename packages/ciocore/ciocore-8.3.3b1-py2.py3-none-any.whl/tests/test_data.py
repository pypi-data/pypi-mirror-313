import unittest
from unittest.mock import patch, MagicMock
from ciocore import data as coredata

class TestCoreData(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_api_responses = {
            'projects': ['ProjectA', 'ProjectB'],
            'instance_types': [
                {'operating_system': 'windows', 'name': 'win_machine', 'cores': 1, 'memory': '1024'},
                {'operating_system': 'linux', 'name': 'linux_machine', 'cores': 1, 'memory': '1024'}
            ],
            'software': [  # Added package_id to each package
                {
                    'name': 'maya-io',
                    'version': '2022',
                    'platform': 'windows',
                    'product': 'maya-io',
                    'package_id': '123456789'
                },
                {
                    'name': 'maya-io',
                    'version': '2022',
                    'platform': 'linux',
                    'product': 'maya-io',
                    'package_id': '123456780'
                },
                {
                    'name': 'nuke',
                    'version': '13.0',
                    'platform': 'linux',
                    'product': 'nuke',
                    'package_id': '123456781'
                }
            ],
            'extra_env': ['PATH=/custom/path', 'LICENSE_SERVER=1234']
        }
        # Clear data before each test
        coredata.clear()

    def tearDown(self):
        """Clean up after each test method."""
        coredata.clear()

    def test_init_with_single_product(self):
        """Test initializing with a single product"""
        coredata.init("maya-io")
        self.assertEqual(coredata.products(), ["maya-io"])
        self.assertEqual(coredata.platforms(), set(["windows", "linux"]))

    def test_init_with_multiple_products(self):
        """Test initializing with multiple products"""
        coredata.init("maya-io", "nuke")
        self.assertEqual(coredata.products(), ["maya-io", "nuke"])

    def test_init_with_deprecated_product(self):
        """Test initializing with deprecated product kwarg"""
        coredata.init(product="maya-io")
        self.assertEqual(coredata.products(), ["maya-io"])

    def test_init_with_all_products(self):
        """Test initializing with 'all' products"""
        coredata.init(product="all")
        self.assertEqual(coredata.products(), [])

    def test_init_conflict_raises_error(self):
        """Test that using both products arg and product kwarg raises error"""
        with self.assertRaises(ValueError):
            coredata.init("maya-io", product="nuke")

    def test_data_requires_init(self):
        """Test that data() raises error if not initialized"""
        with self.assertRaises(ValueError):
            coredata.data()

    @patch('ciocore.data.api_client')
    def test_data_fetching(self, mock_client):
        """Test fetching data through the data() function"""
        # Setup mock responses
        mock_client.request_projects.return_value = self.mock_api_responses['projects']
        mock_client.request_instance_types.return_value = self.mock_api_responses['instance_types']
        mock_client.request_software_packages.return_value = self.mock_api_responses['software']
        mock_client.request_extra_environment.return_value = self.mock_api_responses['extra_env']

        coredata.init("maya-io")
        result = coredata.data()
        
        self.assertIn("projects", result)
        self.assertIn("instance_types", result)
        self.assertIn("software", result)
        self.assertIn("extra_environment", result)
        
        self.assertEqual(result["projects"], self.mock_api_responses["projects"])
        self.assertIsInstance(result["instance_types"], coredata.HardwareSet)
        self.assertIsInstance(result["software"], coredata.PackageTree)

    @patch('ciocore.data.api_client')
    def test_force_refresh(self, mock_client):
        """Test forcing data refresh"""
        # Setup mock responses
        mock_client.request_projects.return_value = self.mock_api_responses['projects']
        mock_client.request_instance_types.return_value = self.mock_api_responses['instance_types']
        mock_client.request_software_packages.return_value = self.mock_api_responses['software']
        mock_client.request_extra_environment.return_value = self.mock_api_responses['extra_env']

        coredata.init("maya-io")
        first_data = coredata.data()
        
        # Second call without force should not make new API calls
        mock_client.request_projects.reset_mock()
        second_data = coredata.data()
        mock_client.request_projects.assert_not_called()
        
        # Call with force=True should make new API calls
        third_data = coredata.data(force=True)
        mock_client.request_projects.assert_called_once()

    def test_valid_state(self):
        """Test valid() function behavior"""
        self.assertFalse(coredata.valid())  # Should be invalid before initialization
        
        coredata.init("maya-io")
        self.assertFalse(coredata.valid())  # Should be invalid before data is fetched
        
        with patch('ciocore.data.api_client') as mock_client:
            # Setup mock responses
            mock_client.request_projects.return_value = self.mock_api_responses['projects']
            mock_client.request_instance_types.return_value = self.mock_api_responses['instance_types']
            mock_client.request_software_packages.return_value = self.mock_api_responses['software']
            mock_client.request_extra_environment.return_value = self.mock_api_responses['extra_env']
            
            coredata.data()  # Fetch data
            self.assertTrue(coredata.valid())  # Should be valid after data is fetched
        
        coredata.clear()
        self.assertFalse(coredata.valid())  # Should be invalid after clear

    @patch('ciocore.data.api_client')
    def test_platforms_filtering(self, mock_client):
        """Test platform filtering based on instance types and software"""
        # Setup mock responses
        mock_client.request_projects.return_value = self.mock_api_responses['projects']
        mock_client.request_instance_types.return_value = self.mock_api_responses['instance_types']
        mock_client.request_software_packages.return_value = self.mock_api_responses['software']
        mock_client.request_extra_environment.return_value = self.mock_api_responses['extra_env']

        coredata.init("nuke")  # nuke only supports linux
        coredata.data()
        
        # Should only have linux instance types since nuke only supports linux
        self.assertEqual(coredata.platforms(), {"linux"})

    @patch('ciocore.data.api_client')
    def test_instances_filter(self, mock_client):
        """Testing that instance_types is passed correctly to api_client"""
        # Set up mock response
        mock_client.request_instance_types.return_value = self.mock_api_responses['instance_types']
        coredata.init("maya-io")

        # Test with no filter
        coredata.data()
        mock_client.request_instance_types.assert_called_with(filter_param="")
        
        # Test with filter and force=True
        mock_client.request_instance_types.reset_mock()

        instances_filter = "gpu.gpu_count=gte:1:int"
        coredata.data(force=True, instances_filter=instances_filter)
        mock_client.request_instance_types.assert_called_with(filter_param=instances_filter)

if __name__ == '__main__':
    unittest.main()