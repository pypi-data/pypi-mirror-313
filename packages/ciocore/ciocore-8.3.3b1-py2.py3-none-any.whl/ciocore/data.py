"""
This module is a singleton that provides the data from Conductor endpoints. Specifically, it provides projects, instance types, and software package data.

Since the data is stored at the module level, you can access it from anywhere in your code without the need to pass it around.
"""

from ciocore.package_tree import PackageTree
from ciocore import api_client
from ciocore.hardware_set import HardwareSet
import copy

__data__ = {}
__products__ = None
__platforms__ = None

def init(*products, **kwargs):
    """
    Initialize the module and let it know what host products to provide.

    Args:
        products (str): Provide a list of products for which to get software packages. If no products are given, the software data contains all products from the packages endpoint. If you provide more than one product, they must all be host level products.

    Keyword Args:
        product (str): `DEPRECATED` Provide one product for which to get software packages.

    Examples:
        >>> from ciocore import data as coredata
        >>> coredata.init()
        # OR
        >>> coredata.init("maya-io")
        # OR LEGACY
        >>> coredata.init(product="all")
        # OR
        >>> coredata.init(product="maya-io")
    """
    global __products__
    global __platforms__
    if products:
        if kwargs.get("product"):
            raise ValueError(
                "Arguments: `products` and `product` specified. Please don't use both together. The `product` arg is deprecated."
            )
        __products__ = list(products)
    elif kwargs.get("product"):
        if kwargs.get("product") == "all":
            __products__ = []
        else:
            __products__ = [kwargs.get("product")]
    else:
        __products__ = []

    __platforms__ = set(kwargs.get("platforms", ["windows", "linux"]))

def data(force=False, instances_filter=""):
    """
    Provide projects, instance types, and software package data.

    Keyword Args:
        force: (bool) If `True`, then force the system to fetch fresh data -- Defaults to `False`.
        instances_filter: (str) complex RHS string query ex:
          "cpu=gte:8:int,operating_system=ne:windows,gpu.gpu_count=eq:1:int"

    Raises:
        ValueError:  Module was not initialized with [init()](/data/#ciocore.data.init).

    Returns:
        dict: Keys are `projects`, `instance_types`, `software`.

    When you access the data, if it has already been fetched, it will be returned. Otherwise,
    requests will be made to fetch the data. You may need to authenticate in order to access the
    data.

    The set of instance types and software can be pruned to match the available platforms
    represented by each other. For example, if the instance types come from an orchestrator that
    provides both Windows and Linux machines, and the software product(s) are available on both
    platforms, no pruning occurs. However, if there are no Windows machines available, any Windows
    software will be removed from the package tree. Similarly, if a product is chosen that only runs
    on Windows, Linux instance types will not appearin the list of available hardware.

    Here is a breakdown of each key in the dictionary:

    * **projects** is a list of project names for your authenticated account.

    * **instance_types** is an instance of HardwareSet, providing you with access to the list of
    available machines configurations.

    * **software** is a PackageTree object containing either all
    the software available at Conductor, or a subset based on specified products.


    Examples:
        >>> from ciocore import data as coredata
        >>> coredata.init(product="maya-io")

        >>> coredata.data()["software"]
        <ciocore.package_tree.PackageTree object at 0x10e9a4040>

        >>> coredata.data()["projects"][0]
        ATestForScott

        >>> coredata.data()["instance_types"]
        <ciocore.hardware_set.HardwareSet object at 0x0000028941CD9DC0>
    """

    global __data__
    global __products__
    global __platforms__

    if __products__ is None:
        raise ValueError(
            'Data must be initialized before use, e.g. data.init("maya-io") or data.init().'
        )
    products_copy = copy.copy(__products__)

    if force:
        clear()
        init(*products_copy)

    if __data__ == {}:
        # PROJECTS
        __data__["projects"] = sorted(api_client.request_projects())
        # INST_TYPES
        instance_types = api_client.request_instance_types(filter_param=instances_filter)
        # SOFTWARE
        software = api_client.request_software_packages()

        # EXTRA ENV VARS
        extra_env_vars = []
        try:
            extra_env_vars = api_client.request_extra_environment()
        except Exception:
            pass   
        __data__["extra_environment"] = extra_env_vars

        # PLATFORMS
        it_platforms = set([it["operating_system"] for it in instance_types])
        valid_platforms = it_platforms.intersection(__platforms__)
        kwargs = {"platforms": valid_platforms}

        # If there's only one product, it's possible to initialize the software tree with a plugin.
        # So we set the product kwarg. Otherwise, we set the host_products kwarg
        host_products = __products__
        if len(__products__) == 1:
            host_products = []
            kwargs["product"] = __products__[0]

        software_tree = PackageTree(software, *host_products, **kwargs)

        if software_tree:
            __data__["software"] = software_tree
            # Revisit instance types to filter out any that are not needed for any software package.
            sw_platforms = software_tree.platforms()

            instance_types = [
                it for it in instance_types if it["operating_system"] in sw_platforms
            ]
        # Then adjust __platforms__ to match the instance types that are represented.
        __platforms__ = set([it["operating_system"] for it in instance_types])

        __data__["instance_types"] = HardwareSet(instance_types)

    return __data__

def valid():
    """
    Check validity.

    Returns:
        bool: True if `projects`, `instance_types`, and `software` are valid.

    Examples:
        >>> from ciocore import data as coredata
        >>> coredata.valid()
        True
    """

    if not __data__.get("projects"):
        return False
    if not __data__.get("instance_types"):
        return False
    if not __data__.get("software"):
        return False
    return True


def clear():
    """
    Clear out data.

    [valid()](/data/#ciocore.data.valid) returns False after clear().
    """
    global __data__
    global __products__
    global __platforms__
    __data__ = {}
    __products__ = None
    __platforms__ = None


def products():
    """

    Returns:
        list(str): The product names. An empty list signifies all products.
    """
    return __products__

def set_fixtures_dir(_):
    """Deprecated. """
    pass

def platforms():
    """
    The set of platforms that both software and instance types are valid on.

    Returns:
        set: A set containing platforms: windows and/or linux.
    """
    return __platforms__

