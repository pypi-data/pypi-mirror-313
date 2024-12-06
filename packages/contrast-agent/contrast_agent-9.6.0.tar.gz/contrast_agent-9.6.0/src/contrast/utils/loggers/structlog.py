# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Using logger.info/debug/someOtherLevel() is not supported in this module. In order to get the correct
frame info, we must skip over functions called in this module and in vendored structlog. If logging is attempted,
incorrect frame info will be displayed on the log message if used in this file.

Use print(...) instead
"""
import asyncio
import os
import pathlib
import io
import sys
from functools import partial
from typing import Union, TextIO, Optional

from contrast.agent import request_state
from contrast.utils.namespace import Namespace
from contrast_vendor import structlog
from contrast.utils.configuration_utils import get_hostname
from . import DEFAULT_PROGNAME, DEFAULT_AGENT_LOGGER_PATH


class module(Namespace):
    file_handle: Optional[io.IOBase] = DEFAULT_AGENT_LOGGER_PATH


LOGGING_TO_BUNYAN_LOG_LEVEL_CONVERSION = {
    "critical": 60,
    "error": 50,
    "warning": 40,
    "info": 30,
    "debug": 20,
}


def add_hostname_for_bunyan(logger, method_name, event_dict):
    event_dict["hostname"] = get_hostname()
    return event_dict


def add_request_id(logger, method_name, event_dict):
    event_dict["request_id"] = request_state.get_request_id()
    return event_dict


def rename_key_for_bunyan(old_name, new_name):
    def key_renamer(logger, method_name, event_dict):
        value = event_dict.get(old_name)
        if value and not event_dict.get(new_name):
            event_dict[new_name] = value
            del event_dict[old_name]

        return event_dict

    return key_renamer


def add_log_level_for_bunyan(logger, log_level, event_dict):
    """
    NOTE: Bunyan uses different log level integers than logging/structlog.
    """
    if log_level == "warn":
        # The stdlib has an alias
        log_level = "warning"

    new_value = LOGGING_TO_BUNYAN_LOG_LEVEL_CONVERSION.get(log_level, None)

    if new_value:
        event_dict["level"] = new_value

    return event_dict


def add_v_for_bunyan(logger, method_name, event_dict):
    event_dict["v"] = 0
    return event_dict


def add_progname_for_bunyan(logger, method_name, event_dict, progname=DEFAULT_PROGNAME):
    """
    progname is the name of the process the agents uses in logs.
    The default value is Contrast Agent. progname will be used
    as the name of the logger as seen in the logs.
    """
    event_dict["name"] = progname

    return event_dict


def add_asyncio_info(logger, method_name, event_dict):
    try:
        current_task = asyncio.current_task()

        # If no name has been explicitly assigned to the Task, the default asyncio Task implementation
        # generates a default name during instantiation.
        event_dict["asyncio_task_name"] = current_task.get_name()

        current_coro = current_task.get_coro()
        if hasattr(current_coro, "__name__"):
            event_dict["asyncio_coro_name"] = current_coro.__name__

        event_dict["asyncio_task_id"] = id(current_task)
    except Exception:
        # This can happen when there is no running event loop
        pass

    return event_dict


def _log_level_to_int(level: str) -> int:
    level_to_int = {
        "DEBUG": 10,
        "TRACE": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50,
    }

    level = level.upper()
    if level == "TRACE":
        sys.stderr.write(
            "Contrast Python Agent: TRACE logging is equivalent to DEBUG\n"
        )

    return level_to_int.get(level, level_to_int["INFO"])


def _close_handler():
    ignore_fds = (sys.stderr, sys.stdout, None)
    file_name = getattr(module.file_handle, "name", None)
    # ignore_names handles a specific case for capturing sys.stderr/stdout in pytest
    # see also: https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html
    ignore_names = ("<stderr>", "<stdout>")

    if (
        module.file_handle not in ignore_fds
        and file_name not in ignore_names
        and not module.file_handle.closed
    ):
        module.file_handle.close()

    module.file_handle = None


def _set_handler(log_file: Union[TextIO, str, None]):
    if isinstance(log_file, str):
        try:
            path = pathlib.Path(log_file).parent.resolve()
            os.makedirs(path, exist_ok=True)
            module.file_handle = open(log_file, "a", encoding="utf-8")
        except Exception as e:
            sys.stderr.write(f"Failed to create log file {log_file} - {e}\n")
    elif isinstance(log_file, io.IOBase):
        module.file_handle = log_file
    elif log_file is None:
        module.file_handle = DEFAULT_AGENT_LOGGER_PATH

    return module.file_handle


def shutdown():
    _close_handler()


def init_structlog(
    log_level_name: str,
    log_file: Union[TextIO, str, None],
    progname: str,
    *,
    # NOTE: We should only enable logger caching if its configuration is finalized. If
    # it's possible for the logging config to change in the future, do not cache it.
    cache_logger: bool = False,
) -> None:
    """
    Initial configuration for structlog. This can still be modified by subsequent calls
    to structlog.configure.
    """
    log_level = _log_level_to_int(log_level_name)

    _close_handler()
    file_handle = _set_handler(log_file)

    structlog.configure(
        processors=[
            # exact key "time" required for bunyan parsing
            structlog.processors.TimeStamper(fmt="iso", key="time"),
            add_log_level_for_bunyan,
            rename_key_for_bunyan("event", "msg"),
            structlog.processors.CallsiteParameterAdder(
                [
                    structlog.processors.CallsiteParameter.PROCESS,
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                    structlog.processors.CallsiteParameter.THREAD,
                    structlog.processors.CallsiteParameter.THREAD_NAME,
                ],
                additional_ignores=[
                    "contrast_vendor.structlog",
                    "contrast.utils.decorators",
                ],
            ),
            rename_key_for_bunyan("process", "pid"),
            add_request_id,
            add_asyncio_info,
            add_hostname_for_bunyan,
            partial(add_progname_for_bunyan, progname=progname),
            add_v_for_bunyan,
            structlog.processors.format_exc_info,
            structlog.processors.StackInfoRenderer(
                additional_ignores=[
                    "contrast_vendor.structlog",
                    "contrast.utils.decorators",
                ]
            ),
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.WriteLoggerFactory(file_handle),
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=cache_logger,
    )
