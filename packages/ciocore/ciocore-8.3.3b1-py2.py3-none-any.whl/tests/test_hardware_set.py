""" test data

   isort:skip_file
"""
import unittest


from ciocore.hardware_set import HardwareSet

PROJECTS = [
    "Deadpool",
    "Harry Potter & the chamber of secrets",
    "Captain Corelli's Mandolin",
    "Gone with the Wind",
]

from package_fixtures import *
from instance_type_fixtures import (
    CW_INSTANCE_TYPES,
    AWS_INSTANCE_TYPES,
    CW_INSTANCE_TYPES_WITH_GPUS,
    ALL_INSTANCE_TYPES,
)


class TestCategorizedInstanceTypes(unittest.TestCase):
    def setUp(self):
        self.hs = HardwareSet(CW_INSTANCE_TYPES)

    def test_number_of_categories(self):
        self.assertEqual(self.hs.number_of_categories(), 4)

    def test_categories_sorted_on_order(self):
        labels = [i["label"] for i in self.hs.get_model()]
        self.assertEqual(labels, ["low", "mid", "high", "extra"])

    def test_content_count(self):
        low_category_values = [c["value"] for c in self.hs.get_model()[0]["content"]]
        self.assertEqual(low_category_values, ["cw-a-4-16", "cw-b-8-16"])

    def test_in_several_categories(self):
        low_category_values = [c["value"] for c in self.hs.get_model()[0]["content"]]
        extra_category_values = [c["value"] for c in self.hs.get_model()[3]["content"]]
        self.assertIn("cw-a-4-16", low_category_values)
        self.assertIn("cw-a-4-16", extra_category_values)

    def test_category_names(self):
        names = self.hs.labels()
        self.assertEqual(names, ["low", "mid", "high", "extra"])


class TestRecategorizeInstanceTypes(unittest.TestCase):
    def setUp(self):
        self.hs = HardwareSet(CW_INSTANCE_TYPES_WITH_GPUS)

    def test_recategorize_cpu_gpu(self):
        test_func = (
            lambda x: [{"label": "GPU", "order": 2}]
            if "gpu" in x and x["gpu"]
            else [{"label": "CPU", "order": 1}]
        )
        self.hs.recategorize(test_func)
        self.assertEqual(self.hs.number_of_categories(), 2)

    def test_find_all_by_condition(self):
        test_func = lambda x: "gpu" in x and x["gpu"]
        result = self.hs.find_all(test_func)
        self.assertEqual(len(result), 2)
        print(self.hs)

    def test_find_first_by_condition(self):
        test_func = lambda x: x["memory"] < 32
        result = self.hs.find_first(test_func)
        self.assertTrue(result["memory"] < 32)

    def test_find_category(self):
        label = "mid"
        result = self.hs.find_category(label)
        self.assertEqual(result["label"], label)
        self.assertEqual(result["order"], 2)


class TestFind(unittest.TestCase):
    def setUp(self):
        self.hs = HardwareSet(CW_INSTANCE_TYPES_WITH_GPUS)

    def test_find_unspecified_category(self):
        result = self.hs.find("cw-e-4-32")
        self.assertIsNotNone(result)

    def test_category_that_exists(self):
        result = self.hs.find("cw-e-4-32", category="high")
        self.assertIsNotNone(result)

    def test_returns_none_if_not_in_category(self):
        result = self.hs.find("cw-e-4-32", category="low")
        self.assertIsNone(result)

    def test_returns_none_if_non_existent_category(self):
        result = self.hs.find("cw-e-4-32", category="foo")
        self.assertIsNone(result)


class TestUncategorizedInstanceTypes(unittest.TestCase):
    def setUp(self):
        self.hs = HardwareSet(ALL_INSTANCE_TYPES)

    def test_number_of_categories_uncategorized(self):
        self.assertEqual(self.hs.number_of_categories(), 1)

    def test_model_sorted_on_cores_mem(self):
        content = self.hs.get_model()[0]["content"]
        result = [c["label"] for c in content]
        self.assertEqual(
            result,
            [
                "windows 4 core 26.0GB Mem",
                "linux 4 core 27.0GB Mem",
                "linux 8 core 30.0GB Mem",
                "windows 32 core 208.0GB Mem",
                "linux 32 core 208.0GB Mem",
                "windows 64 core 416.0GB Mem",
                "linux 64 core 416.0GB Mem",
            ],
        )


class TestProvider(unittest.TestCase):
    def test_gcp_provider(self):
        hs = HardwareSet(ALL_INSTANCE_TYPES)
        self.assertEqual(hs.provider, "gcp")

    def test_cw_provider(self):
        hs = HardwareSet(CW_INSTANCE_TYPES_WITH_GPUS)
        self.assertEqual(hs.provider, "cw")

    def test_aws_provider(self):
        hs = HardwareSet(AWS_INSTANCE_TYPES)
        self.assertEqual(hs.provider, "aws")
