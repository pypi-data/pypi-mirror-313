#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
# Author: Yuriy <1budsmoker1@gmail.com>
"""
This utility uploads mission to HITL/SITL simulator,
waits for completion, then collects and processes the
resulting log with https://logs.px4.io/
"""
import argparse
import logging
import os
import sys
from time import time
from autopilot_tools.vehicle import Vehicle
from autopilot_tools.mission_file.mission_result import StatusCode
from autopilot_tools.mavlink_ftp.ftp_filesystem import File
from autopilot_tools.enums import Devices
from autopilot_tools.enums import AutopilotTypes

logger = logging.getLogger(__name__)

def run_test_scenario(device: str, mission: str, timeout: int, output: str):
    logger.info(f"1/6. Connecting to {device}...")
    vehicle = Vehicle()
    vehicle.connect(device=device)

    logger.info(f"2/6. Uploading mission {mission} to the autopilot...")
    result = vehicle.load_mission(mission)
    if result != StatusCode.OK:
        logger.critical(f'Mission upload failed with code {result}')
        sys.exit(1)

    logger.info(f"3/6. Running mission with timeout={timeout} sec...")
    result = vehicle.run_mission(timeout=timeout)
    if result.status == StatusCode.MISSION_TIMEOUT:
        raise TimeoutError('Mission execution timed out')
    if result.status != StatusCode.OK:
        raise RuntimeError(f'Mission execution failed: {result}')
    logger.info('Mission executed successfully')

    logger.info('4/6. Downloading log...')
    latest_file: File = vehicle.mav_ftp.get_last_log(vehicle.get_log_folder())
    start_time = time()
    latest_file.materialize()
    logger.info(f'Downloaded {latest_file.size}B in {time() - start_time:.2f} s')

    if output is not None:
        logger.info('5/6. Saving log locally...')
        latest_file.save_locally(output)
        logger.info(f"Saved log file to {os.path.abspath(output)}")

        if vehicle.autopilot == AutopilotTypes.PX4:
            logger.info('6/6. Uploading to https://logs.px4.io')
            result.log_link = vehicle.analyze_log(latest_file.data)

    logger.info(result)

def run_with_argparse():
    parser = argparse.ArgumentParser(prog='Run the test scenario', description=__doc__)

    parser.add_argument(
        'mission', type=str,
        help='mission file in .plan format'
    )

    parser.add_argument(
        '-p', '--device', dest='device', choices=list(Devices), type=str, default='serial',
        help='There are 2 options: udp (for SITL) and serial (for HITL). Defaukt is serial'
    )

    parser.add_argument(
        '-t', '--timeout', dest='timeout', type=int, default=300,
        help='Abort the mission if this execution timeout is exceeded. Default is 300 sec.'
    )

    parser.add_argument(
        '-o', '--output', dest='output', default=None, type=str,
        help='directory where to store downloaded log'
    )

    parser.add_argument(
        '-v', '--verbose', dest='verbose', action='store_true',
        help="Use DEBUG logging level. By default - INFO."
    )
    parser.add_argument(
        '-q', '--quite', dest='quite', action='store_true',
        help="Use DEBUG logging level. By default - INFO."
    )

    args = parser.parse_args()

    if args.quite:
        logging_level = logging.ERROR
    elif args.verbose:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logging.basicConfig(level=logging_level)
    logger.setLevel(logging_level)

    run_test_scenario(args.device, args.mission, args.timeout, args.output)

if __name__ == '__main__':
    run_with_argparse()
