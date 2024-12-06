# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import Set
from contrast.agent.middlewares.route_coverage import common
from contrast_fireball import DiscoveredRoute


def create_routes(app) -> Set[DiscoveredRoute]:
    """
    Returns all the routes registered to a Flask or Quart app
    """
    routes = set()

    for rule in list(app.url_map.iter_rules()):
        view_func = app.view_functions[rule.endpoint]
        signature = common.build_signature(rule.endpoint, view_func)
        methods = rule.methods or common.DEFAULT_ROUTE_METHODS
        for method_type in methods:
            routes.add(
                DiscoveredRoute(
                    verb=method_type,
                    url=common.get_normalized_uri(str(rule)),
                    signature=signature,
                    framework=("Quart" if type(app).__name__ == "Quart" else "Flask"),
                )
            )

    return routes
