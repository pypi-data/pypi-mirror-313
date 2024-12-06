#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
# Author: Yuriy <1budsmoker1@gmail.com>

import os
import sys
import logging
import requests
from autopilot_tools.px4._px_uploader import px_uploader

DOWNLOAD_DIR = 'downloads'
SERIAL_PORTS = {
    'darwin': "/dev/tty.usbmodemPX*,/dev/tty.usbmodem*",

    'linux': "/dev/serial/by-id/*_PX4_*,/dev/serial/by-id/usb-3D_Robotics*,"
             "/dev/serial/by-id/usb-The_Autopilot*,/dev/serial/by-id/usb-Bitcraze*,"
             "/dev/serial/by-id/pci-Bitcraze*,/dev/serial/by-id/usb-Gumstix*,"
             "/dev/serial/by-id/usb-UVify*,/dev/serial/by-id/usb-ArduPilot*,"
             "/dev/serial/by-id/ARK*,",

    'cygwin': "/dev/ttyS*",

    'win32': "COM32,COM31,COM30,COM29,COM28,COM27,COM26,COM25,COM24,COM23,COM22,"
             "COM21,COM20,COM19,COM18,COM17,COM16,COM15,COM14,COM13,COM12,COM11,"
             "COM10,COM9,COM8,COM7,COM6,COM5,COM4,COM3,COM2,COM1,COM0"
}[sys.platform]

logger = logging.getLogger(__name__)

def upload_firmware(firmware: str):
    assert isinstance(firmware, str)
    logger.debug(f'Upload firmware {firmware}')
    initial_directory = os.getcwd()

    if os.path.exists(firmware):
        path = os.path.abspath(firmware)
    elif requests.head(firmware, allow_redirects=True,
                        timeout=10).status_code == requests.codes.ok:  # pylint: disable=E1101
        logger.info(f'Link provided {firmware}. Attempting download')
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        r = requests.get(firmware, timeout=300)
        filename = os.path.basename(firmware)
        path = os.path.join(DOWNLOAD_DIR, filename)
        with open(path, 'wb') as f:
            f.write(r.content)
        logger.info('Download successful')
    else:
        os.chdir(initial_directory)
        raise FileNotFoundError(f'Provided path {firmware} is neither a local file nor a link.')

    px_uploader([path], SERIAL_PORTS)
    os.chdir(initial_directory)
