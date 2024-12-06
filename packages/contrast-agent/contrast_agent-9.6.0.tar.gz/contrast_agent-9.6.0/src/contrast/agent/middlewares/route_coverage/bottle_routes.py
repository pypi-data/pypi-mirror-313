# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import Set
from contrast.agent.middlewares.route_coverage.common import (
    build_signature,
    DEFAULT_ROUTE_METHODS,
    get_normalized_uri,
)
from contrast_fireball import DiscoveredRoute

DEFAULT_ROUTE_METHODS = DEFAULT_ROUTE_METHODS + ("PUT", "PATCH", "DELETE")


def create_bottle_routes(app) -> Set[DiscoveredRoute]:
    """
    Returns all the routes registered to a Bottle app.
    """
    return {
        DiscoveredRoute(
            verb=method_type,
            url=get_normalized_uri(str(route.rule)),
            signature=build_signature(route.rule, route.callback),
            framework="Bottle",
        )
        for route in app.routes
        for method_type in DEFAULT_ROUTE_METHODS
    }
