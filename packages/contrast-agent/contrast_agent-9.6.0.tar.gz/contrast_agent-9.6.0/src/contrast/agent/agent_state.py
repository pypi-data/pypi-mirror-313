# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections.abc import Mapping
import sys
import atexit
import threading
import warnings

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Optional, Tuple
from contrast.utils.configuration_utils import get_platform

import contrast
from contrast import __version__, AGENT_CURR_WORKING_DIR
from contrast.agent.exclusions import Exclusions
from contrast.agent.inventory import runtime_environment
from contrast.reporting import Reporter, get_reporting_client
from contrast.utils.locale import DEFAULT_ENCODING
from contrast.agent import (
    agent_lib,
    thread_watcher,
    patch_controller,
    sys_monitoring,
)
from contrast.agent.assess.sampling import SamplerConfig, update_sampler_config
from contrast.agent.assess import contrast_event
from contrast.agent.assess.rules.providers.enable import enable_providers
from contrast.agent.settings import Settings
from contrast.utils.exceptions.deprecation_warning import ContrastDeprecationWarning
from contrast.utils.loggers.logger import (
    configure_syslog_logger,
    setup_basic_agent_logger,
    configure_agent_logger,
    setup_security_logger,
)
from contrast.utils import timer
from contrast.utils.library_reader.library_reader import LibraryReader
from contrast.utils.namespace import Namespace
from contrast.utils.decorators import fail_loudly
from contrast_rewriter import (
    process_rewriter_logs,
    set_rewriter_logger,
)
from contrast_rewriter import is_rewriter_enabled
from contrast.reporting.request_masker import RequestMasker

# NOTE: policy is currently loaded/generated on import. It is applied explicitly in
# policy/applicator.py
from contrast import policy  # noqa: F401

logger = setup_basic_agent_logger()
LOGS_SEPARATOR = "-" * 120

SHARED_WARNING_MESSAGE = """
For specific circumstances where explicit middleware configuration is still
required, set `agent.python.enable_automatic_middleware` to `false` in the
configuration file or set `CONTRAST__AGENT__PYTHON__ENABLE_AUTOMATIC_MIDDLEWARE=false`
in your environment to suppress this warning.

Please see the documentation for additional details:
    https://docs.contrastsecurity.com/en/python-middleware.html
"""

MIDDLEWARE_WITHOUT_RUNNER_WARNING = f"""
Explicit middleware configuration is no longer required or recommended. Instead,
users should run their application with the `contrast-python-run` command, which
automatically detects and enables framework-specific middleware.
{SHARED_WARNING_MESSAGE}
"""

NO_EXPLICIT_MIDDLEWARE_WARNING = f"""
Explicit middleware configuration is generally no longer necessary when using
the `contrast-python-run` command.
{SHARED_WARNING_MESSAGE}
"""

NO_SPECIFIC_MIDDLEWARE_WARNING = """
Using framework-specific middleware is no longer recommended for {}.
Use contrast.{}.ContrastMiddleware instead.
"""

PROTECT_MISMATCH_MESSAGE = (
    "Protect enabled in local config but disabled in Contrast UI. It is running."
)
ASSESS_MISMATCH_MESSAGE = (
    "Assess enabled in local config but disabled in Contrast UI. It is running."
)

if not contrast.telemetry_disabled():
    from contrast.agent.telemetry import Telemetry
else:
    Telemetry = None

Watcher = Optional  # A Watcher is a type that will watch config changes.


class module(Namespace):
    server_environment: Optional[str] = None
    init_lock: threading.Lock = threading.Lock()
    sampling_cfg: Watcher[SamplerConfig] = None
    exclusions: Watcher[Exclusions] = None
    request_data_masker: Watcher[RequestMasker] = None

    is_initialized = False
    id: Optional[int] = None
    settings: Optional[Settings] = None
    reporting_client: Optional[Reporter] = None
    library_reader: Optional[LibraryReader] = None
    first_request: bool = True
    assess_enabled: bool = False
    assess_tags = ""

    automatic_middleware: ContextVar = ContextVar("automatic_middleware", default=False)

    deprecated_middleware: Optional[Tuple[str, bool]] = None

    configured_app_name: Optional[str] = None
    configured_server_name: Optional[str] = None

    # NOTE: these field can be set prior to initialization
    framework: Optional[str] = None
    app_name: Optional[str] = None


def is_runner_in_use():
    from contrast.agent.runner import is_runner_in_use

    return is_runner_in_use()


def _log_environment(settings: Settings):
    """
    Log current working directory, python version and pip version
    """
    log_level = settings.config.get_option("agent.logger.level").value().upper()

    logger.info(
        "ENVIRONMENT",
        python_version=sys.version,
        agent_version=__version__,
        assess_enabled=module.assess_enabled,
        protect_enabled=settings.is_protect_enabled(),
        using_runner=is_runner_in_use(),
        using_rewriter=is_rewriter_enabled(),
        using_sys_monitoring=sys_monitoring.is_enabled(),
        log_level=log_level,
        configured_application_name=module.configured_app_name,
        detected_application_name=module.app_name,
        detected_framework=module.framework,
        installed_framework=settings.framework,
        installed_webserver=settings.server,
        cwd=AGENT_CURR_WORKING_DIR,
        executable=sys.executable,
        platform=get_platform(),
        default_encoding=DEFAULT_ENCODING,
    )

    # py38: remove
    if sys.version_info[:2] == (3, 8):
        _log_and_warn(
            "Contrast Security support for Python 3.8 is deprecated and will be removed"
            " in October 2024"
        )


def _warn_for_misleading_config(settings: Settings):
    protect_option = settings.config.get_option("protect.enable")
    protect_enabled = protect_option.value()
    if protect_enabled and not protect_option.ui_value:
        logger.warning(PROTECT_MISMATCH_MESSAGE)

    assess_option = settings.config.get_option("assess.enable")
    assess_enabled = assess_option.value()
    if assess_enabled and not assess_option.ui_value:
        logger.warning(ASSESS_MISMATCH_MESSAGE)

    if (
        settings.is_agent_config_enabled()
        and not protect_enabled
        and not assess_enabled
    ):
        logger.warning("Neither Protect nor Assess is enabled. Neither is running.")


def initialize_libraries():
    """
    If enabled, read libraries from the application
    :return: True
    """
    if not module.settings.is_analyze_libs_enabled():
        return

    # Passing callback to send message due to a circular import issue, and a
    # deadlock occurring if something is imported inside of a function running in
    # this thread
    module.library_reader = LibraryReader(
        module.settings,
        send_ts_message_func=module.reporting_client.add_message,
    )
    module.library_reader.start_library_analysis_thread()


@fail_loudly("Unable to initialize Contrast Agent Settings.", return_value=False)
def initialize_settings():
    """
    Initialize agent settings.

    Returns True on settings being initialized and False if any failure.
    """
    module.settings = Settings(framework_name=module.framework)

    return True


def is_initialized() -> bool:
    return module.is_initialized


def get_settings():
    return module.settings


def get_server_environment():
    return module.server_environment


def _get_app_name(config: Mapping, app_name):
    if config and (config_name := config.get("application.name")):
        return config_name

    return app_name if app_name else "root"


def get_app_name():
    return module.configured_app_name or _get_app_name(
        module.settings.config, module.app_name
    )


def _get_server_name(config: Mapping):
    """
    Hostname of the server

    Default is socket.gethostname() or localhost
    """
    if config:
        return config.get("server.name")
    return None


def get_server_name():
    return module.configured_server_name or _get_server_name(module.settings.config)


def is_first_request():
    return module.first_request


def set_first_request(val: bool):
    module.first_request = val


def set_assess_enabled(config: Mapping):
    module.assess_enabled = config["assess.enable"]


@fail_loudly("Failed to register detected framework")
def set_detected_framework(name: str):
    """
    Registers the name of the detected framework

    It is safe to call this method prior to initialization of agent state. In
    order to be effective, this method should be called prior to middleware
    initialization.
    """
    module.framework = name


@fail_loudly("Failed to register application name")
def set_application_name(name: Optional[str]):
    """
    Registers the name of the application

    It is safe to call this method prior to initialization of agent state. In
    order to be effective, this method should be called prior to middleware
    initialization.
    """
    module.app_name = name


def set_server_environment_and_sampler(config):
    module.server_environment = config.get("server.environment")

    update_sampler_config(config)


def set_exclusions(config: Mapping):
    module.exclusions = Exclusions(config)


def set_data_masking(config: Mapping):
    module.request_data_masker = RequestMasker(config)


def _log_and_warn(msg):
    warnings.warn(msg, ContrastDeprecationWarning, stacklevel=2)
    logger.warning(msg)


def _check_middleware_warnings():
    # NOTE: currently, we are skipping framework-specific middleware deprecation
    # warnings. In the future, we might want to actually deprecate these. For now,
    # however, we are holding off.
    if False and module.deprecated_middleware is not None:
        (  # pylint: disable=unpacking-non-sequence
            framework,
            is_asgi,
        ) = module.deprecated_middleware
        message = NO_SPECIFIC_MIDDLEWARE_WARNING.format(
            framework, "asgi" if is_asgi else "wsgi"
        )
        _log_and_warn(message)

    # This configuration suppresses both warnings
    if not module.settings.config.enable_automatic_middleware:
        return

    # Warn for the case where the runner is not used at all and middleware is
    # explicitly configured
    if not is_runner_in_use():
        _log_and_warn(MIDDLEWARE_WITHOUT_RUNNER_WARNING)
    # Warn for the case where middleware is explicitly configured but also detected automatically
    # An actual warning doesn't seem necessary in this case, just a log message
    elif not module.automatic_middleware.get():
        logger.warning(NO_EXPLICIT_MIDDLEWARE_WARNING)


@fail_loudly("Failed to process logs from rewriter")
def _process_rewriter_logs(logger):
    if is_runner_in_use():
        logger.debug("---- Beginning of deferred rewriter logs ----")
        process_rewriter_logs(logger)
        logger.debug("---- End of deferred rewriter logs ----")
    else:
        logger.debug("Not checking for deferred rewriter logs")

    logger.debug("Setting rewriter logger to agent logger")
    set_rewriter_logger(logger)


def initialize():
    """
    If this method is called more than once per process, we use the is_initialized
    flag to only run the following work once:
        - library analysis thread initialization
        - turning on patches
        - hardcoded rule providers
        - scanning config rules
        - environment logging
        - loading common configuration
        - initializing settings

    In order to avoid a warning message, callers should check is_initialized()
    prior to calling this function.
    """
    with module.init_lock:
        if module.is_initialized:
            _check_middleware_warnings()
            logger.warning("Attempted to initialize agent state more than once")
            return

        module.id = id(module)

        logger.info(
            "Initializing Contrast Agent %s",
            __name__,
            id=module.id,
            version=__version__,
        )

        if not initialize_settings():
            return

        if module.settings is None:
            logger.warning("Contrast Agent is not enabled.")
            return

        module.configured_server_name = _get_server_name(module.settings.config)
        module.configured_app_name = _get_app_name(
            module.settings.config, module.app_name
        )
        module.assess_tags = module.settings.config["assess.tags"]

        if not module.settings.is_agent_config_enabled():
            logger.warning("Contrast Agent is disabled by local configuration.")
            module.settings.log_effective_config()
            return

        module.settings.config.add_watcher(configure_agent_logger)
        module.settings.config.add_watcher(configure_syslog_logger)
        setup_security_logger(module.settings.config)
        module.settings.config.add_watcher(set_assess_enabled)
        module.settings.config.add_watcher(set_exclusions)
        module.settings.config.add_watcher(set_data_masking)
        module.settings.config.add_watcher(set_server_environment_and_sampler)
        module.settings.config.log_config()

        if module.assess_enabled:
            if module.settings.config.should_enable_sys_monitoring:
                sys_monitoring.enable()
            else:
                logger.debug(
                    "sys.monitoring explicitly disabled in local config - will not enable"
                )

        # NOTE (TODO: PYT-3016)
        # This assumes that initialize is only ever called from middleware.
        # If at some point this no longer holds, it may be necessary to pass a
        # flag to initialize indicating whether these warnings should be
        # processed or not.
        _check_middleware_warnings()

        # The rewriter is applied long before we have any settings or logger so
        # the deferred logs are finally processed here
        _process_rewriter_logs(logger)

        module.reporting_client = get_reporting_client(module.settings.config)
        module.reporting_client.start()

        if not module.reporting_client.initialize_application(
            module.settings.config, framework=module.settings.framework.name_lower
        ):
            disable_agent(reason="Unable to initialize application in Contrast UI")
            module.settings.log_effective_config()
            return

        _warn_for_misleading_config(module.settings)

        # Eventually this should be handled by Fireball.
        if module.settings.is_agent_config_enabled():
            from contrast.reporting.teamserver_messages.effective_config import (
                EffectiveConfig,
            )

            module.reporting_client.add_message(EffectiveConfig())

        # This MUST happen after the initialization calls for TeamServer messaging
        # (sending server start and application start) to ensure that TeamServer will
        # accept the messages sent by our background reporting threads
        # Skip telemetry since it is enabled later in this method
        thread_watcher.ensure_running(module, skip_telemetry=True)

        module.settings.log_effective_config()

        if module.settings.is_inventory_enabled():
            initialize_libraries()

        runtime_environment.report_server_runtime(
            module.reporting_client,
            module.settings.config.get("server.discover_cloud_resource"),
        )

        patch_controller.enable_patches()

        if module.assess_enabled:
            # For now agent runtime starts before config scanning
            # this will be reset when time_limit_threshold is reached,
            # it doesn't symbolize the total agent runtime for all time.
            module.settings.agent_runtime_window = timer.now_ms()

            contrast_event.initialize(module.settings.config)

            enable_providers()
            # NOTE (TODO: PYT-3016) This should stay in middleware
            # scan_configs_in_thread()

        if module.settings.is_protect_enabled() and not agent_lib.initialize(
            module.settings.config
        ):
            disable_agent(reason="Unable to initialize Protect analysis library")
            return

        _log_environment(module.settings)

        logger.info(
            "Finished Initializing Contrast Agent %s",
            __name__,
            id=module.id,
        )

        if Telemetry is not None:
            contrast.TELEMETRY = Telemetry()
            contrast.TELEMETRY.start()
            atexit.register(contrast.TELEMETRY.stop)

        module.is_initialized = True


def disable_agent(reason: str):
    logger.error("Fatal error: Disabling Contrast", reason=reason)
    if module.settings and module.settings.config:
        enable_option = module.settings.config.get_option("enable")
        enable_option.override_value = False


def detected_deprecated_middleware(*, framework: str = "", is_asgi: bool = False):
    module.deprecated_middleware = (framework, is_asgi)


@contextmanager
def automatic_middleware():
    """
    Context manager to be used by automatic middleware hooks when initializing middleware

    This enables us to determine when middleware is initialized from within our
    automatic middleware hooks without having to change the API of any
    middleware classes.
    """
    try:
        module.automatic_middleware.set(True)
        yield
    finally:
        module.automatic_middleware.set(False)


def in_automatic_middleware() -> bool:
    return module.automatic_middleware.get()
