#!/usr/bin/env python3
import struct
from pymavlink import mavutil

from .enums import AutopilotTypes

PARAM_TYPE_TO_STRING = {
    mavutil.mavlink.MAV_PARAM_TYPE_UINT8: "UINT8",      # 1
    mavutil.mavlink.MAV_PARAM_TYPE_INT8: "INT8",        # 2
    mavutil.mavlink.MAV_PARAM_TYPE_INT16: "INT16",      # 4
    mavutil.mavlink.MAV_PARAM_TYPE_INT32: "INT32",      # 6
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32: "REAL32"     # 9
}


def float_to_integer(float_number):
    return struct.unpack('!I', struct.pack('!f', float_number))[0]


def integer_to_float(int_number):
    return struct.unpack('!f', struct.pack('!I', int_number))[0]


def param_value_to_type(param_value):
    if isinstance(param_value, int):
        return mavutil.mavlink.MAV_PARAM_TYPE_INT32
    return mavutil.mavlink.MAV_PARAM_TYPE_REAL32


def deserialize_param_value(autopilot, msg):
    param_name = msg.param_id
    param_type = PARAM_TYPE_TO_STRING[msg.param_type]
    if (msg.param_type == mavutil.mavlink.MAV_PARAM_TYPE_INT32 and
            autopilot == AutopilotTypes.PX4):
        param_value = float_to_integer(msg.param_value)
    elif (msg.param_type == mavutil.mavlink.MAV_PARAM_TYPE_INT32 and
          autopilot == AutopilotTypes.ArduPilot):
        param_value = int(msg.param_value)
    elif msg.param_type == mavutil.mavlink.MAV_PARAM_TYPE_INT8:
        param_value = int(msg.param_value)
    else:
        param_value = msg.param_value

    return param_name, param_type, param_value


def serialize_param_value(param_value):
    param_type = param_value_to_type(param_value)
    if isinstance(param_value, int):
        param_value = integer_to_float(param_value)
    return param_value, param_type
