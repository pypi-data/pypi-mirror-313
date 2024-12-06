#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>

from typing import Union, Any
from pymavlink import mavutil
from pymavlink.mavutil import mavfile
from autopilot_tools.mavlink_params import serialize_param_value

class MavlinkInterface:
    def __init__(self, master: mavfile) -> None:
        self.master = master

    def recv_match(self, recv_type: str, blocking: bool, timeout=None) -> Any:
        assert isinstance(recv_type, str)
        assert isinstance(blocking, bool)

        return self.master.recv_match(type=recv_type, blocking=blocking, timeout=timeout)

    def param_request_list_send(self) -> None:
        self.master.mav.param_request_list_send(
            self.master.target_system,
            self.master.target_component
        )

    def param_request_read_send(self, param_name) -> None:
        self.master.mav.param_request_read_send(
            self.master.target_system,
            self.master.target_component,
            bytes(param_name, 'utf-8'),
            -1
        )

    def param_set_send(self, param_name: str, param_value: Union[float, int]) -> None:
        self.master.mav.param_set_send(
            self.master.target_system,
            self.master.target_component,
            bytes(param_name, 'utf-8'),
            *serialize_param_value(param_value)
        )

    def command_long_send_reset_params_to_default(self) -> None:
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_PREFLIGHT_STORAGE,
            0,
            2, -1, 0, 0, 0, 0, 0
        )

    def command_long_send_force_calibrate(self) -> None:
        param2 = 76
        param5 = 76
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION,
            0,
            0, param2, 0, 0, param5, 0, 0
        )

    @staticmethod
    def mav_cmd_mission_start_full(master, mission_len: int) -> None:
        """
        first_item: the first mission item to run
        the last mission item to run (after this item is run, the mission ends)
        """
        MavlinkInterface.mav_cmd_mission_start(master, 0, mission_len - 1)

    @staticmethod
    def mav_cmd_mission_start(master, first_item, last_item) -> None:
        """
        first_item: the first mission item to run
        the last mission item to run (after this item is run, the mission ends)
        """
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_MISSION_START,
            0,
            first_item,
            last_item,
            0, 0, 0, 0, 0
        )
