# SPDX-FileCopyrightText: 2024-present Kevin Ahr <meowmeowahr@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from kevinbotlib import SerialKevinbot

robot = SerialKevinbot()
robot.connect("/dev/ttyAMA2", 921600, 5, 1)

robot.e_stop()
