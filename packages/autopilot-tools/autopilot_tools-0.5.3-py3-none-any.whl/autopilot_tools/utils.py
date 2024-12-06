#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
# Author: Yuriy <1budsmoker1@gmail.com>
import logging
from time import sleep
from typing import Callable, TypeVar, Union


T = TypeVar('T')
logger = logging.getLogger(__name__)


def retry_command(
        fun: Callable[[], Union[T, None]], times=3,
        test: Callable[[T], bool] = lambda x: x is not None,
        delay: int = 0) -> Union[T, None]:
    exc = None
    for i in range(times):
        res = None
        try:
            res = fun()
            if test(res):
                return res
            # I'm re-raising it later down the line anyways
        except Exception as e:  # pylint: disable=broad-except
            exc = e
        logger.warning(f"Failed command {i+1}/{times} times, "
                    f"result: {res if exc is None else exc}")
        if delay != 0:
            sleep(delay)
    if exc is not None:
        raise exc
    return None
