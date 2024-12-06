""" test package_query
"""
import unittest
import os
import sys
import copy
from ciocore import package_tree
from ciocore import package_query
from package_fixtures import *

class HostnameSortByVersionTest(unittest.TestCase):
    def setUp(self):
        self.packages = copy.deepcopy(SOFTWARE_DATA)
        self.pt = package_tree.PackageTree(self.packages)
        self.hostname_list = self.pt.supported_host_names()
    
    def test_sort_hostnames_by_version(self):
        sorted_hostnames = package_query.sort_hostnames_by_version(self.hostname_list)
        sorted_data = {}
        for item in sorted_hostnames:
            product, version, platform = item.split()
            data = {
                'version': version,
                'platform': platform
            }
            if product in sorted_data.keys():
                sorted_data[product].append(data)
            else:
                sorted_data[product] = [data]
        self.assertTrue(sorted(list(sorted_data.keys())) == list(sorted_data.keys()))
        for product in sorted_data.keys():
            platform_list = [pkg['platform'] for pkg in sorted_data[product]]
            self.assertTrue(sorted(platform_list) == platform_list)
            version_list = [pkg['version'] for pkg in sorted_data[product] if pkg['platform'] == 'linux']
            self.assertTrue(sorted(version_list, reverse=True) == version_list)

if __name__ == "__main__":
    unittest.main()
