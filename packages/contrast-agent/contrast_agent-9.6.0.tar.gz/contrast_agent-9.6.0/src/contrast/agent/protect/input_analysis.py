# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast

import xml.etree.ElementTree
from xml.etree.ElementTree import ParseError

from contrast.api.user_input import DocumentType, InputType
from contrast.agent.settings import Settings
from contrast.agent.agent_lib import input_tracing
from contrast_vendor import structlog as logging
from contrast.utils.decorators import fail_quietly
from contrast_agent_lib import constants

logger = logging.getLogger("contrast")


def _get_enabled_rules():
    """
    This converts our list of enabled rules to an integer value as the bitmask that the
    Agent Library expects.
    """
    rules = 0
    settings = Settings()

    for rule_tuple in settings.protect_rules.items():
        if (
            rule_tuple
            and rule_tuple[1]
            and rule_tuple[1].enabled
            and rule_tuple[1].RULE_NAME in constants.RuleType
        ):
            rules |= constants.RuleType[rule_tuple[1].RULE_NAME]
    return rules


def analyze_inputs():
    """
    Perform input analysis through agent-lib. Results are stored on
    context.user_input_analysis, which is reset every time this function is called.

    Some rules have a special "worth watching" analysis mode. In prefilter, we use this
    more liberal mode to ensure we don't miss attacks that should be blocked at trigger
    time. However, if we make it to the end of the request (without raising a
    SecurityException), we redo input analysis with worth watching mode disabled, which
    leads to more accurate PROBED results (fewer PROBED FPs).
    """
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None:
        return

    context.user_input_analysis = []

    rules = _get_enabled_rules()

    # Input analysis for all the input_tracing.InputType enum values
    _evaluate_headers(context, rules)
    _evaluate_cookies(context, rules)
    _evaluate_body(context, rules)
    _call_check_method_tampering(context)
    _evaluate_query_string_params(context, rules)
    _call_agent_lib_evaluate_input(
        constants.InputType.get("UriPath"),
        context.request.path,
        rules,
        context,
    )
    _evaluate_path_params(context, rules)
    _evaluate_multipart_request(context, rules)


def _evaluate_headers(context, rules):
    for header_name, header_value in context.request.headers.items():
        if "cookie" in header_name.lower() or check_param_input_exclusions(
            context.exclusions, "HEADER", header_name
        ):
            continue

        input_analysis = input_tracing.evaluate_header_input(
            header_name,
            header_value,
            rules,
            prefer_worth_watching=True,
        )

        if input_analysis:
            context.user_input_analysis.extend(input_analysis)
            # Report and block attack if necessary
            _report_and_block_by_rule_list(
                input_analysis,
                ["bot-blocker", "reflected-xss", "unsafe-file-upload"],
                context,
            )


def _evaluate_cookies(context, rules):
    for cookie_name, cookie_value in context.request.cookies.items():
        if check_param_input_exclusions(context.exclusions, "COOKIE", cookie_name):
            continue

        _call_agent_lib_evaluate_input(
            constants.InputType.get("CookieName"),
            cookie_name,
            rules,
            context,
        )
        _call_agent_lib_evaluate_input(
            constants.InputType.get("CookieValue"),
            cookie_value,
            rules,
            context,
        )


@fail_quietly("Failed to evaluate body")
def _evaluate_body(context, rules):
    if check_url_input_exclusion(context.exclusions, "BODY", context.request.url):
        return

    body_type = context.request._get_document_type()
    if body_type == DocumentType.JSON:
        _evaluate_body_json(context, rules, context.request.json)
    elif body_type == DocumentType.XML:
        try:
            data = xml.etree.ElementTree.fromstring(context.request.body)
        except ParseError as e:
            logger.debug("WARNING: Failed to parse XML in response body", exc_info=e)
            return

        text_list = [element.text for element in data]

        for text in text_list:
            if not str(text).startswith("\n"):
                _call_agent_lib_evaluate_input(
                    constants.InputType.get("XmlValue"),
                    str(text),
                    rules,
                    context,
                )
    else:
        _evaluate_key_value_parameters(context, rules, querystring=False)


def _evaluate_body_json(context, rules, body):
    # Using recursion for now to get all the json values and keys and pass them
    # through agent_lib until agent_lib implements parsing of the body for python
    if isinstance(body, dict):
        for key, value in body.items():
            _call_agent_lib_evaluate_input(
                constants.InputType.get("JsonKey"),
                key,
                rules,
                context,
            )
            # This check is to skip a level in the recursion, just a minor optimization
            if isinstance(value, (dict, list)):
                _evaluate_body_json(context, rules, value)
            else:
                _call_agent_lib_evaluate_input(
                    constants.InputType.get("JsonValue"),
                    value,
                    rules,
                    context,
                )
    elif isinstance(body, list):
        for item in body:
            if isinstance(item, (dict, list)):
                _evaluate_body_json(context, rules, item)
            else:
                _call_agent_lib_evaluate_input(
                    constants.InputType.get("JsonValue"),
                    item,
                    rules,
                    context,
                )
    else:
        # In theory we shouldn't enter this block but I would like to have it
        # just in case we get a value instead of dict
        _call_agent_lib_evaluate_input(
            constants.InputType.get("JsonValue"),
            body,
            rules,
            context,
        )


def _evaluate_query_string_params(context, rules):
    """
    Get agent-lib input analysis for all query parameters. This information is stored on
    request context.
    """
    if check_url_input_exclusion(
        context.exclusions, "QUERYSTRING", context.request.url
    ):
        return

    _evaluate_key_value_parameters(context, rules, querystring=True)


def _evaluate_key_value_parameters(context, rules, *, querystring: bool) -> None:
    """
    Used for both form parameters (from the request body) and query string parameters
    """
    if querystring:
        param_dict = context.request.GET
    else:
        param_dict = context.request.POST

    for param_key, param_value in param_dict.items():
        if not isinstance(param_value, str):
            continue

        _call_agent_lib_evaluate_input(
            constants.InputType.get("ParameterKey"),
            param_key,
            rules,
            context,
            is_querystring=querystring,
        )
        _call_agent_lib_evaluate_input(
            constants.InputType.get("ParameterValue"),
            param_value,
            rules,
            context,
            is_querystring=querystring,
        )


def _evaluate_path_params(context, rules):
    """
    Get agent-lib input analysis for all path parameters. This information is
    stored on request context.
    """
    for param in context.request.get_url_parameters():
        if check_param_input_exclusions(context.exclusions, "PARAMETER", param):
            continue

        _call_agent_lib_evaluate_input(
            constants.InputType.get("UrlParameter"),
            param,
            rules,
            context,
        )


def _evaluate_multipart_request(context, rules):
    """
    This is refering to Content-Type: multipart/form-data and checking the file_name for every
    multipart request if there is none it checks the name
    """
    for key, value in context.request.get_multipart_headers().items():
        if value is None and key is None:
            continue

        multipart_name = value if value is not None else key
        _call_agent_lib_evaluate_input(
            constants.InputType.get("MultipartName"),
            multipart_name,
            rules,
            context,
        )


def _call_check_method_tampering(context):
    input_analysis_value = input_tracing.check_method_tampering(
        context.request.method, prefer_worth_watching=True
    )

    if input_analysis_value:
        context.user_input_analysis.extend(input_analysis_value)
        _report_and_block_by_rule_list(
            input_analysis_value, ["reflected-xss", "unsafe-file-upload"], context
        )


def _call_agent_lib_evaluate_input(
    input_type,
    input_value,
    rule_set,
    context,
    *,
    is_querystring=False,
):
    input_analysis_value = input_tracing.evaluate_input_by_type(
        input_type, input_value, rule_set, prefer_worth_watching=True
    )

    if input_analysis_value:
        # This check is specific for querystring because agent-lib doesn't have a way to distinguish
        # url parameter and querystring and TS is expecting it as QUERYSTRING in attack samples
        if is_querystring:
            for input_analysis in input_analysis_value:
                input_analysis.input_type = InputType.QUERYSTRING

        context.user_input_analysis.extend(input_analysis_value)
        _report_and_block_by_rule_list(
            input_analysis_value, ["reflected-xss", "unsafe-file-upload"], context
        )


def _report_and_block_by_rule_list(input_analysis, rule_names, context):
    """
    Checks a list of rules and reports if it finds a score(int with value 0-100 indicating percentage
    of certainty of attack) higher than 90 and blocks if the agent is configured in block mode.
    :param input_analysis: list the response from agent_lib
    :param rule_names: list of names of rules that need to be checked and reported and blocked
    :return: doesn't return anything as it just needs to report and block if needed
    """
    settings = Settings()
    for input_row in input_analysis:
        for rule_name in rule_names:
            rule = settings.protect_rules.get(rule_name)

            # Bot blocker rule is valid only when the input_row.name/header name is "user-agent"
            def bot_blocker_header_check(a, rule_name_val):
                return (
                    a.lower() == "user-agent"
                    if rule_name_val == "bot-blocker"
                    else True
                )

            if rule_name == input_row.rule_id:
                attack = rule.build_attack_with_match(input_row.value, input_row, None)
                context.attacks.append(attack)

            if (
                bot_blocker_header_check(input_row.key, rule_name)
                and input_row.score >= 90
                and rule is not None
                and rule_name == input_row.rule_id
            ):
                logger.debug(
                    f"Input analysis found a value '{input_row.value}' "
                    f"that violated {rule_name} rule!"
                )

                if rule.is_blocked():
                    raise contrast.SecurityException(rule_name=rule_name)


def check_url_input_exclusion(exclusions, input_type, param):
    if not exclusions:
        return False

    return exclusions.evaluate_input_exclusions_url(
        exclusions, input_type, param, mode="defend"
    )


def check_param_input_exclusions(exclusions, input_type, param):
    if not exclusions:
        return False

    return exclusions.evaluate_input_exclusions(
        exclusions, input_type, param, mode="defend"
    )
