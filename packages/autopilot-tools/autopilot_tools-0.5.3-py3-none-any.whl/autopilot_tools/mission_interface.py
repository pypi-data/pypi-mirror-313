#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Yuriy <1budsmoker1@gmail.com>

import time
import math
import logging
from functools import partial
from typing import List, Optional

from pymavlink.dialects.v20.ardupilotmega import \
    (MAVLink_mission_item_int_message, MAVLink_mission_count_message,
     MAV_MISSION_TYPE_FENCE, MAV_MISSION_TYPE_RALLY,
     MAV_MISSION_TYPE_MISSION,
     MAV_MISSION_ACCEPTED)

from autopilot_tools.mission_file.mission_file import Plan, MissionItem, ParamList
from autopilot_tools.mission_file.mission_result import MissionResult, StatusCode, StatusText
from autopilot_tools.exceptions import MavlinkTimeoutError
from autopilot_tools.utils import retry_command
from autopilot_tools.mavlink_interface import MavlinkInterface

logger = logging.getLogger(__name__)

class MissionInterface:
    def __init__(self, master) -> None:
        self.master = master

    def download_from_autopilot(self) -> List[MAVLink_mission_item_int_message]:
        def get_count() -> MAVLink_mission_count_message:
            self.master.mav.mission_request_list_send(
                self.master.target_system, self.master.target_component)
            return self.master.recv_match(type='MISSION_COUNT', blocking=True, timeout=1)

        count = retry_command(get_count)
        if count is None:
            raise MavlinkTimeoutError

        data = []
        i = 0
        while i < count.count:

            def get_mission_item() -> MAVLink_mission_item_int_message:
                self.master.mav.mission_request_int_send(
                    self.master.target_system, self.master.target_component, i)
                return self.master.recv_match(type='MISSION_ITEM_INT', blocking=True, timeout=1)

            data_item = retry_command(get_mission_item)
            if data_item is None:
                raise MavlinkTimeoutError

            if data_item.seq == i:
                i += 1
                data.append(data_item)
        self.master.mav.mission_ack_send(
            self.master.target_system, self.master.target_component, MAV_MISSION_ACCEPTED)
        return data

    def load_to_autopilot(self, path: str) -> StatusCode:
        mission_file = Plan(path)

        fence_items = mission_file.geofence.get_mission_item_representation()
        rally_points_length = mission_file.rally_points.get_mission_item_representation()
        mission_length = mission_file.mission.get_mission_item_representation()

        def send_mission_items(
                count: int, item_list: List[MissionItem], mission_type: int) -> StatusCode:
            self.master.mav.mission_count_send(
                self.master.target_system, self.master.target_component,
                count, mission_type
            )
            if not item_list:
                return StatusCode.EMPTY_MISSION_ITEM_LIST
            reached_last_item = False
            next_item = -1
            while not reached_last_item:
                res = self.master.recv_match(
                    type=['MISSION_REQUEST_INT', 'MISSION_REQUEST'], blocking=True, timeout=0.5)
                if res is None:
                    return StatusCode.MAVLINK_ERROR
                next_item = res.seq
                logger.debug(f"Sending {item_list[next_item]} with id {next_item}")

                to_send = item_list[next_item]

                params = ParamList(
                    *[x if x is not None else math.nan for x in to_send.params]
                )
                self.master.mav.mission_item_int_send(
                    self.master.target_system, self.master.target_component,
                    to_send.arguments.seq,
                    to_send.arguments.frame,
                    to_send.arguments.command,
                    to_send.arguments.current,
                    to_send.arguments.auto_continue,
                    params.param1,
                    params.param2,
                    params.param3,
                    params.param4,
                    params.x,
                    params.y,
                    params.z,
                    to_send.mission_type
                )

                if next_item == count - 1:
                    reached_last_item = True

            res = self.master.recv_match(type='MISSION_ACK', blocking=True, timeout=0.5)

            return StatusCode.OK if res is not None else StatusCode.MAVLINK_ERROR

        result = retry_command(
            partial(send_mission_items, *fence_items, MAV_MISSION_TYPE_FENCE),
            test=lambda x: x in [StatusCode.OK, StatusCode.EMPTY_MISSION_ITEM_LIST])
        if result is None:
            raise MavlinkTimeoutError

        result = retry_command(
            partial(send_mission_items, *rally_points_length, MAV_MISSION_TYPE_RALLY),
            test=lambda x: x in [StatusCode.OK, StatusCode.EMPTY_MISSION_ITEM_LIST])
        if result is None:
            raise MavlinkTimeoutError

        result = retry_command(
            partial(send_mission_items, *mission_length, MAV_MISSION_TYPE_MISSION),
            test=lambda x: x in [StatusCode.OK, StatusCode.EMPTY_MISSION_ITEM_LIST])
        if result is None:
            raise MavlinkTimeoutError
        logger.info('Mission upload complete')
        return StatusCode.OK

    def run(self, timeout: int = 100) -> MissionResult:
        logger.info("Extracting a mission from the autopilot...")
        items_amount = len(self.download_from_autopilot())
        logger.info(f"A mission consisting of {items_amount} items has been found.")

        self._wait_for_disarmed_heatbeat()

        logger.info("Starting the mission...")
        MavlinkInterface.mav_cmd_mission_start_full(self.master, items_amount)

        self._wait_for_armed_heatbeat()

        start_time = time.time()
        end_time = start_time + timeout
        messages = self._wait_until_the_end_of_mission(items_amount, end_time)

        time_taken = int(time.time() - start_time)
        status = StatusCode.OK if time_taken < timeout else StatusCode.MISSION_TIMEOUT
        return MissionResult(status, time_taken, items_amount, messages)

    def _wait_until_the_end_of_mission(self, items_amount, deadline) -> list:
        messages = []
        last_recv_time = time.time()
        time_left = int(deadline - time.time())
        logger.info(f"MISSION_CURRENT seq=0, total={items_amount}, {time_left} sec left...")

        while time.time() < deadline:
            FILTERED_MESSAGES = ['STATUSTEXT', 'HEARTBEAT', 'MISSION_CURRENT']
            msg = self.master.recv_match(type=FILTERED_MESSAGES, blocking=False)

            if time.time() > last_recv_time + 10.0:
                raise TimeoutError("Connection to the autopilot has been lost 10 seconds ago.")

            if msg is None:
                continue

            last_recv_time = time.time()

            if msg.get_type() == 'STATUSTEXT':
                messages.append(StatusText(msg.severity, msg.text))
                logger.info(f"STATUSTEXT: {msg.text}")
            elif msg.get_type() == 'HEARTBEAT':
                if MissionInterface.safety_armed_from_heartbeat(msg) is False:
                    logger.info("The mission has been finished.")
                    break
            elif msg.get_type() == 'MISSION_CURRENT':
                time_left = int(deadline - time.time())
                logger.info((
                    f"MISSION_CURRENT: "
                    f"seq={msg.seq}, "
                    f"total={items_amount}, "
                    f"{time_left} sec left."
                ))
            time.sleep(0.01)

        return messages

    def _wait_for_disarmed_heatbeat(self, timeout=5.0) -> None:
        logger.info("Waiting for the vehicle to be ready to start the mission...")
        is_safety_armed = self._recv_heartbeat_armed_flag(timeout=timeout)
        if is_safety_armed is None:
            raise TimeoutError("HEARTBEAT has not been received.")
        if is_safety_armed:
            raise RuntimeError("Can't start the mission because the vehicle is already armed.")

    def _wait_for_armed_heatbeat(self, timeout=5.0) -> None:
        logger.info("Waiting for the vehicle to be armed...")
        is_safety_armed = self._recv_heartbeat_armed_flag(timeout=timeout)
        if is_safety_armed is None:
            raise TimeoutError("HEARTBEAT has not been received.")
        if not is_safety_armed:
            raise RuntimeError("The vehicle couldn't start the mission. It is still disarmed.")

    def _recv_heartbeat_armed_flag(self, timeout=5.0) -> Optional[bool]:
        deadline = time.time() + timeout

        while time.time() < deadline:
            heartbeat = self.master.recv_match(type='HEARTBEAT', blocking=False)

            if heartbeat is None:
                continue

            return MissionInterface.safety_armed_from_heartbeat(heartbeat)

        return None

    @staticmethod
    def safety_armed_from_heartbeat(heartbeat) -> bool:
        is_safety_armed = bool(heartbeat.base_mode & 128)
        flag_safety_armed_text = "ARMED" if is_safety_armed else "DISARMED"
        logger.info(f'HEARTBEAT: {flag_safety_armed_text}')
        return is_safety_armed
