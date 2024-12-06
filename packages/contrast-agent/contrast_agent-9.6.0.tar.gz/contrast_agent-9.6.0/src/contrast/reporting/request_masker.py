# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from copy import copy
from typing import List, TypedDict
from urllib.parse import parse_qs, urlencode, unquote
from collections.abc import Mapping

from contrast.api.attack import ProtectResponse
from contrast_vendor import structlog as logging
from contrast_vendor.webob.multidict import MultiDict

logger = logging.getLogger("contrast")

MASK = "contrast-redacted-{}"
BODY_MASK = b"contrast-redacted-body"
SEMICOLON_URL_ENCODE_VAL = "%25"


class SensitiveDataRule(TypedDict):
    id: str
    keywords: List[str]


class SensitiveDataPolicy(TypedDict):
    mask_attack_vector: bool
    mask_http_body: bool
    rules: List[SensitiveDataRule]


class RequestMasker:
    def __init__(self, config: Mapping):
        self.request = None
        self.attacks = None
        self.mask_rules: SensitiveDataPolicy = config.get(
            "application.sensitive_data_masking_policy", None
        )

    @classmethod
    def new_request_masker(cls, config: SensitiveDataPolicy):
        return cls({"application.sensitive_data_masking_policy": config})

    def mask_sensitive_data(self, request, attacks=None):
        if not request or not self.mask_rules:
            return

        self.request = request
        self.attacks = attacks or []

        logger.debug("Masker: masking sensitive data")

        self._mask_body()
        self._mask_query_string()
        self._mask_request_params()
        self._mask_request_cookies()
        self._mask_request_headers()

        request._masked = True

    def _mask_body(self):
        # Check if mask_http_body is set to False or is None and skip if true
        if not self.mask_rules.get("mask_http_body"):
            return

        # Checks if body is not empty or null
        if self.request.body:
            self.request._masked_body = BODY_MASK

    def _mask_query_string(self):
        if self.request.query_string:
            self.request._masked_query_string = self._mask_raw_query(
                self.request.query_string
            )

    def _mask_raw_query(self, query_string):
        qs_dict = parse_qs(query_string)
        masked_qs_dict = self._mask_dictionary(qs_dict)
        return urlencode(masked_qs_dict, doseq=True)

    def _mask_request_params(self):
        try:
            params = self.request.params
        except ValueError as e:
            # This likely came form a malformed multipart/form-data request,
            # which is out of our control. Still log the error in case
            # there's another case we haven't considered.
            logger.debug("WARNING: failed to parse params", error=e)
            # set the _masked_params to avoid raising the same error
            # in reportable_request.
            self.request._masked_params = {}
            return
        if not params:
            return

        self.request._masked_params = self._mask_dictionary(params)

    def _mask_request_cookies(self):
        cookies = self.request.cookies
        if not cookies:
            return

        self.request._masked_cookies = self._mask_dictionary(cookies)

    def _mask_request_headers(self):
        headers = self.request.headers
        if not headers:
            return

        self.request._masked_headers = self._mask_dictionary(headers)

    def _mask_dictionary(self, d):
        if not d:
            return d

        if isinstance(d, MultiDict):
            d = d.mixed()

        d_copy = {k: copy(v) for k, v in d.items()}

        for k, v in d_copy.items():
            if k is None or self._find_value_index_in_rules(k.lower()) == -1:
                continue

            if isinstance(v, list):
                self._mask_values(k, v, d_copy, self.attacks)
            else:
                self._mask_hash(k, v, d_copy, self.attacks)
        return d_copy

    def _mask_values(self, k, v, d, attacks):
        for idx, item in enumerate(v):
            if self.mask_rules.get("mask_attack_vector") and self._is_value_vector(
                attacks, item
            ):
                d[k][idx] = MASK.format(k.lower())
            if not self._is_value_vector(attacks, item):
                d[k][idx] = MASK.format(k.lower())

    def _mask_hash(self, k, v, d, attacks):
        if self.mask_rules.get("mask_attack_vector") and self._is_value_vector(
            attacks, v
        ):
            d[k] = MASK.format(k.lower())
        if not self._is_value_vector(attacks, v):
            d[k] = MASK.format(k.lower())

    def _is_value_vector(self, attacks, value):
        if not attacks or not value:
            return False

        for attack in attacks:
            if self._is_value_in_sample(attack.samples, value):
                return attack.response != ProtectResponse.NO_ACTION

        return False

    def _is_value_in_sample(self, samples, value):
        if not samples:
            return False

        # Setting this to remove url encoding of header and cookie values
        value = unquote(value)

        for sample in samples:
            if sample.user_input.value == value:
                return True
        return False

    def _find_value_index_in_rules(self, s):
        index = -1
        # When looking for header it replaces '_' with '-' and I don't want to risk not
        # properly matching to the rules
        s = s.replace("-", "_")
        for rule in self.mask_rules.get("rules"):
            try:
                index = rule.get("keywords").index(s)
                break
            except ValueError:
                index = -1

        return index
