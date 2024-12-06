# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

from contrast_rewriter import rewrite_for_pytest
from contrast.agent import scope
from contrast.agent.patch_controller import enable_assess_patches
from contrast.agent.policy.rewriter import apply_rewrite_policy
from contrast.configuration.agent_config import AgentConfig
from contrast.patches import register_middleware_patches
from contrast_vendor import structlog as logging

from contrast.scripts.runner import USING_RUNNER_ENV_VAR

logger = logging.getLogger("contrast")


def is_runner_in_use() -> bool:
    """
    We could probably check PYTHONPATH or see if our sitecustomize.py is in sys.modules,
    but using our own totally isolated env var is very safe
    """
    return os.environ.get(USING_RUNNER_ENV_VAR, "false") == "true"


@scope.contrast_scope()
def start_runner():
    if rewrite_for_pytest():
        apply_rewrite_policy(override_config=True)
        return

    config = AgentConfig()

    # Policy-based rewrites need to be applied prior to any policy patches.
    # Policy patches can be layered on top of rewritten functions. So that
    # means we need to make sure that the "original" function called by the
    # policy patch is the *rewritten* one.
    if config.should_apply_policy_rewrites:
        apply_rewrite_policy()

    if config.enable_automatic_middleware:
        register_middleware_patches()

    if config.assess_enabled:
        # NOTE: policy is currently loaded/generated on import. It is applied explicitly
        # in policy/applicator.py later
        from contrast import policy  # noqa: F401

        enable_assess_patches()
