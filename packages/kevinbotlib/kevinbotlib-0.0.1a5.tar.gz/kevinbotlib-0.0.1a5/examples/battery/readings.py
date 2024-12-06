# SPDX-FileCopyrightText: 2024-present Kevin Ahr <meowmeowahr@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from kevinbotlib import MqttKevinbot

robot = MqttKevinbot()
robot.connect()

time.sleep(3)  # Wait to get data

print(f"Voltages: {robot.get_state().battery.voltages}")  # noqa: T201
print(f"Raw Voltages: {robot.get_state().battery.raw_voltages}")  # noqa: T201
print(f"States: {robot.get_state().battery.states}")  # noqa: T201
