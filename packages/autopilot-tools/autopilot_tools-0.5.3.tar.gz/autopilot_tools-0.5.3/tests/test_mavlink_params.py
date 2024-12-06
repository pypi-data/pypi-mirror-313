#!/usr/bin/env python3
import unittest
from collections import namedtuple
from autopilot_tools.mavlink_params import deserialize_param_value, \
                                           serialize_param_value, \
                                           integer_to_float
from autopilot_tools.enums import AutopilotTypes


MavlinkMessage = namedtuple('MavlinkMessage', 'param_id param_type param_value')


class TestMavlinkParams(unittest.TestCase):
    def test_deserialize_param_value_px4(self):
        test_case_int = MavlinkMessage('SYS_AUTOSTART', 6, 1.8216880036222622e-41)
        _, _, recv_param_value = deserialize_param_value(AutopilotTypes.PX4, test_case_int)
        self.assertEqual(recv_param_value, 13000)

        test_case_float = MavlinkMessage('CAL_GYRO0_XOFF', 9, 1.0)
        _, _, recv_param_value = deserialize_param_value(AutopilotTypes.PX4, test_case_float)
        self.assertEqual(recv_param_value, 1.0)

    def test_deserialize_param_value_ardupilot(self):
        test_case_int = MavlinkMessage('SCR_ENABLE,', 2, 1.0)
        _, _, recv_param_value = deserialize_param_value(AutopilotTypes.ArduPilot, test_case_int)
        self.assertEqual(recv_param_value, 1)

        test_case_int = MavlinkMessage('some_param,', 4, 42.0)
        _, _, recv_param_value = deserialize_param_value(AutopilotTypes.ArduPilot, test_case_int)
        self.assertEqual(recv_param_value, 42)

        test_case_int = MavlinkMessage('COMPASS_DEV_ID,', 6, 76291.0)
        _, _, recv_param_value = deserialize_param_value(AutopilotTypes.ArduPilot, test_case_int)
        self.assertEqual(recv_param_value, 76291)

        test_case_int = MavlinkMessage('COMPASS_DIA_X,', 9, 0.999)
        _, _, recv_param_value = deserialize_param_value(AutopilotTypes.ArduPilot, test_case_int)
        self.assertEqual(recv_param_value, 0.999)

    def test_serialize_param_value(self):
        self.assertEqual((1.8216880036222622e-41, 6), serialize_param_value(13000))
        self.assertEqual((1.0, 9), serialize_param_value(1.0))

    def test_integer_to_float(self):
        self.assertEqual(1.8216880036222622e-41, integer_to_float(13000))
        # self.assertEqual(-1.8216880036222622e-41, integer_to_float(-1))

if __name__ == '__main__':
    unittest.main()
