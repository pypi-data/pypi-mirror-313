# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import Set
from contrast.agent.middlewares.route_coverage.common import (
    DEFAULT_ROUTE_METHODS,
    get_normalized_uri,
)
from contrast.agent.middlewares.route_coverage.common import build_signature
from contrast_fireball import DiscoveredRoute

DEFAULT_ROUTE_METHODS = DEFAULT_ROUTE_METHODS + ("HEAD",)


def create_starlette_routes(starlette_router) -> Set[DiscoveredRoute]:
    """
    Returns all the routes registered to a Starlette router as a dict.
    :param starlette_app: Starlette router instance (starlette.routing.Router)
    :return: dict {route_id:  api.Route}
    """
    from starlette.routing import Mount

    routes = set()

    for app_route in starlette_router.routes:
        if isinstance(app_route, Mount):
            mnt_routes = create_starlette_routes(app_route)
            routes.update(mnt_routes)
            continue

        view_func = app_route.endpoint

        signature = build_signature(app_route.name, view_func)
        methods = app_route.methods or DEFAULT_ROUTE_METHODS

        for method_type in methods:
            routes.add(
                DiscoveredRoute(
                    verb=method_type,
                    url=get_normalized_uri(str(app_route.name)),
                    signature=signature,
                    framework="Starlette",
                )
            )

    return routes
