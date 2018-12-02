import logging
import {subsystem}Controller
import Model
import Context
import Controller
import Threads
import Commands

# This is for unit tests only since not all CSCs
# have a shutdown command
shutdownAction = None

def run():
    logging.basicConfig(format = "%(asctime)-15s %(threadName)-16s %(name)-10s %(levelname)-8s %(message)s")
    logging.getLogger("Command").setLevel(logging.INFO)
    logging.getLogger("Context").setLevel(logging.INFO)
    logging.getLogger("Controller").setLevel(logging.INFO)
    logging.getLogger("Model").setLevel(logging.INFO)
    logging.getLogger("State").setLevel(logging.INFO)
    logging.getLogger("Thread").setLevel(logging.DEBUG)
    logging.getLogger("Main").setLevel(logging.DEBUG)
    log = logging.getLogger("Main")
    log.info("Starting {subsystem} application.")
    log.info("Initializing {subsystem} SAL interface.")
    sal = {subsystem}Controller.{subsystem}Controller()
    log.info("Initializing {subsystem} model.")
    model = Model.Model(sal)
    global shutdownAction
    shutdownAction = model.triggerShutdown
    log.info("Initializing {subsystem} context.")
    context = Context.Context(sal, model)
    log.info("Initializing {subsystem} controller.")
    controller = Controller.Controller(context)
    log.info("Initializing {subsystem} controller thread.")
    controllerThread = Threads.ControllerThread(controller, 0.001)
    log.info("Initializing {subsystem} subscriber thread.")
    subscriberThread = Threads.SubscriberThread(sal, controller, 0.001)
    log.info("Initializing {subsystem} outer loop thread.")
    outerLoopThread = Threads.OuterLoopThread(controller, 0.050)
    log.info("Adding BootCommand for OfflineState to StandbyState transition.")
    controller.enqueue(Commands.BootCommand())
    log.info("Starting {subsystem} controller thread.")
    controllerThread.start()
    log.info("Starting {subsystem} subscriber thread.")
    subscriberThread.start()
    log.info("Starting {subsystem} outer loop thread.")
    outerLoopThread.start()
    log.info("{subsystem} is now running and waiting for shutdown.")
    model.waitForShutdown()
    log.info("{subsystem} has a shutdown request.")
    log.info("Stopping {subsystem} controller thread.")
    controllerThread.stop()
    controllerThread.join()
    log.info("Stopping {subsystem} subscriber thread.")
    subscriberThread.stop()
    subscriberThread.join()
    log.info("Stopping {subsystem} outer loop thread.")
    outerLoopThread.stop()
    outerLoopThread.join()
    log.info("Closing {subsystem} SAL interface.")
    sal.close()