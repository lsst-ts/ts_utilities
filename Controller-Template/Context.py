import logging
import {subsystem}Controller
import Model
import States
import Commands

class Context(object):
    def __init__(self, sal : {subsystem}Controller.{subsystem}Controller, model : Model.Model):
        self.log = logging.getLogger("Context")
        self.sal = sal
        self.model = model
        self.state = States.OfflineState()

    def boot(self, command : Commands.BootCommand):
        self.log.info("Executing command %s." % command.name)
        self.processStateCommandResult(self.state.boot(command, self.model))

    def update(self, command : Commands.UpdateCommand):
        self.log.debug("Executing command %s." % command.name)
        self.processStateCommandResult(self.state.update(command, self.model))
{commandDefinitions}
    def processStateCommandResult(self, newState):
        if newState == States.States.NoStateTransition:
            return
        if newState == States.States.OfflineState:
            self.state = States.OfflineState()
        elif newState == States.States.StandbyState:
            self.state = States.StandbyState()
        elif newState == States.States.DisabledState:
            self.state = States.DisabledState()
        elif newState == States.States.EnabledState:
            self.state = States.EnabledState()
        elif newState == States.States.FaultState:
            self.state = States.FaultState()
        self.log.info("Transitioning to %s." % self.state.name)
        self.sal.logEvent_summaryState(newState)