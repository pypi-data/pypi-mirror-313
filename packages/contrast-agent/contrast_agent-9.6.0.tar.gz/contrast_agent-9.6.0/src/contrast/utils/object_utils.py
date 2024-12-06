# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import copy
import inspect

NOTIMPLEMENTED_MSG = "This method should be implemented by concrete subclass subclass"


def safe_copy(value):
    """
    Return a safe copy of a value

    :param value: to be copied
    :return: copied value if no exception
    """
    try:
        return copy.copy(value)
    except Exception:
        return value


def get_name(obj):
    return f"{obj.__module__}.{obj.__name__}" if inspect.isclass(obj) else obj.__name__
