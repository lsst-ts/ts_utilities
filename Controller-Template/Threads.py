import logging
import threading
import {subsystem}Controller
import Controller
import Commands
import time

class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = type(self).__name__)
        self.log = logging.getLogger("Thread")
        self.running = False

    def stop(self):
        self.log.info("Stopping thread %s." % self.name)
        self.running = False

class SubscriberThread(Thread):
    def __init__(self, sal : {subsystem}Controller.{subsystem}Controller, controller : Controller.Controller, loopTimeInSec : float):
        Thread.__init__(self)
        self.sal = sal
        self.controller = controller
        self.loopTimeInSec = loopTimeInSec
{commandDefinitions}

    def run(self):
        self.log.info("Starting thread %s." % self.name)
        self.running = True
        while self.running:
            self.sal.runSubscriberChecks()
            time.sleep(self.loopTimeInSec)
        self.log.info("Thread %s completed." % self.name)

class ControllerThread(Thread):
    def __init__(self, controller : Controller.Controller, loopTimeInSec : float):
        Thread.__init__(self)
        self.controller = controller
        self.loopTimeInSec = loopTimeInSec

    def run(self):
        self.log.info("Starting thread %s." % self.name)
        self.running = True
        while self.running:
            command = self.controller.dequeue()
            self.controller.execute(command)
            time.sleep(self.loopTimeInSec)
        self.log.info("Thread %s completed." % self.name)

class OuterLoopThread(Thread):
    def __init__(self, controller : Controller.Controller, loopTimeInSec : float):
        Thread.__init__(self)
        self.controller = controller
        self.loopTimeInSec = loopTimeInSec

    def run(self):
        self.log.info("Starting thread %s." % self.name)
        self.running = True
        while self.running:
            self.controller.enqueue(Commands.UpdateCommand())
            time.sleep(self.loopTimeInSec)
        self.log.info("Thread %s completed." % self.name)