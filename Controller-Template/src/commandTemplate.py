

class >UPPER_NAME<Command(SALCommand):
    def __init__(self, sal: salinterface.>SUBSYSTEM<Controller, commandId: int, data: SALPY_>SUBSYSTEM<.>SUBSYSTEM<_command_>NAME<C):
        super().__init__(sal, commandId, data)

    def ack(self, ackCode: int, errorCode: int, description: str):
        return self.sal.ackCommand_>NAME<(self.commandId, ackCode, errorCode, description)