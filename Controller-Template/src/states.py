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


class State(object):
    def __init__(self):
        self.log = logging.getLogger("State")
        self.name = type(self).__name__

    def boot(self, command: commands.BootCommand, model: model.Model):
        return self.invalidState(command)

    def update(self, command: commands.UpdateCommand, model: model.Model):
        return self.invalidState(command)
>COMMAND_DEFINITIONS<
    def invalidState(self, command: commands.Command):
        self.log.error(f"{command.name} is invalid in the {self.name} state.")
        command.ackInvalidState(f"Command is not valid in the {self.name} state.")
        return domain.States.NoStateTransition


class OfflineState(State):
    def __init__(self):
        super().__init__()

    def boot(self, command: commands.BootCommand, model: model.Model):
        self.log.info(f"Executing {command.name} in {self.name}.")
        command.ackComplete()
        return domain.States.StandbyState


class StandbyState(State):
    def __init__(self):
        super().__init__()

    def update(self, command: commands.UpdateCommand, model: model.Model):
        self.log.debug(f"Executing {command.name} in {self.name}.")
        model.outerLoop()
        return domain.States.NoStateTransition

    def start(self, command: commands.StartCommand, model: model.Model):
        self.log.info(f"Executing {command.name} in {self.name}.")
        command.ackComplete()
        return domain.States.DisabledState


class DisabledState(State):
    def __init__(self):
        super().__init__()

    def update(self, command: commands.UpdateCommand, model: model.Model):
        self.log.debug(f"Executing {command.name} in {self.name}.")
        model.outerLoop()
        return domain.States.NoStateTransition

    def enable(self, command: commands.EnableCommand, model: model.Model):
        self.log.info(f"Executing {command.name} in {self.name}.")
        command.ackComplete()
        return domain.States.EnabledState

    def standby(self, command: commands.StandbyCommand, model: model.Model):
        self.log.info(f"Executing {command.name} in {self.name}.")
        command.ackComplete()
        return domain.States.StandbyState


class EnabledState(State):
    def __init__(self):
        super().__init__()

    def update(self, command: commands.UpdateCommand, model: model.Model):
        self.log.debug(f"Executing {command.name} in {self.name}.")
        model.outerLoop()
        return domain.States.NoStateTransition

    def disable(self, command: commands.DisableCommand, model: model.Model):
        self.log.info(f"Executing {command.name} in {self.name}.")
        command.ackComplete()
        return domain.States.DisabledState


class FaultState(State):
    def __init__(self):
        super().__init__()

    def update(self, command: commands.UpdateCommand, model: model.Model):
        self.log.debug(f"Executing {command.name} in {self.name}.")
        model.outerLoop()
        return domain.States.NoStateTransition

    def standby(self, command: commands.StandbyCommand, model: model.Model):
        self.log.info(f"Executing {command.name} in {self.name}.")
        command.ackComplete()
        return domain.States.StandbyState
