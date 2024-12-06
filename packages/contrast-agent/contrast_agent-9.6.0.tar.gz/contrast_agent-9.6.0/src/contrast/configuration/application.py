# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from .config_builder import ConfigBuilder
from .config_option import ConfigOption
from contrast import AGENT_CURR_WORKING_DIR
import os


class Application(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="application.code", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.group", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.sensitive_data_masking_policy",
                default_value=None,
                type_cast=dict,
            ),
            ConfigOption(
                canonical_name="application.input_exclusions",
                default_value=[],
                type_cast=list,
            ),
            ConfigOption(
                canonical_name="application.metadata", default_value="", type_cast=str
            ),
            ConfigOption(
                # TODO: PYT-2852 Revisit application name detection
                canonical_name="application.name",
                default_value=os.path.basename(AGENT_CURR_WORKING_DIR),
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="application.path", default_value="/", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.tags", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.version", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.session_id", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.session_metadata",
                default_value="",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="application.url_exclusions",
                default_value=[],
                type_cast=list,
            ),
        ]
