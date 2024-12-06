# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from typing import Dict, List, Optional
from contrast.agent.assess.rules.base_rule import BaseRule
from contrast.utils.timer import now_ms
from contrast_fireball import AssessEvent, AssessFinding, AssessRequest


CURRENT_FINDING_VERSION = 4


def build_finding(
    rule: BaseRule,
    properties: Dict[str, str],
    events: Optional[List[AssessEvent]] = None,
    request: Optional[AssessRequest] = None,
    **kwargs,
) -> AssessFinding:
    """
    Builds a finding for the given rule. Properties are expected when the rule
    is a configuration or response scanning rule. Events are expected for
    dataflow rules. Request is expected for dataflow and response scanning rules.
    These expectations are from TeamServer, not checked in this function.
    """
    from contrast.agent import agent_state

    if events:
        kwargs.update(events=events)
    if request:
        kwargs.update(request=request)

    return AssessFinding(
        version=CURRENT_FINDING_VERSION,
        events=events or [],
        properties=properties,
        routes=[],
        rule_id=rule.name,
        tags=agent_state.module.assess_tags,
        request=request,
        evidence=None,
        hash=int(rule.generate_preflight_hash(**kwargs)),
        created=events[-1].time if events else now_ms(),
    )


def send_finding(finding: AssessFinding, context=None):
    """
    Send a finding by either appending it to request context
    OR sending it immediately.

    If `context` exists, agent should not sent message immediately because
    current route needs to be appended in `append_route_to_findings`

    :param finding:  api.Finding instance
    :param context: Request context instance
    :return: None
    """
    if context:
        if (
            context.input_exclusions_trigger_time
            and context.exclusions.evaluate_assess_trigger_time_exclusions(
                context, finding
            )
        ):
            return

        context.findings.append(finding)
        return

    from contrast.reporting import teamserver_messages
    from contrast.agent import agent_state

    agent_state.module.reporting_client.add_message(
        teamserver_messages.Preflight([finding], None)
    )
