# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.api import TypeCheckedProperty
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

DATABASE_TYPE = "db"


class ArchitectureComponent:
    vendor = TypeCheckedProperty(str)
    url = TypeCheckedProperty(str)

    def __init__(self, vendor: str, db_name: str):
        self.vendor = vendor
        self.url = db_name or vendor or "default"

    def to_json(self):
        json = {
            "type": DATABASE_TYPE,
            "url": self.url,
        }

        # vendor must be a string that exactly matches a value from
        # Teamserver's flowmap/technologies.json > service > one of "name"
        if self.vendor:
            json["vendor"] = self.vendor

        return json
