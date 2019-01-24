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

import SALPY_>SUBSYSTEM<
from . import salinterface


class Command(object):
    def __init__(self):
        self.name = type(self).__name__
        self.log = logging.getLogger("Command")
        self.log.debug(f"Creating command {self.name}.")

    def validate(self):
        return True

    def ack(self, ackCode: int, errorCode: int, description: str):
        return SALPY_>SUBSYSTEM<.SAL__OK

    def ackInProgress(self):
        self.log.debug(f"Sending {self.name} ack command in progress.")
        return self.ack(SALPY_>SUBSYSTEM<.SAL__CMD_INPROGRESS, 0, "In-Progress")

    def ackComplete(self):
        self.log.info(f"Sending {self.name} ack command completed.")
        return self.ack(SALPY_>SUBSYSTEM<.SAL__CMD_COMPLETE, 0, "Complete")

    def ackNotPermitted(self, errorCode: int, description: str):
        self.log.warning(f"Sending {self.name} ack command not permitted. Error code {errorCode}. {description}")
        return self.ack(SALPY_>SUBSYSTEM<.SAL__CMD_NOPERM, errorCode, f"Not Permitted: {description}")

    def ackAborted(self, errorCode: int, description: str):
        self.log.warning(f"Sending {self.name} ack command aborted. Error code {errorCode}. {description}")
        return self.ack(SALPY_>SUBSYSTEM<.SAL__CMD_ABORTED, errorCode, f"Aborted: {description}")

    def ackFailed(self, errorCode: int, description: str):
        self.log.warning(f"Sending {self.name} ack command failed. Error code {errorCode}. {description}")
        return self.ack(SALPY_>SUBSYSTEM<.SAL__CMD_FAILED, errorCode, f"Failed: {description}")

    def ackInvalidState(self, description: str):
        self.log.warning(f"Sending {self.name} ack command invalid state. {description}")
        return self.ack(SALPY_>SUBSYSTEM<.SAL__CMD_FAILED, -320, f"Failed: {description}")

    def ackInvalidParameter(self, description: str):
        self.log.warning(f"Sending {self.name} ack command invalid parameter. {description}")
        return self.ack(SALPY_>SUBSYSTEM<.SAL__CMD_FAILED, -321, f"Failed: {description}")

    def ackAlreadyInProgress(self, description: str):
        self.log.warning(f"Sending {self.name} ack command already in progress. {description}")
        return self.ack(SALPY_>SUBSYSTEM<.SAL__CMD_FAILED, -322, f"Failed: {description}")

    def ackExecutionBlocked(self, description: str):
        self.log.warning(f"Sending {self.name} ack command execution blocked. {description}")
        return self.ack(SALPY_>SUBSYSTEM<.SAL__CMD_FAILED, -323, f"Failed: {description}")

    def ackAlreadyInState(self, description: str):
        self.log.warning(f"Sending {self.name} ack command already in state. {description}")
        return self.ack(SALPY_>SUBSYSTEM<.SAL__CMD_FAILED, -324, f"Failed: {description}")


class SALCommand(Command):
    def __init__(self, sal: salinterface.>SUBSYSTEM<Controller, commandId: int, data):
        super().__init__()
        self.sal = sal
        self.commandId = commandId
        self.data = data

    def getCommandId(self):
        return self.commandId

    def getData(self):
        return self.data


class BootCommand(Command):
    def __init__(self):
        super().__init__()


class UpdateCommand(Command):
    def __init__(self):
        super().__init__()>COMMAND_DEFINITIONS<
