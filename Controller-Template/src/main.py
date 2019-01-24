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

from . import commands
from . import context
from . import controller
from . import model
from . import salinterface
from . import threads


# This is for unit tests only since not all CSCs have a shutdown command
shutdownAction = None


def run():
    logging.basicConfig(format="%(asctime)-15s %(threadName)-16s %(name)-10s %(levelname)-8s %(message)s")
    logging.getLogger("Command").setLevel(logging.INFO)
    logging.getLogger("Context").setLevel(logging.INFO)
    logging.getLogger("Controller").setLevel(logging.INFO)
    logging.getLogger("Model").setLevel(logging.INFO)
    logging.getLogger("State").setLevel(logging.INFO)
    logging.getLogger("Thread").setLevel(logging.DEBUG)
    logging.getLogger("Main").setLevel(logging.DEBUG)
    log = logging.getLogger("Main")
    log.info("Starting >SUBSYSTEM< application.")
    log.info("Initializing >SUBSYSTEM< SAL interface.")
    the>SUBSYSTEM<SAL = salinterface.>SUBSYSTEM<Controller()
    log.info("Initializing >SUBSYSTEM< model.")
    theModel = model.Model(the>SUBSYSTEM<SAL)
    global shutdownAction
    shutdownAction = theModel.triggerShutdown
    log.info("Initializing >SUBSYSTEM< context.")
    theContext = context.Context(the>SUBSYSTEM<SAL, theModel)
    log.info("Initializing >SUBSYSTEM< controller.")
    theController = controller.Controller(theContext)
    log.info("Initializing >SUBSYSTEM< controller thread.")
    controllerThread = threads.ControllerThread(theController, 0.001)
    log.info("Initializing >SUBSYSTEM< subscriber thread.")
    subscriberThread = threads.SubscriberThread(the>SUBSYSTEM<SAL, theController, 0.001)
    log.info("Initializing >SUBSYSTEM< outer loop thread.")
    outerLoopThread = threads.OuterLoopThread(theController, 0.050)
    log.info("Adding BootCommand for OfflineState to StandbyState transition.")
    theController.enqueue(commands.BootCommand())
    log.info("Starting >SUBSYSTEM< controller thread.")
    controllerThread.start()
    log.info("Starting >SUBSYSTEM< subscriber thread.")
    subscriberThread.start()
    log.info("Starting >SUBSYSTEM< outer loop thread.")
    outerLoopThread.start()
    log.info(">SUBSYSTEM< is now running and waiting for shutdown.")
    theModel.waitForShutdown()
    log.info(">SUBSYSTEM< has a shutdown request.")
    log.info("Stopping >SUBSYSTEM< controller thread.")
    controllerThread.stop()
    controllerThread.join()
    log.info("Stopping >SUBSYSTEM< subscriber thread.")
    subscriberThread.stop()
    subscriberThread.join()
    log.info("Stopping >SUBSYSTEM< outer loop thread.")
    outerLoopThread.stop()
    outerLoopThread.join()
    log.info("Closing >SUBSYSTEM< SAL interface.")
    the>SUBSYSTEM<SAL.close()
