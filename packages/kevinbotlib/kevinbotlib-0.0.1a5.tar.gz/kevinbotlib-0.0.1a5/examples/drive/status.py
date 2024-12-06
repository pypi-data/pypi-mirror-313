# SPDX-FileCopyrightText: 2024-present Kevin Ahr <meowmeowahr@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from kevinbotlib import Drivebase, MqttKevinbot

robot = MqttKevinbot()
robot.connect()

drive = Drivebase(robot)

robot.request_enable()  # Ask the core to enable
while not robot.get_state().enabled:  # Wait until the core is enabled
    time.sleep(0.01)

time.sleep(1)  # Wait for data to arrive

print(f"Speeds: {drive.get_powers()}")  # noqa: T201
print(f"Watts: {drive.get_watts()}")  # noqa: T201
print(f"Amps: {drive.get_amps()}")  # noqa: T201
