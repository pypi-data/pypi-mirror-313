# SPDX-FileCopyrightText: 2024-present Kevin Ahr <meowmeowahr@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from kevinbotlib import MqttKevinbot

robot = MqttKevinbot()
robot.connect()

while True:
    print(f"Uptime (s) : {robot.get_state().uptime}")  # noqa: T201
    print(f"Uptime (ms): {robot.get_state().uptime_ms}")  # noqa: T201
    time.sleep(1)
