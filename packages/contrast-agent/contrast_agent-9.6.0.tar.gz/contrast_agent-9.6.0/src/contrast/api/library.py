# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import time
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class Library:
    def __init__(self, data):
        self.current_time = int(time.time() * 1000)

        self.version = data["version"]
        self.class_count = data["class_count"]
        self.file_path = data["file_path"]
        self.url = data["url"]
        self.hash_code = data["hash_code"]

    def to_json(self, settings):
        return {
            "classCount": self.class_count,
            "file": self.file_path,
            "hash": self.hash_code,
            "url": self.url,
            "version": self.version,
            "externalDate": self.current_time,
            "internalDate": self.current_time,
            "tags": settings.config.get("inventory.tags"),
        }
