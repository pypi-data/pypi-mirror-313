# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import OrderedDict
import functools
import inspect
import sys
from typing import Optional

from contrast.utils.decorators import fail_quietly
from contrast_vendor import wrapt

from contrast.agent.policy import patch_manager
from contrast.utils.object_utils import get_name

from contrast_vendor.wrapt import function_wrapper
from contrast_vendor import structlog as logging

from contrast.utils.string_utils import ensure_string

logger = logging.getLogger("contrast")


def add_watermark(func):
    """
    Adds a "secret" attribute to patched function for debugging purposes.

    Do not rely on the existence of this attribute in agent source code.
    """
    try:
        func.__contrast__ = True
    except Exception:
        pass
    return func


def wrap_and_watermark(orig_func, wrapper):
    # NOTE: adding a watermark here doesn't make a ton of sense anymore since
    # 1. The function wrapper always has a __wrapped__ attribute, which is a good watermark itself
    # 2. We can't apply the watermark to the wrapped function because in that
    # case it actually gets applied to the underlying object (which we don't want).
    return function_wrapper(add_watermark(wrapper))(orig_func)


def pack_self(instance: Optional[object], args: tuple) -> tuple:
    """Instance can never be None"""
    return args if instance is None else (instance,) + args


def build_and_apply_patch(
    owner,
    attr_name,
    patch_builder,
    builder_args=None,
    owner_name=None,
    force=False,
):
    """
    Builds new patch using given builder and applies it to specified patch location

    :param owner: Module or class where patch will be applied
    :param loc_name: Fully specified name of module or class where patch will apply
    :param attr_name: Name of the method that is being patched/replaced
    :param patch_builder: Callback function used to build new patch
    :param builder_args: A tuple of positional args to be passed to `patch_builder`

    The `patch_builder` function must take at least two arguments:
        1. A pointer to the original function
        2. The patch policy associated with this patch (may be `None`)
    The `patch_builder` may accept additional positional arguments that are passed to
    this function as a tuple via `builder_args`.

    The `patch_builder` function must return a function that matches the argument
    signature of the original function. The returned function must call the original
    function and return the result.

    Not all patches will have policy. Some patch locations are used solely to apply
    proxies or do library analysis, and so no policy exists for those locations.
    Callers can indicate this by passing "" or None for `loc_name`, in which case no
    patch policy will be retrieved.
    """
    original_func = getattr(owner, attr_name)

    # In most cases, we don't want to patch a function that has already been patched.
    # Sometimes we do, though, so we have a `force` flag to allow it.
    # An examples of when we might want to force a patch is applying automatic
    # CommonMiddlewarePatch with route coverage patches.
    if patch_manager.is_patched(original_func) and not force:
        return

    from contrast.agent.policy import registry

    loc_name = owner_name if owner_name is not None else get_name(owner)

    patch_policy = (
        registry.get_policy_by_name(f"{loc_name}.{attr_name}") if loc_name else None
    )

    patch = patch_builder(original_func, patch_policy, *(builder_args or ()))

    patch_manager.patch(owner, attr_name, patch)

    func = add_watermark(patch_manager.as_func(getattr(owner, attr_name)))
    if hasattr(func, "__name__") and not isinstance(func, wrapt.FunctionWrapper):
        func.__name__ = ensure_string(attr_name)


def get_loaded_modules(use_for_patching=False):
    """
    Retrieves and filters all loaded modules

    The parameter `use_for_patching` indicates that this function is being
    called to enable patching. In this case the modules are sorted to
    provide deterministic behavior, and .so modules are filtered out.
    Without `use_for_patching`, a simple, unsorted dict is returned.

    NOTE: This method gets called multiple times during the course of agent
    initialization. Ideally it would be called only once for PERF optimization,
    but because sys.modules is global to all threads, we can't guarantee its contents
    will be the same and that a race condition won't happen which would add modules
    across different threads.

    :return: dict of name and module as value
    """
    if not use_for_patching:
        # Have to make a copy of sys.modules in order to avoid RuntimeError: dictionary changed size during iteration
        return {k: v for k, v in dict(sys.modules).items() if inspect.ismodule(v)}

    filtered = OrderedDict()
    filtered.update(
        {
            name: module
            for name, module in sorted(sys.modules.items())
            if inspect.ismodule(module) and not is_so_module(module)
        }
    )

    return filtered


def is_so_module(module):
    """
    Return True if module is an .so file, such as
    ".../readline.cpython-38-darwin.so"

    :param module: python module object
    :return: bool
    """
    if not hasattr(module, "__file__") or module.__file__ is None:
        return False

    return module.__file__.endswith(".so")


def is_patchable(obj):
    if inspect.ismodule(obj):
        return False
    if inspect.isclass(obj):
        return True
    if type(obj) is functools.partial:
        return True

    # cython methods look like unpatchable builtins, but they can be patched normally
    # an example of this is lxml.etree.fromstring
    # for additional info, see https://groups.google.com/forum/#!topic/cython-users/v5dXFOu-DNc
    is_unpatchable_builtin_method = inspect.ismethoddescriptor(
        obj
    ) and not obj.__class__.__name__.startswith("cython")

    return inspect.isroutine(obj) and not is_unpatchable_builtin_method


@fail_quietly("Unable to repatch single module")
def repatch_module(module):
    """Repatch a single module. See docstring for repatch_imported_modules"""

    module_attrs = list(vars(module).items())

    for attr_name, attr in module_attrs:
        try:
            if not is_patchable(attr):
                continue
        except Exception as e:
            if (
                module.__name__.startswith("django")
                and type(e).__name__ == "ImproperlyConfigured"
            ):
                # Django gives ImproperlyConfigured if present in the env but unused.
                # This is not an issue, but can lead to noisy logging.
                continue
            logger.debug(
                "exception occurred while checking whether to patch %s in %s",
                attr_name,
                module.__name__,
                exc_info=e,
            )
            continue

        if type(attr) is functools.partial and (
            orig_patch := patch_manager.get_patch(attr.func)
        ):
            patch = functools.partial(orig_patch, *attr.args, **attr.keywords)
        else:
            patch = patch_manager.get_patch(patch_manager.as_func(attr))

        if patch:
            logger.debug("applying repatch to %s in %s", attr_name, module.__name__)
            patch_manager.patch(module, attr_name, patch)


@fail_quietly("Unable to patch previously imported modules")
def repatch_imported_modules():
    """
    Applies patches to modules that were already imported prior to agent startup

    Here's the problem: our patches don't get applied until after our
    middleware class is initialized. At this point it's likely that most (or
    all) application modules will have already been imported.

    If we patch the function `foo.bar.baz`, and an application module that was
    loaded prior to our patches imports it as `from foo.bar import baz`, then
    our patch will have no effect within that application module. This is
    because the application module has a reference to the *original* function,
    and that reference remains unchanged even after we apply a patch to the
    `foo.bar` module.

    On the other hand, if the application imports it as `from foo import bar`
    and uses it as `bar.baz()`, then our patches will work just fine. In this
    case, the application module has a reference to the *module itself*, which
    is where we apply our patch. This means that when the application calls
    `bar.baz()`, it will be calling the updated (patched) function.

    Incidentally, if the application imports as `from foo.bar import baz`, but
    this module is not loaded until *after* our patches have been applied, our
    patch will be effective. However, we have no control over the order of
    imports in an application.

    This function is designed to remedy the former case in order to make sure
    that our patches are effective regardless of how they are imported or the
    order in which they are imported by the application.

    Prior to calling this function, we make a record of every function that
    gets patched. After all patches are applied, this function iterates
    through all imported modules, which includes all modules that may have been
    imported before our patches were applied. We look for any instances of the
    original functions that need to be patched, and we replace them with the
    patches in those modules.
    """
    for module in get_loaded_modules(use_for_patching=True).values():
        repatch_module(module)
