from Context import Context

class Command(object):
    def __init__(self):
        pass

    def validate(self):
        return True
    
    def execute(self, context):
        pass

    def ack(self, ackCode, errorCode, description):
        pass

    def ackInProgress(self):
        self.ack(301, 0, "In-Progress")

    def ackComplete(self):
        self.ack(303, 0, "Complete")

    def ackNotPermitted(self, errorCode, description):
        self.ack(-300, errorCode, "Not Permitted: %s" % (description))

    def ackAborted(self, errorCode, description):
        self.ack(-303, errorCode, "Aborted: %s" % (description))

    def ackFailed(self, errorCode, description):
        self.ack(-302, errorCode, "Failed: %s" % (description))

    def ackInvalidState(self, description):
        self.ackFailed(-320, description)

    def ackInvalidParameter(self, description):
        self.ackFailed(-321, description)

    def ackAlreadyInProgress(self, description):
        self.ackFailed(-322, description)

    def ackExecutionBlocked(self, description):
        self.ackFailed(-323, description)

    def ackAlreadyInState(self, description):        
        self.ackFailed(-324, description)

class SALCommand(Command):
    def __init__(self, sal, commandId, data):
        Command.__init__(self)
        self.sal = sal
        self.commandId = commandId
        self.data = data

    def getCommandId(self):
        return self.commandId

    def getData(self):
        return self.data

class BootCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def execute(self, context):
        context.boot(self)

class StartCommand(SALCommand):
    def __init__(self, sal, commandId, data):
        SALCommand.__init__(self, sal, commandId, data)

    def execute(self, context):
        context.start(self)

    def ack(self, ackCode, errorCode, description):
        self.sal.ackCommand_start(self.commandId, ackCode, errorCode, description)

class EnableCommand(SALCommand):
    def __init__(self, sal, commandId, data):
        SALCommand.__init__(self, sal, commandId, data)
        
    def execute(self, context):
        context.enable(self)

    def ack(self, ackCode, errorCode, description):
        self.sal.ackCommand_enable(self.commandId, ackCode, errorCode, description)

class DisableCommand(SALCommand):
    def __init__(self, sal, commandId, data):
        SALCommand.__init__(self, sal, commandId, data)

    def execute(self, context):
        context.disable(self)

    def ack(self, ackCode, errorCode, description):
        self.sal.ackCommand_disable(self.commandId, ackCode, errorCode, description)

class StandbyCommand(SALCommand):
    def __init__(self, sal, commandId, data):
        SALCommand.__init__(self, sal, commandId, data)

    def execute(self, context):
        context.standby(self)

    def ack(self, ackCode, errorCode, description):
        self.sal.ackCommand_standby(self.commandId, ackCode, errorCode, description)

class UpdateCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def execute(self, context):
        context.update(self)