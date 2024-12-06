# SPDX-FileCopyrightText: 2024-present Kevin Ahr <meowmeowahr@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from kevinbotlib import SerialEyes

eyes = SerialEyes()
eyes.connect("/dev/ttyUSB0", 115200, 5)

print(eyes.get_state().model_dump_json(indent=4))  # noqa: T201

time.sleep(1)
