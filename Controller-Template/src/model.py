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
import queue
import time

from . import salinterface


class Model(object):
    def __init__(self, sal: salinterface.>SUBSYSTEM<Controller):
        self.log = logging.getLogger("Model")
        self.sal = sal
        self.shutdown = queue.Queue()
        self.lastOuterLoop = 0

    def getSAL(self):
        return self.sal

    def waitForShutdown(self):
        self.log.info("Waiting for shutdown.")
        self.shutdown.get()

    def triggerShutdown(self):
        self.log.info("Triggering shutdown.")
        self.shutdown.put(0)

    def outerLoop(self):
        current = time.time()
        executionTime = current - self.lastOuterLoop
        self.log.debug(f"Outer loop execution time {executionTime:0.4f}.")
        self.lastOuterLoop = current
