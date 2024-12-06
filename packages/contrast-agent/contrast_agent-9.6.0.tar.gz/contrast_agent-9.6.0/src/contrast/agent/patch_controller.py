# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.policy import string_propagation
from contrast.agent.policy import registry
from contrast.agent.policy.applicator import register_import_hooks
from contrast.agent.policy.rewriter import apply_rewrite_policy
from contrast.agent.settings import Settings
from contrast.assess_extensions import cs_str
from contrast.patches import (
    cs_str as cs_str_patches,
    register_assess_patches,
    register_common_patches,
    register_library_patches,
)
from contrast.utils.namespace import Namespace
from contrast.utils.patch_utils import repatch_imported_modules
from contrast_rewriter import register as register_rewriter

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

ALWAYS_PURE_PYTHON_METHODS = ["format", "__repr__", "__getitem__"]


class module(Namespace):
    assess_patches_enabled: bool = False


def enable_method_hooks(string_types):
    """
    Enable string propagation hooks for individual string type methods

    This method uses policy to determine all of the string methods that need to be
    patched. Patches are applied in pure Python.
    """
    for strtype in string_types:
        for node in registry.get_string_method_nodes():
            method_name = node.method_name

            if method_name.lower() in ["cast", "concat"]:
                # these are applied directly in the C extension only
                continue

            real_method_name = (
                "format_map" if method_name == "formatmap" else method_name
            )

            if not hasattr(strtype, real_method_name):
                continue

            cs_str_patches.patch_strtype_method(strtype, real_method_name)
            logger.debug(
                "Applied pure Python patch for %s.%s", strtype.__name__, method_name
            )


def enable_assess_patches():
    """
    Enables string patches.

    Has no effect if these patches are already enabled.
    """
    if module.assess_patches_enabled:
        return
    # NOTE: String propagator functions *must* be built before the extension
    # is initialized.
    string_propagation.build_string_propagator_functions()
    cs_str.initialize()
    cs_str.enable_required_hooks()
    cs_str_patches.enable_str_properties()
    enable_method_hooks([str, bytes, bytearray])

    module.assess_patches_enabled = True


def disable_assess_patches():
    """
    Disables extension hooks and other string patches.

    Has no effect if these patches are not already enabled.

    This does not disable "pure python" strtype patches applied with set_attr_on_type.
    """
    if not module.assess_patches_enabled:
        return

    cs_str.disable()

    module.assess_patches_enabled = False


def _enable_protect_patches():
    register_common_patches()

    logger.debug("adding protect policy")
    register_import_hooks(protect_mode=True)

    # This has no effect if the patches are not enabled
    disable_assess_patches()


def _enable_assess_patches(settings: Settings):
    enable_assess_patches()

    # Policy-based rewrites need to be applied prior to any policy patches.
    # Policy patches can be layered on top of rewritten functions. So that
    # means we need to make sure that the "original" function called by the
    # policy patch is the *rewritten* one.
    # Pathlib rewrites must not be applied here. They are only stable when applied by
    # the runner. The exact reason for this is unknown, but it's related to repatching.
    # If this causes noticeable issues, use the runner. This will eventually be
    # mandatory anyway, and policy-based rewrites will be removed from here entirely.
    apply_rewrite_policy(rewrite_pathlib=False)

    logger.debug("enabled assess string patches")
    register_common_patches()
    register_assess_patches()

    logger.debug("adding assess policy")
    register_import_hooks()

    # This is included as a fallback so that we continue to support the case
    # where the runner is not used. If the rewriter has already been enabled by
    # the runner, this has no effect (other than to log a message).
    register_rewriter()


def enable_patches():
    settings = Settings()

    if settings.is_analyze_libs_enabled():
        register_library_patches()

    if settings.is_protect_enabled():
        _enable_protect_patches()

    from contrast.agent import agent_state

    if agent_state.module.assess_enabled:
        _enable_assess_patches(settings)

    logger.debug("revisiting imported modules to apply patches")
    repatch_imported_modules()
