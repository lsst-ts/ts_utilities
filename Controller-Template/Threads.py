import time
import threading
from Commands import StartCommand, EnableCommand, DisableCommand, StandbyCommand, UpdateCommand

class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False

    def stop(self):
        self.running = False

class SubscriberThread(Thread):
    def __init__(self, sal, controller):
        Thread.__init__(self)
        self.sal = sal
        self.controller = controller
        self.sal.subscribeCommand_start(lambda commandId, data: self.controller.enqueue(StartCommand(self.sal, commandId, data)))
        self.sal.subscribeCommand_enable(lambda commandId, data: self.controller.enqueue(EnableCommand(self.sal, commandId, data)))
        self.sal.subscribeCommand_disable(lambda commandId, data: self.controller.enqueue(DisableCommand(self.sal, commandId, data)))
        self.sal.subscribeCommand_standby(lambda commandId, data: self.controller.enqueue(StandbyCommand(self.sal, commandId, data)))

    def run(self):
        self.running = True
        while self.running:
            self.sal.runSubscriberChecks()
            time.sleep(0.001)

class ControllerThread(Thread):
    def __init__(self, controller):
        Thread.__init__(self)
        self.controller = controller

    def run(self):
        self.running = True
        while self.running:
            command = self.controller.dequeue()
            self.controller.execute(command)
            time.sleep(0.001)

class OuterLoopThread(Thread):
    def __init__(self, controller, loopTime):
        Thread.__init__(self)
        self.controller = controller
        self.loopTime = loopTime

    def run(self):
        self.running = True
        while self.running:
            self.controller.enqueue(UpdateCommand())
            time.sleep(self.loopTime)