import getpass
import logging
import os
import platform
import socket
import sys

from typing import List

_logger = logging.getLogger("clipped.utils.env")


def is_notebook():
    return "ipykernel" in sys.modules


def get_filename():
    if is_notebook():
        return "notebook"
    try:
        return os.path.basename(__file__)
    except Exception as e:
        _logger.debug("Could not detect filename, %s", e)
        return "not found"


def get_module_path():
    try:
        return os.path.dirname(os.path.realpath("__file__"))
    except Exception as e:
        _logger.debug("Could not detect module path, %s", e)
        return "not found"


def get_user():
    try:
        return getpass.getuser()
    except Exception as e:
        _logger.debug("Could not detect installed packages, %s", e)
        return "unknown"


def get_run_env(packages: List[str]):
    import pkg_resources

    def get_packages():
        try:
            installed_packages = [d for d in pkg_resources.working_set]  # noqa
            return sorted(
                ["{}=={}".format(pkg.key, pkg.version) for pkg in installed_packages]
            )
        except Exception as e:
            _logger.debug("Could not detect installed packages, %s", e)
            return []

    data = {
        "pid": os.getpid(),
        "hostname": socket.gethostname(),
        "os": platform.platform(aliased=True),
        "system": platform.system(),
        "python_version_verbose": sys.version,
        "python_version": platform.python_version(),
        "user": get_user(),
        "sys.argv": sys.argv,
        "is_notebook": is_notebook(),
        "filename": get_filename(),
        "module_path": get_module_path(),
        "packages": get_packages(),
    }

    for package in packages:
        try:
            data[f"{package}_version"] = pkg_resources.get_distribution(package).version
        except pkg_resources.DistributionNotFound:
            data[f"{package}_version"] = ""

    return data
