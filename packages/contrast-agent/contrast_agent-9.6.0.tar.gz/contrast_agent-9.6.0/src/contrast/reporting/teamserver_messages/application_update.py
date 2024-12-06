# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import requests

from .base_ts_message import BaseTsAppMessage
from contrast.utils.decorators import fail_loudly
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class ApplicationUpdate(BaseTsAppMessage):
    def __init__(self, libraries):
        super().__init__()

        self.extra_headers["Content-Type"] = "application/json"

        # activity message sends "components" aka "architectures"
        # so we will not send the "components" field at this time.

        # field "timestamp" represents the amount of time that has passed
        # since the app settings were changed (not an actual timestamp).
        self.body = {
            "timestamp": self.since_last_update,
            "libraries": [
                lib.to_json(self.settings) for lib in libraries if lib.hash_code
            ],
        }

    @property
    def name(self):
        return "application-update"

    @property
    def path(self):
        return "update/application"

    @property
    def request_method(self):
        return requests.put

    @fail_loudly("Failed to process ApplicationUpdate response")
    def process_response(self, response, reporting_client):
        self.process_response_code(response, reporting_client)
