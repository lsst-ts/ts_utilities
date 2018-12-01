import logging
import Context
import queue
import Commands

class Controller(object):
    def __init__(self, context : Context.Context):
        self.log = logging.getLogger("Controller")
        self.context = context
        self.queue = queue.Queue()

    def clear(self):
        self.log.info("Clearing command queue.")
        self.queue = queue.Queue()

    def enqueue(self, command : Commands.Command):
        self.log.debug("Attempting to add %s to the command queue." % command.name)
        if command.validate():
            self.queue.put(command)

    def dequeue(self):
        return self.queue.get()

    def execute(self, command : Commands.Command):
        self.log.debug("Starting to execute %s." % command.name)
        command.ackInProgress()
        if isinstance(command, Commands.UpdateCommand):
            self.context.update(command)
        elif isinstance(command, Commands.BootCommand):
            self.context.boot(command)
{commandDefinitions}
        else:
            self.log.error("Unhandled command %s. Cannot execute." % command.name)