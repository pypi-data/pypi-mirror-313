import os

# Get the version from the VERSION file
# The VERSION file may be in the current directory or (in dev) one directory up


def read_version(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as version_file:
            return version_file.read().strip()
    except IOError:
        return None


file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "VERSION")
version = read_version(file_path)
if not version:
    file_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "VERSION"
    )
    version = read_version(file_path)
if not version:
    version = "dev"
