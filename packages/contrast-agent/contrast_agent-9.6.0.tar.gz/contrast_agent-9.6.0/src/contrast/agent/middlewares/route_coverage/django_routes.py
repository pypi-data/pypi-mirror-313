# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import Set

import ast
import textwrap
import functools

from collections import deque
from copy import copy
from importlib import import_module
from types import FunctionType, MethodType
from inspect import isclass, getsource
from contrast_fireball import DiscoveredRoute
from django.urls import get_resolver
from django.urls.exceptions import Resolver404
from django.utils.regex_helper import normalize

from contrast.agent.middlewares.route_coverage.common import (
    DEFAULT_ROUTE_METHODS,
    build_args_from_function,
)

from contrast_vendor import structlog as logging
from contrast.utils.decorators import fail_quietly

logger = logging.getLogger("contrast")


def check_for_http_decorator(func):
    """
    Grabs the require_http_methods decorator from a view function call via inspect

    NOTE: this only works for require_http_methods; it does not currently work for require_GET,
    require_POST, require_safe
    """
    method_types = {}

    if isinstance(func, functools.partial):
        func = getattr(func, "func", None)

    if func is None:
        return method_types

    def visit_function_def(node):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                # decorator name which should be require_http_methods
                if getattr(decorator.func, "id", "") == "require_http_methods":
                    name = (
                        decorator.func.attr
                        if isinstance(decorator.func, ast.Attribute)
                        else decorator.func.id
                    )
                    method_list = decorator.args[0] if len(decorator.args) > 0 else []
                    method_str_list = list(
                        filter(
                            None,
                            [
                                getattr(s, "value", "")
                                for s in getattr(method_list, "elts", [])
                            ],
                        )
                    )
                    if not method_str_list:
                        continue
                    method_types[name] = method_str_list
                    return

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_function_def
    node_source = textwrap.dedent(getsource(func))
    node_iter.visit(ast.parse(node_source))

    return method_types


def get_lowest_function_call(func):
    if isclass(func) or func.__closure__ is None:
        return func
    closure = (c.cell_contents for c in func.__closure__)
    return next((c for c in closure if isinstance(c, (FunctionType, MethodType))), None)


def create_url(pattern_or_resolver):
    pattern = pattern_or_resolver.pattern.regex.pattern

    try:
        normalized = normalize(pattern)[0][0]
        url = normalized.replace("%(", "{").replace(")", "}")
    except Exception:
        url = pattern_or_resolver.name

    return url


def get_method_info(pattern_or_resolver):
    method_types = []
    method_arg_names = "()"

    lowest_function = get_lowest_function_call(pattern_or_resolver.callback)

    if lowest_function is not None:
        method_arg_names = build_args_from_function(lowest_function)

        # this method returns a dict because it uses one to store state in the recursive function
        method_types_dict = check_for_http_decorator(lowest_function)
        method_types = method_types_dict.get("require_http_methods", [])

        if not isinstance(method_types, list):
            method_types = [method_types]

    return method_types or DEFAULT_ROUTE_METHODS, method_arg_names


def create_routes(urlpatterns) -> Set[DiscoveredRoute]:
    from django.urls.resolvers import (
        URLPattern as RegexURLPattern,
        URLResolver as RegexURLResolver,
    )

    routes = set()

    urlpatterns_deque = deque(urlpatterns)

    while urlpatterns_deque:
        url_pattern = urlpatterns_deque.popleft()

        if isinstance(url_pattern, RegexURLResolver):
            urlpatterns_deque.extend(url_pattern.url_patterns)

        elif isinstance(url_pattern, RegexURLPattern):
            method_types, method_arg_names = get_method_info(url_pattern)
            url = create_url(url_pattern)
            signature = build_django_signature(url_pattern, method_arg_names)
            for method_type in method_types:
                routes.add(
                    DiscoveredRoute(
                        verb=method_type,
                        url=url,
                        signature=signature,
                        framework="Django",
                    )
                )
    return routes


def create_django_routes() -> Set[DiscoveredRoute]:
    """
    Grabs all URL's from the root settings and searches for possible required_method decorators

    In Django there is no implicit declaration of GET or POST. Often times decorators are used to fix this.

    Returns a dict of key = id, value = api.Route.
    """

    from django.conf import settings

    if not settings.ROOT_URLCONF:
        logger.info("Application does not define settings.ROOT_URLCONF")
        logger.debug("Skipping enumeration of urlpatterns")
        return set()

    try:
        root_urlconf = import_module(settings.ROOT_URLCONF)
    except Exception as exception:
        logger.debug("Failed to import ROOT_URLCONF: %s", exception)
        return set()

    try:
        urlpatterns = root_urlconf.urlpatterns or []
    except Exception as exception:
        logger.debug("Failed to get urlpatterns: %s", exception)
        return set()

    url_patterns = copy(urlpatterns)
    return create_routes(url_patterns)


def _function_loc(func):
    """Return the function's module and name"""
    return f"{func.__module__}.{func.__name__}"


def build_django_signature(obj, method_arg_names=None):
    if hasattr(obj, "lookup_str"):
        signature = obj.lookup_str
    elif hasattr(obj, "callback"):
        cb = obj.callback
        signature = _function_loc(cb)
    elif callable(obj):
        signature = _function_loc(obj)
    else:
        logger.debug(
            "WARNING: can't build django signature for object type %s", type(obj)
        )
        return ""

    if method_arg_names is None:
        method_arg_names = build_args_from_function(obj)

    signature += method_arg_names
    return signature


@fail_quietly("Failed to get view function for django application")
def get_view_func(path):
    from django.conf import settings

    try:
        result = get_resolver().resolve(path or "/")
    except Resolver404:
        return None

    if (
        result is None
        and not path.endswith("/")
        and "django.middleware.common.CommonMiddleware" in settings.MIDDLEWARE
        and settings.APPEND_SLASH
    ):
        result = get_view_func(f"{path}/")
    if result is None:
        return None

    return result.func
