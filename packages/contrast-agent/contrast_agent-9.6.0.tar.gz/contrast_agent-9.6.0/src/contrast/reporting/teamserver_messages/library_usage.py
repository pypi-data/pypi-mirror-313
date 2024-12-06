# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import requests

from .base_ts_message import BaseTsAppMessage
from contrast.utils.decorators import fail_loudly
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class LibraryUsage(BaseTsAppMessage):
    def __init__(self, observed_libraries=None):
        # This message does not need "Application-Path" header but it doesn't hurt
        # either.
        super().__init__()

        self.base_url = f"{self.settings.api_url}/agents/v1.0/"
        self.body = {"observations": []}

        if observed_libraries is None:
            return
        for lib in observed_libraries:
            if len(lib.get("used_files")) > 0:
                message = {
                    "id": lib.get("hash_code"),
                    "names": list(lib.get("used_files")),
                }

                self.body["observations"].append(message)

    @property
    def name(self):
        return "library-usage"

    @property
    def path(self):
        return "/".join(
            [
                "applications",
                self.server_name_b64,
                self.server_path_b64,
                self.server_type_b64,
                self.app_language_b64,
                self.app_name_b64,
                "library-usage",
            ]
        )

    @property
    def request_method(self):
        return requests.post

    @fail_loudly("Failed to process LibraryUsage response")
    def process_response(self, response, reporting_client):
        self.process_response_code(response, reporting_client)
