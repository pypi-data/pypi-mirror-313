# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from dataclasses import replace
from enum import Enum
from typing import List, Optional, Set

import contrast
from contrast.agent.disable_reaction import DisableReaction
from contrast.agent.request import Request
from contrast.configuration.agent_config import AgentConfig
from contrast.configuration.config_option import DEFAULT_VALUE_SRC
from contrast.reporting.reporting_client import ReportingClient
from contrast import get_canonical_version
from contrast_fireball import (
    AgentLanguage,
    AppArchivedError,
    ArgumentValidationError,
    AssessFinding,
    AssessRequest,
    AuthenticationError,
    ConfigurationError,
    DiscoveredRoute,
    InitOptions,
    ObservedRoute,
    Panic,
    UnexpectedError,
    get_info,
    initialize_application,
    Error,
    new_discovered_routes,
    new_observed_route,
    new_finding,
)

from contrast_vendor import structlog as logging, wrapt

logger = logging.getLogger("contrast")


def _handle_errors(return_value=None) -> wrapt.FunctionWrapper:
    """
    A decorator that catches and logs errors that occur while reporting to Contrast.

    Disabling the agent in response to authentication errors or archived applications
    is handled here.

    Errors that indicate a bug in the agent or Fireball are reported to telemetry.

    This decorator should only be used on Client methods, since it expects the
    wrapped function to be a method with AgentConfig stored on the instance.
    """

    @wrapt.function_wrapper
    def wrapper(wrapped, instance, args, kwargs):
        try:
            return wrapped(*args, **kwargs)
        except Error as e:
            if isinstance(
                e, (ConfigurationError, AuthenticationError, AppArchivedError)
            ):
                # These error messages are user-facing. Log them directly without
                # the stack trace to reduce the noise in the message.
                logger.error(e.message)
            else:
                logger.error(
                    "An error occurred while reporting to Contrast", exc_info=e
                )

            if (
                isinstance(
                    e,
                    (
                        Panic,
                        ArgumentValidationError,
                        UnexpectedError,
                    ),
                )
                and contrast.TELEMETRY is not None
            ):
                contrast.TELEMETRY.report_error(e, wrapped)

            if isinstance(
                e,
                (
                    AppArchivedError,
                    AuthenticationError,
                ),
            ):
                DisableReaction.run(instance.config)

            return return_value

    return wrapper


class Client(ReportingClient):
    """
    A client for reporting to the Contrast UI using the Fireball library.
    Fireball docs: https://fireball.prod.dotnet.contsec.com/fireball/index.html

    The client will fallback to directly reporting for endpoints that do not
    have Python bindings yet.
    """

    def __init__(self):
        self.config = None
        info = get_info()
        super().__init__(instance_id=info["reporting_instance_id"])

    @_handle_errors(return_value=False)
    def initialize_application(self, config: AgentConfig, framework="") -> bool:
        """
        Initialize an application in the Contrast UI.

        This function must be called before any other reporting functions.
        """

        # Store config on the client for disable reaction on AppArchivedError
        self.config = config

        result = initialize_application(
            InitOptions(
                app_name=config["application.name"],
                app_path=config["application.path"],
                agent_language=AgentLanguage.PYTHON,
                agent_version=get_canonical_version(),
                server_host_name=config["server.name"],
                server_path=config["server.path"],
                server_type=config["server.type"] or framework,
                config_paths=None,
                overrides=agent_config_to_plain_dict(config),
            )
        )
        self.app_id = result.data["app_id"]
        config.session_id = result.data["common_config"]["application"]["session_id"]

        # This is a workaround to process the startup settings from the UI.
        # Long-term, we'll read the settings from the result, but for now
        # we want to use the well-tested direct response processing behavior.
        return super().initialize_application(config)

    @_handle_errors()
    def new_discovered_routes(self, routes: Set[DiscoveredRoute]):
        """
        Report discovered routes to the Contrast UI.

        If an exception occurs, no routes are reported.
        """

        new_discovered_routes(self.app_id, list(routes))

    @_handle_errors()
    def new_observed_route(self, route: ObservedRoute):
        """
        Record an observed route.

        Routes are reported periodically in batches. This endpoint can be called multiple
        times for the same route, but Fireball will only report duplicate routes at a rate
        of once per minute to avoid overloading TeamServer.
        """

        new_observed_route(self.app_id, route)

    @_handle_errors()
    def new_findings(self, findings: List[AssessFinding], request: Optional[Request]):
        """
        Record Assess findings.

        Findings are reported periodically in batches. Failures are handled for each
        individual finding, so that a failure in one finding does not prevent others
        from being reported.
        """
        fireball_request = request.to_fireball_assess_request() if request else None
        for finding in findings:
            self._new_finding(finding, fireball_request)

    @_handle_errors()
    def _new_finding(self, finding: AssessFinding, request: Optional[AssessRequest]):
        new_finding(self.app_id, replace(finding, request=request))


def agent_config_to_plain_dict(config: AgentConfig):
    """
    Convert all set options in the AgentConfig to a plain dictionary.
    """

    def conv(obj: object):
        if isinstance(obj, Enum):
            return obj.name
        return str(obj)

    return {
        key: conv(v)
        for key, opt in config._config.items()
        if opt.source() != DEFAULT_VALUE_SRC and (v := opt.value()) is not None
    }
