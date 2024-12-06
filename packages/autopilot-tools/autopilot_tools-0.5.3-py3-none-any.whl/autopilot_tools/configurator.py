#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
# Author: Yuriy <1budsmoker1@gmail.com>
"""
This utility flashes the MCU with the new firmware
and then uploads the new set of parameters from yaml file
"""

import os
import glob
import time
import logging
import argparse
from typing import Optional
import yaml
from autopilot_tools.enums import Devices
from autopilot_tools.vehicle import load_parameters
from autopilot_tools.px4.firmware_uploader import upload_firmware

REPO_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BINARY_OUTPUT_PATH = os.path.join(REPO_DIR, "firmware.bin")

logger = logging.getLogger(__name__)

class AutopilotConfigurator:
    SERIAL_PATH_TO_AUTOPILOT_NAME = {
        "/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v5"      : "px4_fmu-v5",
        "/dev/serial/by-id/usb-3D_Robotics_PX4_BL_FMU_v5"   : "px4_fmu-v5",

        "/dev/serial/by-id/usb-Auterion_PX4_FMU_v6X"        : "px4_fmu-v6x",
        "/dev/serial/by-id/usb-Auterion_PX4_BL_FMU_v6X"     : "px4_fmu-v6x",

        "/dev/serial/by-id/usb-Auterion_PX4_FMU_v6C"        : "px4_fmu-v6c",
        "/dev/serial/by-id/usb-Auterion_PX4_BL_FMU_v6C"     : "px4_fmu-v6c",

        "/dev/serial/by-id/usb-CUAV_PX4_CUAV_X7Pro"         : "cuav_x7pro",
        "/dev/serial/by-id/usb-ArduPilot_CUAV-X7-BL"        : "cuav_x7pro",

        "/dev/serial/by-id/usb-CUAV_PX4_CUAV_Nora"          : "cuav_nora",
        "/dev/serial/by-id/usb-ArduPilot_CUAV-Nora-BL"      : "cuav_nora",
    }

    MODE_TO_TARGET_NAME = {
        "cyphal" : "cyphal",
        "dronecan" : "default",
    }

    @staticmethod
    def find_autopilot(blocking=True) -> Optional[str]:
        """
        Return px4_fmu-v5, px4_fmu-v6x, px4_fmu-v6c, cuav_x7pro or None
        """
        if blocking:
            autopilot = AutopilotConfigurator.find_autopilot(blocking=False)
            while autopilot is None:
                logging.info("Waiting for autopilot to be connected...")
                time.sleep(1)
                autopilot = AutopilotConfigurator.find_autopilot(blocking=False)
        else:
            autopilot = None
            for path, name in AutopilotConfigurator.SERIAL_PATH_TO_AUTOPILOT_NAME.items():
                connected_devices = glob.glob(path + '*')
                for connected_device in connected_devices:
                    if os.path.exists(connected_device):
                        autopilot = name
                        break

        return autopilot

    @staticmethod
    def configure(firmware: str,
                  files_with_params: list,
                  device: str,
                  force_calibrate: bool) -> None:
        """
        firmware - either a path to a .px4 file or a link
        """
        if firmware is None and files_with_params is None:
            logger.error("Nothing to do!")
            return

        if files_with_params is not None:
            AutopilotConfigurator._verify_files_with_params(files_with_params)

        if firmware is not None:
            upload_firmware(firmware=firmware)

        if files_with_params:
            load_parameters(files_with_params, device, force_calibrate)

    @staticmethod
    def configure_with_yaml_file(config_path: str,
                                 need_upload_firmware: bool = True,
                                 need_load_parameters: bool = True) -> None:
        logger.info(f"config_path: {config_path}")
        with open(config_path, 'r', encoding="utf-8") as file:
            yaml_config = yaml.safe_load(file)

        if not need_upload_firmware and not need_load_parameters:
            logger.error("Nothing to do!")
            return

        if need_upload_firmware:
            if 'release' in yaml_config:
                url = AutopilotConfigurator._parse_release(yaml_config)
                upload_firmware(firmware=url)
            elif 'firmware' in yaml_config:
                upload_firmware(firmware=yaml_config['firmware'])
            else:
                logger.critical("There is no release or firmware in the yaml file.!")
                return

        if need_load_parameters and 'params' in yaml_config:
            files_with_params = yaml_config.get('params')
            AutopilotConfigurator._verify_files_with_params(files_with_params)
            load_parameters(files_with_params, "serial", force_calibrate=True)

    @staticmethod
    def _parse_release(yaml_config: dict) -> str:
        assert isinstance(yaml_config, dict)

        fmu = AutopilotConfigurator.find_autopilot(blocking=True)
        logger.info(f"Flight controller {fmu} has been found.")
        release = yaml_config.get('release')
        org = release.get('org')
        repo = release.get('repo')
        tag = release.get('tag')
        target = AutopilotConfigurator.MODE_TO_TARGET_NAME[yaml_config.get('mode')]
        url = f"https://github.com/{org}/{repo}/releases/download/{tag}/{fmu}_{target}.px4"
        return url

    @staticmethod
    def _verify_files_with_params(files_with_params: list) -> None:
        if not isinstance(files_with_params, list) or len(files_with_params) == 0:
            raise ValueError("files_with_params must be a non-empty list.")

        for file_with_params in files_with_params:
            if not isinstance(file_with_params, str):
                raise TypeError("Each item in files_with_params must be a file path string.")
            if not os.path.isfile(file_with_params):
                raise FileNotFoundError(f"The file '{file_with_params}' does not exist.")

def run_with_argparse():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--firmware', type=str,
                        help='path/link to the firmware file')
    parser.add_argument('--params', type=str, nargs='+', metavar='FW',
                        help='Upload those set(s) of parameters to the MCU')
    parser.add_argument('--load', type=str,
                        help='A yaml file with files with parameters')
    parser.add_argument('--force', type=str,
                        help='A yaml file with firmware/release URL and parameters')
    parser.add_argument('-d', '--device', choices=Devices, type=str, default='serial',
                        help='either udp (SITL) or serial (HITL)')
    parser.add_argument('-f', '--force-calibrate', action='store_true',
                        help='set this flag to force calibration')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO if args.verbose else logging.CRITICAL)
    logger.setLevel(logging.INFO if args.verbose else logging.CRITICAL)

    if args.load:
        AutopilotConfigurator.configure_with_yaml_file(args.load, False, True)
    elif args.force:
        AutopilotConfigurator.configure_with_yaml_file(args.force, True, True)
    elif args.firmware or args.params:
        AutopilotConfigurator.configure(firmware=args.firmware,
                                        files_with_params=args.params,
                                        device=args.device,
                                        force_calibrate=args.force_calibrate)
    else:
        parser.error('Nothing to do! Please provide either --firmware, --params or --config')

if __name__ == '__main__':
    run_with_argparse()
