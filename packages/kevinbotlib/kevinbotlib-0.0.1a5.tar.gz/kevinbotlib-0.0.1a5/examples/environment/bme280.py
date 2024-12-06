# SPDX-FileCopyrightText: 2024-present Kevin Ahr <meowmeowahr@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from kevinbotlib import MqttKevinbot

robot = MqttKevinbot()
robot.connect()

while True:
    print(f"Temp  : {robot.get_state().enviro.temperature} *C")  # noqa: T201
    print(f"Humi  : {robot.get_state().enviro.humidity} %")  # noqa: T201
    print(f"Pres  : {robot.get_state().enviro.pressure} hPa")  # noqa: T201
    time.sleep(2)
