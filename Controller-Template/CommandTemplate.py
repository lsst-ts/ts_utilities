class {upperName}Command(SALCommand):
    def __init__(self, sal : {subsystem}Controller.{subsystem}Controller, commandId : int, data : SALPY_{subsystem}.{subsystem}_command_{name}C):
        SALCommand.__init__(self, sal, commandId, data)

    def ack(self, ackCode : int, errorCode : int, description : str):
        return self.sal.ackCommand_{name}(self.commandId, ackCode, errorCode, description)
