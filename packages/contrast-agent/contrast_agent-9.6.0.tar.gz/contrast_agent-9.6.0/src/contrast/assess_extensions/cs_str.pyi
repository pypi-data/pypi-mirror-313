# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys


Py_TPFLAGS_HEAPTYPE: int
if sys.version_info >= (3, 10):
    Py_TPFLAGS_IMMUTABLETYPE: int

DEBUG: int


def initialize() -> None: ...
def disable() -> None: ...
def enable_required_hooks() -> None: ...


def get_tp_version_tag(type: type, /) -> int: ...


def set_attr_on_type(owner: type, name: str, value, /) -> None: ...
