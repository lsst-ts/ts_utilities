import logging
import {subsystem}Controller
import queue
import time

class Model(object):
    def __init__(self, sal : {subsystem}Controller.{subsystem}Controller):
        self.log = logging.getLogger("Model")
        self.sal = sal
        self.shutdown = queue.Queue()
        self.lastOuterLoop = 0

    def getSAL(self):
        return self.sal

    def waitForShutdown(self):
        self.log.info("Waiting for shutdown.")
        self.shutdown.get()

    def triggerShutdown(self):
        self.log.info("Triggering shutdown.")
        self.shutdown.put(0)

    def outerLoop(self):
        current = time.time()
        self.log.debug("Outer loop execution time %0.4f" % (current - self.lastOuterLoop))
        self.lastOuterLoop = current