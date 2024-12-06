# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast_vendor.wrapt import register_post_import_hook
from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import build_and_apply_patch, wrap_and_watermark


def build_noop_patch(original_func, patch_policy):
    del patch_policy

    def noop_intern(wrapped, instance, args, kwargs):
        """
        Defeat interning by returning the original string

        sys.intern takes no kwargs
        """
        del wrapped, instance, kwargs

        return args[0]

    return wrap_and_watermark(original_func, noop_intern)


def patch_sys(module):
    build_and_apply_patch(module, "intern", build_noop_patch)


def register_patches():
    register_post_import_hook(patch_sys, "sys")


def reverse_patches():
    # sys is always imported, no need to check
    patch_manager.reverse_patches_by_owner(sys)
