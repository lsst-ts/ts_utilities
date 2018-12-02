import logging
import SALPY_{subsystem}
import {subsystem}Controller

class Command(object):
    def __init__(self):
        self.name = type(self).__name__
        self.log = logging.getLogger("Command")
        self.log.debug("Creating command %s." % self.name)

    def validate(self):
        return True
    
    def ack(self, ackCode : int, errorCode : int, description : str):
        return SALPY_{subsystem}.SAL__OK

    def ackInProgress(self):
        self.log.debug("Sending %s ack command in progress." % self.name)
        return self.ack(SALPY_{subsystem}.SAL__CMD_INPROGRESS, 0, "In-Progress")

    def ackComplete(self):
        self.log.info("Sending %s ack command completed." % self.name)
        return self.ack(SALPY_{subsystem}.SAL__CMD_COMPLETE, 0, "Complete")

    def ackNotPermitted(self, errorCode : int, description : str):
        self.log.warning("Sending %s ack command not permitted. Error code %d. %s" % (self.name, errorCode, description))
        return self.ack(SALPY_{subsystem}.SAL__CMD_NOPERM, errorCode, "Not Permitted: %s" % (description))

    def ackAborted(self, errorCode : int, description : str):
        self.log.warning("Sending %s ack command aborted. Error code %d. %s" % (self.name, errorCode, description))
        return self.ack(SALPY_{subsystem}.SAL__CMD_ABORTED, errorCode, "Aborted: %s" % (description))

    def ackFailed(self, errorCode : int, description : str):
        self.log.warning("Sending %s ack command failed. Error code %d. %s" % (self.name, errorCode, description))
        return self.ack(SALPY_{subsystem}.SAL__CMD_FAILED, errorCode, "Failed: %s" % (description))

    def ackInvalidState(self, description : str):
        self.log.warning("Sending %s ack command invalid state. %s" % (self.name, description))
        return self.ack(SALPY_{subsystem}.SAL__CMD_FAILED, -320, "Failed: %s" % (description))

    def ackInvalidParameter(self, description : str):
        self.log.warning("Sending %s ack command invalid parameter. %s" % (self.name, description))
        return self.ack(SALPY_{subsystem}.SAL__CMD_FAILED, -321, "Failed: %s" % (description))

    def ackAlreadyInProgress(self, description : str):
        self.log.warning("Sending %s ack command already in progress. %s" % (self.name, description))
        return self.ack(SALPY_{subsystem}.SAL__CMD_FAILED, -322, "Failed: %s" % (description))

    def ackExecutionBlocked(self, description : str):
        self.log.warning("Sending %s ack command execution blocked. %s" % (self.name, description))
        return self.ack(SALPY_{subsystem}.SAL__CMD_FAILED, -323, "Failed: %s" % (description))

    def ackAlreadyInState(self, description : str):
        self.log.warning("Sending %s ack command already in state. %s" % (self.name, description))
        return self.ack(SALPY_{subsystem}.SAL__CMD_FAILED, -324, "Failed: %s" % (description))

class SALCommand(Command):
    def __init__(self, sal : {subsystem}Controller.{subsystem}Controller, commandId : int, data):
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

class UpdateCommand(Command):
    def __init__(self):
        Command.__init__(self)
{commandDefinitions}