# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implements patches for the operator module

Our propagation rewrites are implemented in terms of these patches, so they
must always be enabled when Assess is enabled.
"""
import sys

from contrast.agent.assess.policy.propagators.base_propagator import SUPPORTED_TYPES
from contrast_vendor.wrapt import register_post_import_hook

from contrast.agent import scope
from contrast.agent.assess.utils import is_trackable
from contrast.agent.assess.policy import string_propagation
from contrast.agent.policy import patch_manager
from contrast.patches.utils import analyze_policy, get_propagation_node
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import build_and_apply_patch, wrap_and_watermark


def cformat_propagation_func(format_str: object):
    if isinstance(format_str, str):
        return string_propagation.propagate_unicode_cformat
    if isinstance(format_str, bytes):
        return string_propagation.propagate_bytes_cformat
    if isinstance(format_str, bytearray):
        # TODO: PYT-2709 - Update tests to verify bytearray is supported
        return string_propagation.propagate_bytearray_cformat
    return None


@fail_quietly("failed to propagate through modulo in contrast__cformat__modulo")
def _propagate_cformat(propagation_func, result, format_str, args):
    with scope.contrast_scope(), scope.propagation_scope():
        propagation_func(result, format_str, result, args, None)


def build_add_hook(original_func, patch_policy):
    policy_node = get_propagation_node(patch_policy)

    def add(wrapped, instance, args, kwargs):
        del instance

        if not isinstance(args[0], SUPPORTED_TYPES) and not isinstance(
            args[1], SUPPORTED_TYPES
        ):
            # This is an operation we don't support, so we return the result
            # without any tracking.
            # Don't enter scope, because this could be an operation against
            # a class with a custom __add__ method, and we want to track
            # dataflow through that user code.
            return wrapped(*args, **kwargs)

        with scope.contrast_scope():
            result = wrapped(*args, **kwargs)
        if not is_trackable(result) or scope.in_contrast_or_propagation_scope():
            return result

        analyze_policy(policy_node.name, result, args, kwargs)

        return result

    return wrap_and_watermark(original_func, add)


def build_mod_hook(original_func, patch_policy):
    # cformat is a bit of a special case so we don't use policy here
    del patch_policy

    def mod(wrapped, instance, args, kwargs):
        del instance

        format_string = args[0]
        prop_func = cformat_propagation_func(format_string)
        if prop_func is None:
            # This is a modulo operation that we don't support,
            # so we return the result without any tracking.
            # Don't enter scope, because this could be an operation
            # against a class with a custom __mod__ method, and we
            # want to track dataflow through that user code.
            return wrapped(*args, **kwargs)

        with scope.contrast_scope():
            result = wrapped(*args, **kwargs)
        if not is_trackable(result) or scope.in_contrast_or_propagation_scope():
            return result
        _propagate_cformat(prop_func, result, *args)

        return result

    return wrap_and_watermark(original_func, mod)


def patch_operator(operator_module):
    build_and_apply_patch(operator_module, "add", build_add_hook)
    build_and_apply_patch(operator_module, "iadd", build_add_hook)
    build_and_apply_patch(operator_module, "mod", build_mod_hook)


def register_patches():
    register_post_import_hook(patch_operator, "operator")


def reverse_patches():
    operator_module = sys.modules.get("operator")
    if not operator_module:
        return

    patch_manager.reverse_patches_by_owner(operator_module)
