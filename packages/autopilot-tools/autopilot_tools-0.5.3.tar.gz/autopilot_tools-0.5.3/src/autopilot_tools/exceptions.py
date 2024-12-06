#!/usr/bin/env python3
from typing import Any


class NoSessionsAvailable(Exception):
    def __str__(self):
        return "No more sessions available"


class UnknownError(Exception):
    data: Any = None

    def __init__(self, data: Any):
        Exception.__init__(self, data)
        self.data = data

    def __str__(self):
        return \
            f"An unknown error occurred, " \
            f"find more info in this failed message {str(self.data)}"


class MavlinkTimeoutError(Exception):
    def __str__(self):
        return "Timed out while waiting for Mavlink message"
