# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy import patch_manager
from contrast_vendor.wrapt import register_post_import_hook
import sys
from contrast.patches.databases import dbapi2

PYMYSQL = "pymysql"
VENDOR = "MySQL"


def instrument_pymysql(pymysql):
    dbapi2.instrument_adapter(
        pymysql, VENDOR, dbapi2.Dbapi2Patcher, extra_cursors=[pymysql.cursors.Cursor]
    )


def register_patches():
    register_post_import_hook(instrument_pymysql, PYMYSQL)


def reverse_patches():
    if pymysql := sys.modules.get(PYMYSQL):
        patch_manager.reverse_patches_by_owner(pymysql)
        patch_manager.reverse_patches_by_owner(pymysql.connections.Connection)
        patch_manager.reverse_patches_by_owner(pymysql.cursors.Cursor)
