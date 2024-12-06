# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast_vendor.isort import stdlibs

version_info = sys.version_info
_version_string = f"py{version_info[0]}{version_info[1]}"
_stdlib_modules = (
    getattr(stdlibs, _version_string).stdlib
    if version_info < (3, 10)
    else sys.stdlib_module_names
)


def is_stdlib_module(module_name):
    """
    Returns True if module_name belongs to standard library module, False otherwise.

    NOTE: 'test' is included in _stdlib_modules so if we're testing this,
    we cannot pass in a module that starts with test.file...
    """
    top_module_name = module_name.split(".")[0]
    return top_module_name in _stdlib_modules
