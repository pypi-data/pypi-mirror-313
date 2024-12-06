"""
This module contains the **HardwareSet** class. 

It is designed to allow submission tools and other clients that consume instance types to be able to display them in categories. This is particularly useful for UIs that utilize combo-boxes, since they can be orgnaized into a nested structure and displayed in a tree-like fashion.

        
"""
import copy
import logging

logger = logging.getLogger(__name__)


#   {
#     "cores": 32,
#     "description": "32 core, 120GB Mem (8 V100 GPUs with 16GB Mem)",
#     "gpu": {
#       "gpu_architecture": "NVIDIA Volta",
#       "gpu_count": 8,
#       "gpu_cuda_cores": 5120,
#       "gpu_memory": "16",
#       "gpu_model": "V100",
#       "total_gpu_cuda_cores": 40960,
#       "total_gpu_memory": "128"
#     },
#     "memory": "120",
#     "name": "n1-standard-32-v1-8",
#     "operating_system": "linux"
#   },


DESCRIPTION_TEMPLATE_OS = {
    "cpu": "{operating_system} {cores} core {memory}GB Mem",
    "gpu": "{operating_system} {cores} core {memory}GB Mem ({gpu_count} {gpu_model} GPUs {gpu_memory}GB Mem)",
}
DESCRIPTION_TEMPLATE = {
    "cpu": "{cores} core {memory}GB Mem",
    "gpu": "{cores} core {memory}GB Mem ({gpu_count} {gpu_model} GPUs {gpu_memory}GB Mem)",
}

def flatten_dict(d):
    flat_dict = {}
    for key, value in d.items():
        if isinstance(value, dict):
            nested_dict = flatten_dict(value)
            for nested_key, nested_value in nested_dict.items():
                flat_dict[nested_key] = nested_value
        else:
            flat_dict[key] = value
    return flat_dict


class HardwareSet(object):
    """A class to manage categorized instance types.

    A HardwareSet encapsulates the instance types available to an account. It accepts a flat list of instance types and builds a nested structure where those instance types exist in categories.

    It keeps a dictionary of instance types (`instance_types`) with the name field as key. This allows easy lookup by name.

    In addition, it keeps the nested structure of categories (`categories`) that contain the instance types. Each category is a dictionary with keys: `label`, `content`, and `order`.

    `content` is a list of instance types in the category. The order is used to sort the categories. The order of the instance types within a category is determined by the number of cores and memory.

    If all instance_types have not been assigned any categories, then the structure is built with two default categories: CPU and GPU.
    """

    def __init__(self, instance_types):
        """Initialize the HardwareSet with a list of instance types.
        Typically, you would access the HardwareSet through the ciocore.data.data() function, which initializes it for you. However, you can also initialize it directly with a list of instance types straight from ciocore.api_client. The difference being that the latter contains all instance types, whereas the former contains only the instance types compatible with the products you have specified, as well as being cached.

        Args:
            instance_types (list): A list of instance types.

        Returns:
            HardwareSet: The initialized HardwareSet.

        Examples:
            ### Initialize with a list of instance types
            >>> from ciocore import api_client
            >>> from ciocore.hardware_set import HardwareSet
            >>> instance_types = api_client.request_instance_types()
            >>> hardware_set = HardwareSet(instance_types)
            <ciocore.hardware_set.HardwareSet object at 0x104c43d30>

            ### Initialize implicitly with a list of instance types from ciocore.data (recommended).
            >>> from ciocore import data as coredata
            >>> coredata.init("cinema4d")
            >>> hardware_set = coredata.data()["instance_types"]
            <ciocore.hardware_set.HardwareSet object at 0x104c43ee0>

            !!! note
                To avoid repetition, we use the implicit initialization for the examples below.
        """
        
        self.instance_types = self._build_unique(instance_types)
        self.categories = self._build_categories()
        self.provider = self._get_provider()

    def labels(self):
        """Get the list of category labels.

        Returns:
            list: A list of category labels.

        Example:
            >>> from ciocore import data as coredata
            >>> coredata.init()
            >>> hardware_set = coredata.data()["instance_types"]
            >>> hardware_set.labels()
            ['CPU', 'GPU']

        """
        return [c["label"] for c in self.categories]

    def number_of_categories(self):
        """Get the number of categories in the data.

        Returns:
            int: The number of categories.

        Example:
            >>> from ciocore import data as coredata
            >>> coredata.init()
            >>> hardware_set = coredata.data()["instance_types"]
            >>> hardware_set.number_of_categories()
            2

        """
        return len(self.categories)

    def recategorize(self, partitioner):
        """Recategorize the instance types.

        Args:
            partitioner (function): A function that takes an instance type and returns a list of categories to assign to it. The function should return an empty list if the instance type should not be categorized.

        Example:
            # Confirm current categories
            >>> from ciocore import data as coredata
            >>> coredata.init()
            >>> hardware_set = coredata.data()["instance_types"]
            >>> print(hardware_set.labels()
            ['CPU', 'GPU']

            # Recategorize
            >>> hardware_set.recategorize(lambda x: [{'label': 'Low cores', 'order': 10}] if  x["cores"] < 16 else [{'label': 'High cores', 'order': 20}])
            >>> print(hardware_set.labels()
            ['Low cores', 'High cores']
        """
        for key in self.instance_types:
            self.instance_types[key]["categories"] = partitioner(
                self.instance_types[key]
            )
        self.categories = self._build_categories()

    def find(self, name, category=None):
        """Find an instance type by its name (sku).

        Args:
            name (str): The name of the instance type.

        Returns:
            dict: The instance type or None if not found.
        Example:
            >>> from ciocore import data as coredata
            >>> coredata.init()
            >>> hardware_set = coredata.data()["instance_types"]
            >>> hardware_set.find("n2-highmem-80")
            {
                'cores': 80,
                'description': '80 core, 640GB Mem',
                'gpu': None,
                'memory': '640',
                'name': 'n2-highmem-80',
                'operating_system': 'linux',
                'categories': [
                    {'label': 'High cores', 'order': 20}
                ]
            }

        """
        if not category:
            return self.instance_types.get(name)

        return self.find_first(
            lambda x: x["name"] == name
            and category in [c["label"] for c in x["categories"]]
        )

    def find_category(self, label):
        """Find a category by label.

        Args:
            label (str): The label of the category.

        Returns:
            dict: The category or None if not found.
        Example:
            >>> from ciocore import data as coredata
            >>> coredata.init()
            >>> hardware_set = coredata.data()["instance_types"]
            >>> hardware_set.find_category("High cores")
            {
                "label": "Low cores",
                "content": [
                    {
                        "cores": 8,
                        "description": "8 core, 52GB Mem",
                        "gpu": None,
                        "memory": "52",
                        "name": "n1-highmem-8",
                        "operating_system": "linux",
                        "categories": [{"label": "Low cores", "order": 10}],
                    },
                    {
                        "cores": 8,
                        "description": "8 core, 7.2GB Mem",
                        "gpu": None,
                        "memory": "7.2",
                        "name": "n1-highcpu-8",
                        "operating_system": "linux",
                        "categories": [{"label": "Low cores", "order": 10}],
                    },
                    ...
                ],
                "order": 10
            }
        """
        return next((c for c in self.categories if c["label"] == label), None)

    def find_all(self, condition):
        """Find all instance types that match a condition.

        Args:
            condition (function): A function that takes an instance type and returns True or False.

        Returns:
            list: A list of instance types that match the condition.

        Example:
            >>> from ciocore import data as coredata
            >>> coredata.init()
            >>> hardware_set = coredata.data()["instance_types"]
            >>> hardware_set.find_all(lambda x: x["gpu"])
            [
                {
                    "cores": 4,
                    "description": "4 core, 15GB Mem (1 T4 Tensor GPU with 16GB Mem)",
                    "gpu": {
                        "gpu_architecture": "NVIDIA Turing",
                        "gpu_count": 1,
                        "gpu_cuda_cores": 2560,
                        "gpu_memory": "16",
                        "gpu_model": "T4 Tensor",
                        "gpu_rt_cores": 0,
                        "gpu_tensor_cores": 0,
                        "total_gpu_cuda_cores": 2560,
                        "total_gpu_memory": "16",
                        "total_gpu_rt_cores": 0,
                        "total_gpu_tensor_cores": 0,
                    },
                    "memory": "15",
                    "name": "n1-standard-4-t4-1",
                    "operating_system": "linux",
                    "categories": [{"label": "Low cores", "order": 10}],
                },
                {
                    "cores": 8,
                    "description": "8 core, 30GB Mem (1 T4 Tensor GPU with 16GB Mem)",
                    "gpu": {
                        "gpu_architecture": "NVIDIA Turing",
                        "gpu_count": 1,
                        "gpu_cuda_cores": 2560,
                        "gpu_memory": "16",
                        "gpu_model": "T4 Tensor",
                        "gpu_rt_cores": 0,
                        "gpu_tensor_cores": 0,
                        "total_gpu_cuda_cores": 2560,
                        "total_gpu_memory": "16",
                        "total_gpu_rt_cores": 0,
                        "total_gpu_tensor_cores": 0,
                    },
                    "memory": "30",
                    "name": "n1-standard-8-t4-1",
                    "operating_system": "linux",
                    "categories": [{"label": "Low cores", "order": 10}],
                },
                ...
            ]
        """
        result = []
        for key in self.instance_types:
            if condition(self.instance_types[key]):
                result.append(self.instance_types[key])
        return result

    def find_first(self, condition):
        """Find the first instance type that matches a condition.

        Please see find_all() above for more details. This method is just a convenience wrapper around find_all() that returns the first result or None if not found.

        Args:
            condition (function): A function that takes an instance type and returns True or False.

        Returns:
            dict: The first instance type that matches the condition or None if not found.
        """
        return next(iter(self.find_all(condition)), None)

    # DEPRECATED
    def get_model(self, with_misc=False):
        """Get the categories structure with renaming ready for some specific widget, such as a Qt Combobox.

        Deprecated:
            The get_model() method is deprecated. The `with_misc` parameter is no longer used, which means that this function only serves to rename a few keys. What's more, the init function ensures that every instance type has a category. This function is no longer needed. Submitters that use it will work but should be updated to use the categories structure directly as it minimizes the levels of indirection necessary to work with it.
        """
        if with_misc:
            logger.warning("with_misc is no longer used")
        result = []
        for category in self.categories:
            result.append(
                {
                    "label": category["label"],
                    "content": [
                        {"label": k["description"], "value": k["name"]}
                        for k in category["content"]
                    ],
                }
            )

        return result

    # PRIVATE METHODS
    @classmethod
    def _build_unique(cls, instance_types):
        """Build a dictionary of instance types using the name field as key. This allows fast lookup by name.

        Args:
            instance_types (list): A list of instance types.

        Returns:
            dict: A dictionary of instance types with the name field as key.
        """

        instance_types = cls._rewrite_descriptions(instance_types)
        categories = [
            category
            for it in instance_types
            for category in (it.get("categories") or [])
        ]
        result = {}
        for it in instance_types:
            is_gpu = it.get("gpu", False)
            if categories:
                if it.get("categories") in [[], None]:
                    continue
            else:
                # make our own categories GPU/CPU
                it["categories"] = (
                    [{"label": "GPU", "order": 2}]
                    if is_gpu
                    else [{"label": "CPU", "order": 1}]
                )
            result[it["name"]] = it

        return result




    @classmethod
    def _rewrite_descriptions(cls, instance_types):
        """Rewrite the descriptions of the instance types.
        
        If there are both OS types, then the descriptions are prefixed with the OS type.

        Args:
            instance_types (list): A list of instance types.

        Returns:
            list: A list of instance types with rewritten descriptions.
        """
        if not instance_types:
            return instance_types
        
        first_os = instance_types[0]["operating_system"]
        dual_platforms = next((it for it in instance_types if it["operating_system"] != first_os), False)

        if dual_platforms:
            for it in instance_types:
                flat_dict = flatten_dict(it)
                is_gpu = "gpu_count" in flat_dict
                if is_gpu:
                    it["description"] = DESCRIPTION_TEMPLATE_OS["gpu"].format(**flat_dict)
                else:
                    it["description"] = DESCRIPTION_TEMPLATE_OS["cpu"].format(**flat_dict)
        else:
            for it in instance_types:
                flat_dict = flatten_dict(it)
                is_gpu = "gpu_count" in flat_dict
                if is_gpu:
                    it["description"] = DESCRIPTION_TEMPLATE["gpu"].format(**flat_dict)
                else:
                    it["description"] = DESCRIPTION_TEMPLATE["cpu"].format(**flat_dict)

        return instance_types

    def _build_categories(self):
        """Build a sorted list of categories where each category contains a sorted list of machines.

        Returns:
            list: A list of categories where each category is a dictionary with keys: `label`, `content`, and `order`.
        """

        dikt = {}
        for key in self.instance_types:
            it = self.instance_types[key]
            categories = it["categories"]
            for category in categories:
                label = category["label"]
                if label not in dikt:
                    dikt[label] = {
                        "label": label,
                        "content": [],
                        "order": category["order"],
                    }
                dikt[label]["content"].append(it)

        result = []
        for label in dikt:
            category = dikt[label]
            category["content"].sort(key=lambda k: (k["cores"], k["memory"]))
            result.append(category)
        return sorted(result, key=lambda k: k["order"])

    def _get_provider(self):
        """Get the provider from the first instance type.

        Returns:
            str: The provider.
        """
        first_name = next(iter(self.instance_types))
        if not first_name:
            return None
        if first_name.startswith("cw-"):
            return "cw"
        if "." in first_name:
            return "aws"
        return "gcp"
