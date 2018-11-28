from {subsystem}Enumerations import SummaryStates

class States(object):
    OfflineState = SummaryStates.OfflineState
    StandbyState = SummaryStates.StandbyState
    DisabledState = SummaryStates.DisabledState
    EnabledState = SummaryStates.EnabledState
    FaultState = SummaryStates.FaultState
    NoStateTransition = 9999

class State(object):
    def __init__(self, name):
        self.name = name

    def boot(self, command, model):
        return self.invalidState(command)

    def start(self, command, model):
        return self.invalidState(command)

    def enable(self, command, model):
        return self.invalidState(command)

    def disable(self, command, model):
        return self.invalidState(command)

    def standby(self, command, model):
        return self.invalidState(command)

    def update(self, command, model):
        return self.invalidState(command)

    def invalidState(self, command):
        command.ackInvalidState("Command is not valid in the {state} state.".format(state = self.name))
        return States.NoStateTransition

class OfflineState(State):
    def __init__(self):
        State.__init__(self, "Offline")

    def boot(self, command, model):
        command.ackComplete()
        return States.StandbyState

class StandbyState(State):
    def __init__(self):
        State.__init__(self, "Standby")

    def start(self, command, model):
        command.ackComplete()
        return States.DisabledState

class DisabledState(State):
    def __init__(self):
        State.__init__(self, "Disabled")

    def enable(self, command, model):
        command.ackComplete()
        return States.EnabledState

    def standby(self, command, model):
        command.ackComplete()
        return States.StandbyState

class EnabledState(State):
    def __init__(self):
        State.__init__(self, "Enabled")

    def disable(self, command, model):
        command.ackComplete()
        return States.DisabledState

class FaultState(State):
    def __init__(self):
        State.__init__(self, "Fault")

    def standby(self, command, model):
        command.ackComplete()
        return States.StandbyState