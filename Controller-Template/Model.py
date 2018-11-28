from queue import Queue

class Model(object):
    def __init__(self, sal):
        self.sal = sal
        self.shutdown = Queue()

    def getSAL(self):
        return self.sal

    def waitForShutdown(self):
        self.shutdown.get()

    def triggerShutdown(self):
        self.shutdown.put(0)