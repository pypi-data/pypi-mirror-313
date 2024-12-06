# SPDX-FileCopyrightText: 2024-present Kevin Ahr <meowmeowahr@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from kevinbotlib import MqttKevinbot

robot = MqttKevinbot()
robot.connect()

while True:
    print(f"Left Motor : {robot.get_state().thermal.left_motor} *C")  # noqa: T201
    print(f"Right Motor: {robot.get_state().thermal.right_motor} *C")  # noqa: T201
    print(f"Internal: {robot.get_state().thermal.internal} *C")  # noqa: T201
    time.sleep(2)
