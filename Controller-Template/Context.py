from States import States, OfflineState, StandbyState, DisabledState, EnabledState, FaultState

class Context(object):
    def __init__(self, sal, model):
        self.sal = sal
        self.model = model
        self.state = OfflineState()

    def boot(self, command):
        self.processStateCommandResult(self.state.boot(command, self.model))

    def start(self, command):
        self.processStateCommandResult(self.state.start(command, self.model))

    def enable(self, command):
        self.processStateCommandResult(self.state.enable(command, self.model))

    def disable(self, command):
        self.processStateCommandResult(self.state.disable(command, self.model))

    def standby(self, command):
        self.processStateCommandResult(self.state.standby(command, self.model))

    def update(self, command):
        self.processStateCommandResult(self.state.update(command, self.model))

    def processStateCommandResult(self, newState):
        if newState == States.NoStateTransition:
            return
        if newState == States.OfflineState:
            self.state = OfflineState()
        elif newState == States.StandbyState:
            self.state = StandbyState()
        elif newState == States.DisabledState:
            self.state = DisabledState()
        elif newState == States.EnabledState:
            self.state = EnabledState()
        elif newState == States.FaultState:
            self.state = FaultState()
        self.sal.logEvent_summaryState(newState)