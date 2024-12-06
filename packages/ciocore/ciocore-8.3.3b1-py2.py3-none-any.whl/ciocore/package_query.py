"""
Generate markdown from the software packages list.
"""
import os
import sys
import json
from ciocore.package_tree import PackageTree
from ciocore import api_client
import markdown
import io
import tempfile
import webbrowser

PURE = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css" integrity="sha384-X38yfunGUhNzHpBaEBsWLO+A0HDYOQi8ufWDkZ0k9e0eXz/tH3II7uKZ9msv++Ls" crossorigin="anonymous">
<meta name="viewport" content="width=device-width, initial-scale=1">
"""

def green(rhs):
    return "\033[92m{}\033[0m".format(rhs)


def red(rhs):
    return "\033[91m{}\033[0m".format(rhs)


def blue(rhs):
    return "\033[94m{}\033[0m".format(rhs)


def magenta(rhs):
    return "\033[95m{}\033[0m".format(rhs)


def raw(rhs, stream):
    stream.write("{}\n\n".format(rhs))


def d(n, rhs, stream):
    """Indent with dashes"""
    stream.write("{} {}\n".format("-" * n, rhs))


def hr(stream):
    stream.write("---\n\n")


def h(n, rhs, stream):
    stream.write("{} {}\n\n".format("#" * n, rhs))


def plugin_table_header(stream):
    stream.write(
        '|<div style="width:150px">Plugin</div> |<div style="min-width:400px">Versions</div>|\n|:------------|:-------------|\n'
    )


def plugin_table_row(plugin, versions, stream):
    stream.write("|{}|{}|\n".format(plugin, versions))


def write_markdown(hostnames, tree_data, platform, stream):
    """
    Write the tree of packages in Markdown.

    Use this to generate docs for the Conductor mkdocs site.
    """
    if not hostnames:
        return
    h(2, "{} Software".format(platform.capitalize()), stream)
    last_hostgroup = None
    for hostname in hostnames:
        display_hostname = " ".join(hostname.split()[:2])
        hostgroup = hostname.split(" ")[0]
        stream.write("\n")
        if not hostgroup == last_hostgroup:
            hr(stream)
            h(3, hostgroup, stream)
        h(4, display_hostname, stream)
        last_hostgroup = hostgroup
        plugins = tree_data.supported_plugins(hostname)
        if plugins:
            plugin_table_header(stream)
            for plugin in plugins:
                plugin_table_row(
                    plugin["plugin"], ", ".join(plugin["versions"]), stream
                )


def write_text(hostnames, tree_data, platform, color_func, stream):
    """
    Write the tree of packages as text.

    Products are indented with one dash.
    Host packages are indented with two dashes.
    Plugin packages are indented with three dashes.
    """
    if not hostnames:
        d(0, red("There are no '{}' host packages".format(platform)), stream)
        return
    d(0, "{} Software".format(platform).upper(), stream)
    last_hostgroup = None
    for hostname in hostnames:
        display_hostname = " ".join(hostname.split()[:2])
        hostgroup = hostname.split(" ")[0]
        if not hostgroup == last_hostgroup:
            d(0, green("-" * 30), stream)
            d(1, color_func(hostgroup), stream)
        d(2, color_func(display_hostname), stream)
        last_hostgroup = hostgroup
        plugins = tree_data.supported_plugins(hostname)
        if plugins:
            for plugin in plugins:
                d(
                    3,
                    color_func(
                        "{} [{}]".format(
                            plugin["plugin"], ", ".join(plugin["versions"])
                        )
                    ),
                    stream,
                )
                
def sort_hostnames_by_version(hostnames):
    def sort_version(pkg):
        hostname, product, version, platform = pkg
        return f"{version} {product} {platform}"
    def sort_product(pkg):
        hostname, product, version, platform = pkg
        return f"{product} {platform}"
    pkg_sortable = [(hostname, hostname.split()[0], hostname.split()[1], hostname.split()[2]) for hostname in hostnames]
    _psorted = sorted(pkg_sortable, key=sort_version, reverse=True)
    _sorted = sorted(_psorted, key=sort_product)
    return [pkg[0] for pkg in _sorted]

def pq(format="text"):
    packages = api_client.request_software_packages()

    tree_data = PackageTree(packages)

    hostnames = sort_hostnames_by_version(tree_data.supported_host_names())
    linux_hostnames = [h for h in hostnames if h.endswith("linux")]
    windows_hostnames = [h for h in hostnames if h.endswith("windows")]

    if format == "markdown":
        stream = sys.stdout
        raw(
            "This page contains the complete list of software available at Conductor. If you require applications or plugins that are not in the list, please [create a support ticket](https://support.conductortech.com/hc/en-us/requests/new) and let us know.",
            stream,
        )
        write_markdown(linux_hostnames, tree_data, "linux", stream)
        write_markdown(windows_hostnames, tree_data, "windows", stream)
    elif format == "text":
        stream = sys.stdout
        write_text(linux_hostnames, tree_data, "linux", magenta, stream)
        d(0, "", stream)
        write_text(windows_hostnames, tree_data, "windows", blue, stream)
    elif format == "html":
        stream = io.StringIO()
        raw(
            "This page contains the complete list of software available at Conductor. If you require applications or plugins that are not in the list, please [create a support ticket](https://support.conductortech.com/hc/en-us/requests/new) and let us know.",
            stream,
        )

        write_markdown(linux_hostnames, tree_data, "linux", stream)
        write_markdown(windows_hostnames, tree_data, "windows", stream)

        html = markdown.markdown(
            stream.getvalue(), extensions=["markdown.extensions.tables"]
        )

        html = decorate(html)

        stream.close()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write(html)
            webbrowser.open("file://" + f.name, new=2)

def decorate(html):
    html = html.replace("<table>", '<table class="pure-table pure-table-bordered">')
    html = '<html><head>{}</head><body style="margin: 2em;">{}</body></html>'.format(PURE, html)
    return html
