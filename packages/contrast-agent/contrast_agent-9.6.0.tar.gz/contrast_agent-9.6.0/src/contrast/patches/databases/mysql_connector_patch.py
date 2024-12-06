# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast_vendor.wrapt import register_post_import_hook
import sys
from contrast.agent.policy import patch_manager
from contrast.patches.databases import dbapi2

MYSQL_CONNECTOR = "mysql.connector"
VENDOR = "MySQL"


def instrument_mysql_connector(mysql_connector):
    extra_cursors = [
        mysql_connector.cursor.MySQLCursor,
    ]

    # CursorBase is a base class for MySQLCursor prior to 9.0.0,
    # when it was removed.
    if cb := getattr(mysql_connector.cursor, "CursorBase", None):
        extra_cursors.append(cb)

    try:
        # The C extension is technically optional
        extra_cursors.append(mysql_connector.cursor_cext.CMySQLCursor)
    except AttributeError:
        pass

    dbapi2.instrument_adapter(
        mysql_connector,
        VENDOR,
        dbapi2.Dbapi2Patcher,
        extra_cursors=extra_cursors,
    )


def register_patches():
    register_post_import_hook(instrument_mysql_connector, MYSQL_CONNECTOR)


def reverse_patches():
    if mysql_connector := sys.modules.get(MYSQL_CONNECTOR):
        patch_manager.reverse_patches_by_owner(mysql_connector)
        patch_manager.reverse_patches_by_owner(
            mysql_connector.connection_cext.CMySQLConnection
        )
        if cb := getattr(mysql_connector.cursor, "CursorBase", None):
            patch_manager.reverse_patches_by_owner(cb)
        patch_manager.reverse_patches_by_owner(mysql_connector.cursor.MySQLCursor)
        patch_manager.reverse_patches_by_owner(mysql_connector.cursor_cext.CMySQLCursor)
