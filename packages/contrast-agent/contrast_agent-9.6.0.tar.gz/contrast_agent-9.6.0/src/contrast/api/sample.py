# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.utils.timer import now_ms


class Sample:
    def __init__(self):
        self.timestamp_ms = now_ms()
        self.user_input = None
        self.stack_trace_elements = []
        self.details = {}

    def set_stack(self, stack):
        self.stack_trace_elements = stack

    def set_user_input(self, user_input):
        self.user_input = user_input
