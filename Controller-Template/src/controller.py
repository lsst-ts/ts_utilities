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

from . import commands
from . import context


class Controller(object):
    def __init__(self, context: context.Context):
        self.log = logging.getLogger("Controller")
        self.context = context
        self.queue = queue.Queue()

    def clear(self):
        self.log.info("Clearing command queue.")
        self.queue = queue.Queue()

    def enqueue(self, command: commands.Command):
        self.log.debug(f"Attempting to add {command.name} to the command queue.")
        if command.validate():
            self.queue.put(command)

    def dequeue(self):
        return self.queue.get()

    def execute(self, command: commands.Command):
        self.log.debug(f"Starting to execute {command.name}.")
        command.ackInProgress()
        if isinstance(command, commands.UpdateCommand):
            self.context.update(command)
        elif isinstance(command, commands.BootCommand):
            self.context.boot(command)
>COMMAND_DEFINITIONS<
        else:
            self.log.error(f"Unhandled command {command.name}. Cannot execute.")
