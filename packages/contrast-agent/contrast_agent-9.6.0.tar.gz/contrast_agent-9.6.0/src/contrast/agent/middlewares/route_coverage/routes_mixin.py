# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import List, Optional

from contrast_fireball import (
    AssessFinding,
    AssessRoute,
    AssessRouteObservation,
    ObservedRoute,
)
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class RoutesMixin:
    """
    Class for route coverage work.
    Route coverage is assess only.
    """

    def handle_routes(self, context, request) -> None:
        """
        Method that should run for all middlewares at the end of request processing.
        """
        if context and request:
            self.update_route_information(context, request)
            self.append_route_to_findings(context.observed_route, context.findings)

    def update_route_information(self, context, request) -> None:
        """
        Store the information for this request's route on RequestContext.
        """
        context.observed_route = ObservedRoute(
            signature=self._get_signature(context, request) or "",
            url=context.request.get_normalized_uri(),
            verb=request.method,
            sources=context.observed_route.sources,
        )

        logger.debug(
            "stored observed route on context", observed_route=context.observed_route
        )

    def _get_signature(self, context, request) -> Optional[str]:
        """
        There are a few different strategies we might use to obtain a route signature.
        In order of preference:

        1.  Obtain a signature at some point during the request; this string is set on
            `context.view_func_str`. For supported frameworks, this is accomplished with
            framework-specific patches. One exception to this is aiohttp, where it
            happens directly in the middleware. It is essential that for a particular
            route this signature exactly matches the one found during route discovery.
            In the future, all frameworks will take this approach.

        2.  If context.view_func_str isn't set, we didn't get any framework-specific
            information about the view function. In this case we use the request's
            normalized URI as the signature. We expect to hit this case in pure WSGI /
            ASGI.

        Framework-specific route observation code should set either view_func_str, which
        takes priority, or view_func. It doesn't make sense to set both, since only
        view_func_str would be used in that case.
        """
        if context.view_func_str:
            return context.view_func_str

        logger.debug(
            "Did not find a view function signature for the current request. "
            "Falling back on normalized URI."
        )
        return context.request.get_normalized_uri()

    def append_route_to_findings(
        self, observed_route: ObservedRoute, findings: List[AssessFinding]
    ):
        """
        Append the observed route to any existing findings. We can't necessarily do this
        at finding creation time, because we might not have route info yet.
        """
        if not findings:
            logger.debug("No findings to append route to")
            return

        for finding in findings:
            if not finding.routes:
                logger.debug(
                    "Appending route %s:%s to %s",
                    observed_route.verb,
                    observed_route.url,
                    finding.rule_id,
                )
                finding.routes.append(
                    AssessRoute(
                        count=1,
                        signature=observed_route.signature,
                        observations=[
                            AssessRouteObservation(
                                url=observed_route.url, verb=observed_route.verb or ""
                            )
                        ],
                    )
                )
