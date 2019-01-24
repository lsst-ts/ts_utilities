# This file is part of >SUBSYSTEM<.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import threading
import time

from . import commands
from . import controller
from . import salinterface


class Thread(threading.Thread):
    def __init__(self):
        super().__init__(name=type(self).__name__.replace("Thread", ""))
        self.log = logging.getLogger("Thread")
        self.running = False

    def stop(self):
        self.log.info(f"Stopping thread {self.name}.")
        self.running = False


class SubscriberThread(Thread):
    def __init__(self, sal: salinterface.>SUBSYSTEM<Controller, controller: controller.Controller, loopTimeInSec: float):
        super().__init__()
        self.sal = sal
        self.controller = controller
        self.loopTimeInSec = loopTimeInSec
>COMMAND_DEFINITIONS<

    def run(self):
        self.log.info(f"Starting thread {self.name}.")
        self.running = True
        while self.running:
            self.sal.runSubscriberChecks()
            time.sleep(self.loopTimeInSec)
        self.log.info(f"Thread {self.name} completed.")


class ControllerThread(Thread):
    def __init__(self, controller: controller.Controller, loopTimeInSec: float):
        super().__init__()
        self.controller = controller
        self.loopTimeInSec = loopTimeInSec

    def run(self):
        self.log.info(f"Starting thread {self.name}.")
        self.running = True
        while self.running:
            command = self.controller.dequeue()
            self.controller.execute(command)
            time.sleep(self.loopTimeInSec)
        self.log.info(f"Thread {self.name} completed.")


class OuterLoopThread(Thread):
    def __init__(self, controller: controller.Controller, loopTimeInSec: float):
        super().__init__()
        self.controller = controller
        self.loopTimeInSec = loopTimeInSec

    def run(self):
        self.log.info(f"Starting thread {self.name}.")
        self.running = True
        while self.running:
            self.controller.enqueue(commands.UpdateCommand())
            time.sleep(self.loopTimeInSec)
        self.log.info(f"Thread {self.name} completed.")
