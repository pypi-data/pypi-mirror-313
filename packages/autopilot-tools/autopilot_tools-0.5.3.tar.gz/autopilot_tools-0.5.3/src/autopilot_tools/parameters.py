#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>

import sys
import time
import math
import logging
from typing import Union, Optional, Any
import yaml
from autopilot_tools.mavlink_interface import MavlinkInterface
from autopilot_tools.enums import AutopilotTypes
from autopilot_tools.mavlink_params import deserialize_param_value, float_to_integer

MAV_PARAM_TYPE_INT32 = 6

logger = logging.getLogger(__name__)


class ParametersInterface:
    def __init__(self, mav: MavlinkInterface, autopilot: AutopilotTypes) -> None:
        assert isinstance(mav, MavlinkInterface)
        assert isinstance(autopilot, AutopilotTypes)
        self.mav = mav
        self.autopilot = autopilot

    def set_multiple(self, params: dict) -> None:
        """
        Send a set request for a specific group of parameters.
        """
        assert isinstance(params, dict)

        logger.info(f"Trying to write {len(params)} params...")

        num_of_recv_params = 0

        for name, set_param_value in params.items():
            # Let's increase the timeout for the first message because it may require more time
            timeout = 1.0 if num_of_recv_params != 0 else 5.0
            if self._set(name, set_param_value, timeout):
                num_of_recv_params += 1

        if num_of_recv_params == len(params):
            logger.info("All %s params has been successfully configured.", num_of_recv_params)
        elif num_of_recv_params == 0:
            logger.error(f"Configuration failed: {num_of_recv_params}/{len(params)}.")
            sys.exit(1)
        else:
            logger.warning("Configuration has encountered a few problems: %s/%s.",
                           num_of_recv_params, len(params))

    def set(self, name: str, value: Union[float, int], timeout: float=1.0) -> bool:
        """
        Send a set request for a specific parameter.
        Return True in success, otherwise False.
        """
        assert isinstance(name, str)
        assert isinstance(value, (float, int))

        return self._set(name, value, timeout)

    def read_all(self) -> Optional[dict]:
        """
        Send param list request
        Return a dict with paramters
        """
        self.mav.param_request_list_send()

        params = {}
        deadline = time.time() + 1.0
        while deadline + 1.0 > time.time():
            time.sleep(0.01)
            recv_msg = self._recv_match_param_value()
            if recv_msg is not None:
                if recv_msg.param_type == MAV_PARAM_TYPE_INT32:
                    recv_msg.param_value = float_to_integer(recv_msg.param_value)
                recv_msg = recv_msg.to_dict()
                params[recv_msg['param_id']] = recv_msg['param_value']
                logger.info(f"name: {recv_msg['param_id']} value: {recv_msg['param_value']}")
                deadline = time.time() + 1.0

        logger.info("Done reading parameters")

        return params

    def read(self, name: str, attempts=100) -> None:
        """
        Non-blocking read of the specific parameter.
        Several attemps until fail.
        """
        assert isinstance(name, str)
        assert isinstance(attempts, int)

        logger.info(f"{name: <18}", end='', flush=True)

        recv_msg = None
        value = None
        for _ in range(attempts):
            self.mav.param_request_read_send(name)

            recv_msg = self._recv_match_param_value()
            if recv_msg is None:
                time.sleep(0.1)
                continue

            recv_param_name, param_type, value = deserialize_param_value(self.autopilot, recv_msg)
            if recv_param_name == name:
                logger.info(f"{param_type: <6} {value}")
                break

        if recv_msg is None:
            logger.warning(f'Reading {name} failed {attempts} times.')
        return value

    def reset_to_default(self) -> None:
        self.mav.command_long_send_reset_params_to_default()

    def force_calibrate(self) -> None:
        self.mav.command_long_send_force_calibrate()

    @staticmethod
    def yaml_to_dict(path_to_yaml_file: str) -> Optional[dict]:
        assert isinstance(path_to_yaml_file, str)

        with open(path_to_yaml_file, encoding='UTF-8') as file_descriptor:
            params = yaml.load(file_descriptor, Loader=yaml.FullLoader)

        logger.info(f"{path_to_yaml_file} has : {params}")

        return params

    def _set(self, name: str, value: Union[float, int], timeout: float=1.0) -> bool:
        DELAY_NO_RESPONSE = 0.1
        DELAY_BUSY = 0.02

        start_time = time.time()
        deadline = start_time + timeout

        logger.info(f'Request {name}:={value}')
        self.mav.param_set_send(name, value)
        time.sleep(DELAY_BUSY)

        while time.time() < deadline:
            recv_msg = self._recv_match_param_value()
            if recv_msg is None:
                logger.info(('Recv None, '
                             f'then request {name}:={value} and wait {DELAY_NO_RESPONSE} sec.'))
                self.mav.param_set_send(name, value)
                time.sleep(DELAY_NO_RESPONSE)
                continue

            recv_name, recv_type, recv_value = deserialize_param_value(self.autopilot, recv_msg)
            if recv_name != name:
                logger.info((f'Recv {recv_name} but expected {name}, '
                            f'then wait {DELAY_BUSY} sec.'))
                time.sleep(DELAY_BUSY)
                continue

            if math.isclose(recv_value, value, rel_tol=1e-4):
                elapsed = time.time() - start_time
                logger.info(f"Recv {recv_name: <18} {recv_type: <6} {recv_value} {elapsed:.3} s.")
                return True

            logger.error(f'{name}: expected {value}, received {recv_value}.')
            return False

        logger.warning(f'Writing {name} failed. Timeout ({timeout} sec).')
        return False

    def _recv_match_param_value(self, timeout: Optional[float] = None) -> Any:
        if timeout is not None:
            return self.mav.recv_match(recv_type='PARAM_VALUE', blocking=True, timeout=timeout)

        return self.mav.recv_match(recv_type='PARAM_VALUE', blocking=False)
