from {subsystem}Controller import {subsystem}Controller
from Model import Model
from Context import Context
from Controller import Controller
from Threads import SubscriberThread, ControllerThread, OuterLoopThread
from Commands import BootCommand

print("Main: Starting SAL")
sal = {subsystem}Controller()
print("Main: Model")
model = Model(sal)
print("Main: Context")
context = Context(sal, model)
print("Main: Controller")
controller = Controller(context)
print("Main: Controller Thread")
controllerThread = ControllerThread(controller)
print("Main: Subscriber Thread")
subscriberThread = SubscriberThread(sal, controller)
print("Main: Outer Loop Thread")
outerLoopThread = OuterLoopThread(controller, 0.050)
controllerThread.start()
subscriberThread.start()
outerLoopThread.start()
print("Main: Adding boot command")
controller.enqueue(BootCommand())
print("Main: Waiting for shutdown")
model.waitForShutdown()
print("Main: Shutdown")
outerLoopThread.stop()
subscriberThread.stop()
controllerThread.stop()
print("Main: Closing SAL")
sal.close()