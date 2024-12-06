#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
# Author: Yuriy <1budsmoker1@gmail.com>
import logging
import os
import sys
import time
from io import BufferedIOBase
from typing import List, Union
import serial
from pymavlink import mavutil
from pymavlink.dialects.v20.ardupilotmega import \
    (MAVLink_mission_item_int_message, MAV_AUTOPILOT_ARDUPILOTMEGA,
     MAV_AUTOPILOT_PX4, enums)
from pymavlink.mavutil import mavlink

from autopilot_tools.utils import retry_command
from autopilot_tools.mavlink_interface import MavlinkInterface
from autopilot_tools.parameters import ParametersInterface
from autopilot_tools.mission_interface import MissionInterface

from .enums import AutopilotTypes, Devices

from .mission_file.mission_result import MissionResult, StatusCode
from .px4.px4_utils import upload_px4_log
from .mavlink_ftp.mavftputils import MavFTP

SOURCE_SYSTEM = 2
SOURCE_COMPONENT = 1
MAX_REQUESTED_SIZE = 90

logger = logging.getLogger(__name__)

class Vehicle:
    # pylint: disable=too-many-instance-attributes
    def __init__(self) -> None:
        self.device_path = None
        self.autopilot: AutopilotTypes = AutopilotTypes.PX4
        self.device: Devices = Devices.serial
        self.master = None
        self.mav_ftp = None
        self.mav = None
        self.params = None
        self.mission = None

    def connect(self, device: Devices = "serial"):
        self.device = device
        if device == Devices.serial:
            self._connect_serial()
        elif device == Devices.udp:
            self.device_path = 'udpin:localhost:14540'
            self._connect_once()
            logger.info(f"Connected: {self.device_path}")
        else:
            logger.critical(
                f"Unknown device {device}: it should be {Devices.udp} or {Devices.serial}")

        self.mav = MavlinkInterface(self.master)
        self.params = ParametersInterface(self.mav, self.autopilot)
        self.mission = MissionInterface(self.master)

    def configure(self, file_with_params: str, reboot=True):
        self.params.set_multiple(ParametersInterface.yaml_to_dict(file_with_params))

        if reboot:
            time.sleep(2)
            self.reboot()
            time.sleep(2)
            self.connect()

    def reset_params_to_default(self):
        logger.info("Reset parameters to default")
        self.params.reset_to_default()
        self.reboot()
        time.sleep(7)
        self.connect()

    def force_calibrate(self):
        self.params.force_calibrate()

    def reboot(self):
        logger.info("Reboot the autopilot")
        self.master.reboot_autopilot()
        self.master.close()

    def download_mission(self) -> List[MAVLink_mission_item_int_message]:
        return self.mission.download_from_autopilot()

    def load_mission(self, path: str) -> StatusCode:
        return self.mission.load_to_autopilot(path)

    def get_autopilot_type(self):
        return self.autopilot

    def run_mission(self, timeout: int = 100) -> MissionResult:
        return self.mission.run(timeout)

    def _connect_serial(self):
        logger.info("Trying to connect to a serial port.")
        start_time = time.time()
        while True:
            try:
                self.device_path, self.autopilot = Vehicle._get_autopilot_serial_path()
                if self.device_path is not None:
                    self._connect_once()
                    elapsed_time = round(time.time() - start_time, 1)
                    logger.info(f"Connected: {self.device_path} in {elapsed_time} seconds.")
                    break
            except serial.serialutil.SerialException:
                pass

            time.sleep(1)
            logger.info(f"Waiting for the Autopilot {self.device_path}...")

    @staticmethod
    def _get_autopilot_serial_path() -> tuple:
        serial_devices = retry_command(
            lambda: os.listdir('/dev/serial/by-id'),
            delay=5, times=6
        )
        return Vehicle.get_autopilot_type_by_serial_devices(serial_devices)

    @staticmethod
    def get_autopilot_type_by_serial_devices(serial_devices: list) -> tuple:
        if len(serial_devices) < 1:
            return None, None

        device_path = None
        autopilot_type = None
        for serial_device in serial_devices:
            if -1 != serial_device.find(AutopilotTypes.ArduPilot):
                device_path = f"/dev/serial/by-id/{serial_device}"
                autopilot_type = AutopilotTypes.ArduPilot
                break
            if -1 != serial_device.find(AutopilotTypes.PX4):
                device_path = f"/dev/serial/by-id/{serial_device}"
                autopilot_type = AutopilotTypes.PX4
                break
        logger.info(f"Autopilot {device_path} has been found")
        return device_path, autopilot_type

    def get_log_folder(self) -> Union[str, None]:
        folder = {
            (Devices.udp, AutopilotTypes.PX4): '/log',
            (Devices.udp, AutopilotTypes.ArduPilot): None,
            (Devices.serial, AutopilotTypes.PX4): '/fs/microsd/log/',
            (Devices.serial, AutopilotTypes.ArduPilot): '/APM/LOGS'
        }.get((self.device, self.autopilot))
        if folder is None:
            logger.critical(f"For now only {AutopilotTypes.PX4} SITL is supported")
        return folder

    def _connect_once(self):
        self.master = mavutil.mavlink_connection(
            self.device_path,
            source_component=SOURCE_COMPONENT,
            source_system=SOURCE_SYSTEM)
        self.master.mav.heartbeat_send(
            type=mavlink.MAV_TYPE_CHARGING_STATION,
            autopilot=6,
            base_mode=12,
            custom_mode=0,
            system_status=4)
        hb = self.master.wait_heartbeat(timeout=20)

        if hb is None:
            logger.critical('Failed to receive a heartbeat from the FMU. '
                            'Please check your setup. Terminating.')
            sys.exit(1)

        self.mav_ftp = MavFTP(self.master)
        self.autopilot = {
            MAV_AUTOPILOT_ARDUPILOTMEGA: AutopilotTypes.ArduPilot,
            MAV_AUTOPILOT_PX4: AutopilotTypes.PX4
        }.get(hb.autopilot)

        if self.autopilot is None:
            logger.error(
                f'You are connected to unsupported autopilot: '
                f' {enums["MAV_AUTOPILOT"][hb.autopilot].name}. '
                f'Proceed with caution')

        system_str = f"system {self.master.target_system}"
        component_str = f"component {self.master.target_component}"
        logger.info(f"Heartbeat from system ({system_str} {component_str})")

    def analyze_log(self, log: Union[str, bytes, BufferedIOBase, os.PathLike]) -> Union[str, None]:
        if isinstance(log, (str, os.PathLike)):
            with open(log, 'rb') as f:
                log = f.read()

        if isinstance(log, BufferedIOBase):
            log = log.read()

        if self.autopilot == AutopilotTypes.PX4:
            return upload_px4_log(log)
        if self.autopilot == AutopilotTypes.ArduPilot:
            logger.critical("For now only PX4 log analysis is supported")
        return None

def load_parameters(files_with_params: list, device: str, force_calibrate: bool):
    assert isinstance(files_with_params, list)
    assert isinstance(device, str)
    assert isinstance(force_calibrate, bool)

    for idx, path in enumerate(files_with_params):
        assert isinstance(path, str), f"Element at index {idx} is not a string: {path}"

        if not os.path.isabs(path):
            files_with_params[idx] = os.path.abspath(path)

        file_with_params = files_with_params[idx]
        assert os.path.isfile(file_with_params), f"File does not exist: {file_with_params}"

    vehicle = Vehicle()
    vehicle.connect(device)

    vehicle.reset_params_to_default()
    for file_with_params in files_with_params:
        vehicle.configure(file_with_params, reboot=True)

    if force_calibrate:
        vehicle.force_calibrate()
        vehicle.reboot()
