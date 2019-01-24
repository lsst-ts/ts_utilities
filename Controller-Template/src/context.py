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
from . import domain
from . import model
from . import salinterface
from . import states


class Context(object):
    def __init__(self, sal: salinterface.>SUBSYSTEM<Controller, model: model.Model):
        self.log = logging.getLogger("Context")
        self.sal = sal
        self.model = model
        self.state = states.OfflineState()

    def boot(self, command: commands.BootCommand):
        self.log.info(f"Executing command {command.name}.")
        self.processStateCommandResult(self.state.boot(command, self.model))

    def update(self, command: commands.UpdateCommand):
        self.log.debug(f"Executing command {command.name}.")
        self.processStateCommandResult(self.state.update(command, self.model))
>COMMAND_DEFINITIONS<
    def processStateCommandResult(self, newState):
        if newState == domain.States.NoStateTransition:
            return
        if newState == domain.States.OfflineState:
            self.state = states.OfflineState()
        elif newState == domain.States.StandbyState:
            self.state = states.StandbyState()
        elif newState == domain.States.DisabledState:
            self.state = states.DisabledState()
        elif newState == domain.States.EnabledState:
            self.state = states.EnabledState()
        elif newState == domain.States.FaultState:
            self.state = states.FaultState()
        self.log.info(f"Transitioning to {self.state.name}.")
        self.sal.logEvent_summaryState(newState)
