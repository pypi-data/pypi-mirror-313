# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from enum import Enum, auto

from contrast.api import TypeCheckedProperty


class DocumentType(Enum):
    NORMAL = auto()
    JSON = auto()
    XML = auto()


# This is an exact representation of TS InputType. Not all are currently used, since we
# have to map from agent-lib's own input type to this enum.
class InputType(Enum):
    COOKIE_NAME = auto()
    COOKIE_VALUE = auto()
    HEADER = auto()
    PARAMETER_NAME = auto()
    PARAMETER_VALUE = auto()
    QUERYSTRING = auto()
    URI = auto()
    SOCKET = auto()
    JSON_VALUE = auto()
    JSON_ARRAYED_VALUE = auto()
    MULTIPART_CONTENT_TYPE = auto()
    MULTIPART_VALUE = auto()
    MULTIPART_FIELD_NAME = auto()
    MULTIPART_NAME = auto()
    XML_VALUE = auto()
    DWR_VALUE = auto()
    UNKNOWN = auto()
    METHOD = auto()
    REQUEST = auto()
    URL_PARAMETER = auto()

    def cef_string(self, key: str):
        fmt = _CEF_FMT_FROM_INPUT_TYPE.get(self, "untrusted input")
        return fmt.format(key) if fmt.endswith("{}") else fmt


_CEF_FMT_FROM_INPUT_TYPE = {
    InputType.COOKIE_NAME: "cookie {}",
    InputType.COOKIE_VALUE: "cookie {}",
    InputType.HEADER: "header {}",
    InputType.PARAMETER_NAME: "parameter {}",
    InputType.PARAMETER_VALUE: "parameter {}",
    InputType.QUERYSTRING: "querystring",
    InputType.URI: "URI",
    InputType.SOCKET: "socket",
    InputType.JSON_VALUE: "JSON value {}",
    InputType.JSON_ARRAYED_VALUE: "JSON array value {}",
    InputType.MULTIPART_CONTENT_TYPE: "content-type of the multipart {}",
    InputType.MULTIPART_VALUE: "value of the multipart {}",
    InputType.MULTIPART_FIELD_NAME: "multipart field name {}",
    InputType.MULTIPART_NAME: "name of the multipart {}",
    InputType.XML_VALUE: "XML value {}",
    InputType.DWR_VALUE: "DWR parameter {}",
    InputType.METHOD: "method {}",
    InputType.REQUEST: "HTTP request",
    InputType.UNKNOWN: "untrusted input",
}


class UserInput:
    input_type = TypeCheckedProperty(InputType, constructor_arg=InputType.UNKNOWN)
    key = TypeCheckedProperty(str)
    value = TypeCheckedProperty(str)
    path = TypeCheckedProperty(str)
    matcher_ids = TypeCheckedProperty(list)
    document_type = TypeCheckedProperty(
        DocumentType, constructor_arg=DocumentType.NORMAL
    )

    def __init__(
        self, input_type, key, value, path="", matcher_ids=None, document_type=None
    ):
        self.input_type = input_type
        self.key = key
        self.value = value
        self.path = path
        self.matcher_ids = [] if matcher_ids is None else matcher_ids

        self.document_type = (
            DocumentType.NORMAL if document_type is None else document_type
        )
