import logging
import SALPY_{subsystem}
import Commands
import Model

class States(object):
    OfflineState = SALPY_{subsystem}.SAL__STATE_OFFLINE
    StandbyState = SALPY_{subsystem}.SAL__STATE_STANDBY
    DisabledState = SALPY_{subsystem}.SAL__STATE_DISABLED
    EnabledState = SALPY_{subsystem}.SAL__STATE_ENABLED
    FaultState = SALPY_{subsystem}.SAL__STATE_FAULT
    NoStateTransition  = 999

class State(object):
    def __init__(self):
        self.log = logging.getLogger("State")
        self.name = type(self).__name__

    def boot(self, command : Commands.BootCommand, model : Model.Model):
        return self.invalidState(command)

    def update(self, command : Commands.UpdateCommand, model : Model.Model):
        return self.invalidState(command)
{commandDefinitions}
    def invalidState(self, command : Commands.Command):
        self.log.error("%s is invalid in the %s state." % (command.name, self.name))
        command.ackInvalidState("Command is not valid in the {state} state.".format(state = self.name))
        return States.NoStateTransition

class OfflineState(State):
    def __init__(self):
        State.__init__(self)

    def boot(self, command : Commands.BootCommand, model : Model.Model):
        self.log.info("Executing %s in %s." % (command.name, self.name))
        command.ackComplete()
        return States.StandbyState

class StandbyState(State):
    def __init__(self):
        State.__init__(self)

    def update(self, command : Commands.UpdateCommand, model : Model.Model):
        self.log.debug("Executing %s in %s." % (command.name, self.name))
        model.outerLoop()
        return States.NoStateTransition

    def start(self, command : Commands.StartCommand, model : Model.Model):
        self.log.info("Executing %s in %s." % (command.name, self.name))
        command.ackComplete()
        return States.DisabledState

class DisabledState(State):
    def __init__(self):
        State.__init__(self)

    def update(self, command : Commands.UpdateCommand, model : Model.Model):
        self.log.debug("Executing %s in %s." % (command.name, self.name))
        model.outerLoop()
        return States.NoStateTransition

    def enable(self, command : Commands.EnableCommand, model : Model.Model):
        self.log.info("Executing %s in %s." % (command.name, self.name))
        command.ackComplete()
        return States.EnabledState

    def standby(self, command : Commands.StandbyCommand, model : Model.Model):
        self.log.info("Executing %s in %s." % (command.name, self.name))
        command.ackComplete()
        return States.StandbyState

class EnabledState(State):
    def __init__(self):
        State.__init__(self)

    def update(self, command : Commands.UpdateCommand, model : Model.Model):
        self.log.debug("Executing %s in %s." % (command.name, self.name))
        model.outerLoop()
        return States.NoStateTransition

    def disable(self, command : Commands.DisableCommand, model : Model.Model):
        self.log.info("Executing %s in %s." % (command.name, self.name))
        command.ackComplete()
        return States.DisabledState

class FaultState(State):
    def __init__(self):
        State.__init__(self)

    def update(self, command : Commands.UpdateCommand, model : Model.Model):
        self.log.debug("Executing %s in %s." % (command.name, self.name))
        model.outerLoop()
        return States.NoStateTransition

    def standby(self, command : Commands.StandbyCommand, model : Model.Model):
        self.log.info("Executing %s in %s." % (command.name, self.name))
        command.ackComplete()
        return States.StandbyState