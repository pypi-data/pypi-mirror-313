#!/usr/bin/env python3
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List


class StatusCode(Enum):
    OK = auto()
    EMPTY_MISSION_ITEM_LIST = auto()
    MISSION_TIMEOUT = auto()
    MAVLINK_TIMEOUT = auto()
    MAVLINK_ERROR = auto()
    DID_NOT_REACH_TARGET = auto()


@dataclass
class StatusText:
    severity: int
    text: str


@dataclass
class MissionResult:
    status: StatusCode
    time_taken: int = field(default=0)
    mission_item_count: int = field(default=0)
    messages: List[StatusText] = field(default_factory=list)
    log_link: str = field(default='')
