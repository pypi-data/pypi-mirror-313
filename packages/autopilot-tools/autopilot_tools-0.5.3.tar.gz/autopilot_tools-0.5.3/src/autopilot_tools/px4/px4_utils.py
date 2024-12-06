#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
# Author: Yuriy <1budsmoker1@gmail.com>
from typing import Union
import logging
import requests

SERVER = 'https://logs.px4.io'
UPLOAD_URL = SERVER + '/upload'

payload = {
    'description': '1', 'email': '', 'feedback': '2',
    'public': 'true', 'rating': 'notset', 'source': 'webui',
    'type': 'flightreport', 'videoUrl': '', 'windSpeed': -1
}


logger = logging.getLogger(__name__)

def upload_px4_log(log: bytes, timeout: int = 300) -> Union[str, None]:
    r = requests.post(
        UPLOAD_URL, data=payload, files={'filearg': log},
        allow_redirects=False, timeout=timeout)

    if (r.status_code == requests.codes.found and  # pylint: disable=E1101
            'Location' in r.headers):
        plot_url = r.headers['Location']
        if len(plot_url) > 0 and plot_url[0] == '/':
            plot_url = SERVER + plot_url

        return plot_url
    logger.warning(f"Failed to upload log: Error {r.status_code}")
    return None
