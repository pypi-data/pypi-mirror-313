# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast_vendor.wrapt import register_post_import_hook
from contrast.agent.policy.patch_manager import reverse_patches_by_owner

MOD_WSGI_SERVER = "mod_wsgi.server"


def mod_wsgi_hook(mod_wsgi_server):
    from contrast.agent.agent_state import automatic_middleware
    from contrast.wsgi import ContrastMiddleware
    from contrast.utils.patch_utils import build_and_apply_patch, wrap_and_watermark

    def build___init__(orig_func, _):
        def __init__(wrapped, instance, args, kwargs):
            wrapped(*args, **kwargs)
            with automatic_middleware():
                instance.application = ContrastMiddleware(instance.application)

        return wrap_and_watermark(orig_func, __init__)

    build_and_apply_patch(
        mod_wsgi_server.ApplicationHandler,
        "__init__",
        build___init__,
    )


def register_patches():
    register_post_import_hook(mod_wsgi_hook, MOD_WSGI_SERVER)


def reverse_patches():  # pragma: no cover
    module = sys.modules.get(MOD_WSGI_SERVER)
    if module is not None:
        reverse_patches_by_owner(module.ApplicationHandler)
