#!/usr/bin/env python3
from strenum import StrEnum


class AutopilotTypes(StrEnum):
    PX4 = 'PX4'
    ArduPilot: str = 'ArduPilot'


class Devices(StrEnum):
    udp = 'udp'
    serial = 'serial'
