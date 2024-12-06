# SPDX-FileCopyrightText: 2024-present Kevin Ahr <meowmeowahr@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from kevinbotlib import SerialKevinbot

robot = SerialKevinbot()
robot.connect("/dev/ttyAMA2", 921600, 5, 1)

while True:
    print(f"Left Motor : {robot.get_state().thermal.left_motor} *C")  # noqa: T201
    print(f"Right Motor: {robot.get_state().thermal.right_motor} *C")  # noqa: T201
    print(f"Internal: {robot.get_state().thermal.internal} *C")  # noqa: T201
    time.sleep(2)
