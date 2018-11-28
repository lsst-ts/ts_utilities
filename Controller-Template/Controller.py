from queue import Queue

class Controller(object):
    def __init__(self, context):
        self.context = context
        self.queue = Queue()

    def clear(self):
        self.queue = Queue()

    def enqueue(self, command):
        valid = command.validate()
        if valid:
            self.queue.put(command)
        return valid

    def dequeue(self):
        return self.queue.get()

    def execute(self, command):
        command.ackInProgress()
        command.execute(self.context)