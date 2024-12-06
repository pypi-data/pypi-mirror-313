# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from . import (
    cs_io,
    encodings_patch,
    re_patch,
    threading_patch,
    exec_and_eval,
    genshi_patch,
    lxml_patch,
    pathlib_patch,
    sys_patch,
    import_patch,
    cgi_patch,
    concurrent_futures_thread_patch,
    str_new,
    operator,
    os_patch,
)

from .databases import (
    mysql_connector_patch,
    pymysql_patch,
    psycopg2_patch,
    sqlalchemy_patch,
    sqlite3_patch,
)

from .frameworks import (
    bottle_patches,
    django_patches,
    drf_patches,
    falcon_patches,
    pyramid_patch,
    starlette_patches,
    flask_and_quart_patches,
)

from .middleware import django, mod_wsgi, aiohttp
from .middleware.common import CommonMiddlewarePatch, AppInterfaceType

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

COMMON_PATCH_MODULES = (
    pathlib_patch,
    sqlalchemy_patch,
    # our sqlite3_patch also contains the import hook for pysqlite2.dbapi2
    sqlite3_patch,
    mysql_connector_patch,
    pymysql_patch,
    psycopg2_patch,
    concurrent_futures_thread_patch,
)


LIBRARY_READER_PATCHES = (import_patch,)


ASSESS_PATCH_MODULES = (
    operator,
    threading_patch,
    cs_io,
    encodings_patch,
    re_patch,
    exec_and_eval,
    genshi_patch,
    lxml_patch,
    pyramid_patch,
    django_patches,
    drf_patches,
    bottle_patches,
    flask_and_quart_patches,
    falcon_patches,
    sys_patch,
    import_patch,
    cgi_patch,
    starlette_patches,
    str_new,
    os_patch,
)


MIDDLEWARE_PATCH_MODULES = (
    django,
    mod_wsgi,
    CommonMiddlewarePatch("flask"),
    CommonMiddlewarePatch("bottle"),
    CommonMiddlewarePatch(
        "pyramid.router",
        application_class_name="Router",
        framework_name="pyramid",
    ),
    CommonMiddlewarePatch(
        "fastapi",
        application_class_name="FastAPI",
        app_interface=AppInterfaceType.ASGI,
    ),
    aiohttp,
    CommonMiddlewarePatch(
        "falcon",
        application_class_name="App",
        framework_name="falcon",
        app_interface=AppInterfaceType.AUTO_DETECT,
    ),
    # NOTE: falcon.asgi.App is a subclass of falcon.App. Because of this, registering
    # this patch can cause multiple middleware initializations - for this case, it
    # doesn't cause any issues. We still need this patch, since the two classes do not
    # share any code for `__call__` (only for `__init__`)
    CommonMiddlewarePatch(
        "falcon.asgi",
        application_class_name="App",
        framework_name="falcon",
        app_interface=AppInterfaceType.ASGI,
    ),
    CommonMiddlewarePatch("quart", app_interface=AppInterfaceType.ASGI),
)


def register_module_patches(module, patch_group):
    logger.debug("registering %s patches for %s", patch_group, module.__name__)

    try:
        module.register_patches()
    except Exception:
        logger.exception("failed to register patches for %s", module.__name__)


def register_library_patches():
    for module in LIBRARY_READER_PATCHES:
        register_module_patches(module, "library analysis")


def register_common_patches():
    for module in COMMON_PATCH_MODULES:
        register_module_patches(module, "common")


def register_assess_patches():
    for module in ASSESS_PATCH_MODULES:
        register_module_patches(module, "assess")


def register_middleware_patches():
    logger.debug("registering automatic middleware patches")
    for module in MIDDLEWARE_PATCH_MODULES:
        register_module_patches(module, "middleware")
