import os

class SALPYRemoteGenerator:
    template = """import time
from SALPY_{subsystem} import *

class {subsystem}Remote:
    def __init__(self, index = 0):
        self.sal = SAL_{subsystem}(index)
        self.sal.setDebugLevel(0)
{commandInitializers}
{eventInitializers}
{telemetryInitializers}
{eventSubscriptionInitializers}
{telemetrySubscriptionInitializers}
        self.topicsSubscribedToo = {emptyMap}

    def close(self):
        time.sleep(1)
        self.sal.salShutdown()

    def flush(self, action):
        result, data = action()
        while result >= 0:
            result, data = action()
            
    def checkForSubscriber(self, action, subscribers):
        buffer = []
        result, data = action()
        while result == 0:
            buffer.append(data)
            result, data = action()
        if len(buffer) > 0:
            for subscriber in subscribers:
                subscriber(buffer)
            
    def runSubscriberChecks(self):
        for subscribedTopic in self.topicsSubscribedToo:
            action = self.topicsSubscribedToo[subscribedTopic][0]
            subscribers = self.topicsSubscribedToo[subscribedTopic][1]
            self.checkForSubscriber(action, subscribers)
            
    def getEvent(self, action):
        lastResult, lastData = action()
        while lastResult >= 0:
            result, data = action()
            if result >= 0:
                lastResult = result
                lastData = data
            elif result < 0:
                break
        return lastResult, lastData

    def getTimestamp(self):
        return self.sal.getCurrentTime()

{commandDefinitions}

{eventDefinitions}

{telemetryDefinitions}
"""
    def __init__(self, commands, events, telemetry):
        self.commands = commands
        self.events = events
        self.telemetry = telemetry

    def generate(self, outputDirectory):
        text = self.template.format(subsystem = self.commands[0].subsystem, commandInitializers = self.getCommandInitializers(), eventInitializers = self.getEventInitializers(), telemetryInitializers = self.getTelemetryInitializers(), commandDefinitions = self.getCommandDefinitions(), eventDefinitions = self.getEventDefinitions(), telemetryDefinitions = self.getTelemetryDefinitions(), eventSubscriptionInitializers = self.getEventSubscriptionInitializers(), telemetrySubscriptionInitializers = self.getTelemetrySubscriptionInitializers(), emptyMap = "{}")
        path = os.path.join(outputDirectory, "%sRemote.py" % (self.commands[0].subsystem))
        with open(path, "w") as file:  
            file.write(text)

    def getCommandInitializers(self):
        template = "        self.sal.salCommand(\"{subsystem}_command_{name}\")\n"
        result = ""
        for command in self.commands:
            result = result + template.format(subsystem = command.subsystem, name = command.name)
        return result

    def getCommandDefinitions(self):
        template = """
    def issueCommand_{name}(self, {parameters}):
        data = {subsystem}_command_{name}C()
{setParameters}
        return self.sal.issueCommand_{name}(data)

    def getResponse_{name}(self):
        data = {subsystem}_ackcmdC()
        result = self.sal.getResponse_{name}(data)
        return result, data
        
    def waitForCompletion_{name}(self, cmdId, timeoutInSeconds = 10):
        waitResult = self.sal.waitForCompletion_{name}(cmdId, timeoutInSeconds)
        #ackResult, ack = self.getResponse_{name}()
        #return waitResult, ackResult, ack
        return waitResult
        
    def issueCommandThenWait_{name}(self, {parameters}, timeoutInSeconds = 10):
        cmdId = self.issueCommand_{name}({parameters})
        return self.waitForCompletion_{name}(cmdId, timeoutInSeconds)
"""

        parameterTemplate = "{name}, "
        setParameterTemplate = "        data.{name} = {name}\r\n"
        setArrayParameterTemplate = """        for i in range({count}):
            data.{name}[i] = {name}[i]
"""
        result = ""
        for command in self.commands:
            parameters = ""
            setParameters = ""
            for parameter in command.parameters:
                parameters = parameters + parameterTemplate.format(name = parameter.name)
                if int(parameter.count) > 1 and parameter.type != "string":
                    setParameters = setParameters + setArrayParameterTemplate.format(name = parameter.name, count = parameter.count)
                else:
                    setParameters = setParameters + setParameterTemplate.format(name = parameter.name)
            result = result + template.format(subsystem = command.subsystem, name = command.name, parameters = parameters[:-2], setParameters = setParameters)
        return result
            
    def getEventInitializers(self):
        template = "        self.sal.salEvent(\"{subsystem}_logevent_{name}\")\n"
        result = ""
        for event in self.events:
            result = result + template.format(subsystem = event.subsystem, name = event.name)
        return result
        
    def getEventSubscriptionInitializers(self):
        template = "        self.eventSubscribers_{name} = []\n"
        result = ""
        for event in self.events:
            result = result + template.format(name = event.name)
        return result

    def getEventDefinitions(self):
        template = """
    def getNextEvent_{name}(self):
        data = {subsystem}_logevent_{name}C()
        result = self.sal.getEvent_{name}(data)
        return result, data
        
    def getEvent_{name}(self):
        return self.getEvent(self.getNextEvent_{name})
        
    def subscribeEvent_{name}(self, action):
        self.eventSubscribers_{name}.append(action)
        if "event_{name}" not in self.topicsSubscribedToo:
            self.topicsSubscribedToo["event_{name}"] = [self.getNextEvent_{name}, self.eventSubscribers_{name}]
"""

        result = ""
        for event in self.events:
            result = result + template.format(subsystem = event.subsystem, name = event.name)
        return result
    
    def getTelemetryInitializers(self):
        template = "        self.sal.salTelemetrySub(\"{subsystem}_{name}\")\n"
        result = ""
        for telemetry in self.telemetry:
            result = result + template.format(subsystem = telemetry.subsystem, name = telemetry.name)
        return result
        
    def getTelemetrySubscriptionInitializers(self):
        template = "        self.telemetrySubscribers_{name} = []\n"
        result = ""
        for telemetry in self.telemetry:
            result = result + template.format(name = telemetry.name)
        return result

    def getTelemetryDefinitions(self):
        template = """
    def getNextSample_{name}(self):
        data = {subsystem}_{name}C()
        result = self.sal.getNextSample_{name}(data)
        return result, data

    def getSample_{name}(self):
        data = {subsystem}_{name}C()
        result = self.sal.getSample_{name}(data)
        return result, data
        
    def subscribeTelemetry_{name}(self, action):
        self.telemetrySubscribers_{name}.append(action)
        if "telemetry_{name}" not in self.topicsSubscribedToo:
            self.topicsSubscribedToo["telemetry_{name}"] = [self.getNextSample_{name}, self.telemetrySubscribers_{name}]
"""

        result = ""
        for telemetry in self.telemetry:
            result = result + template.format(subsystem = telemetry.subsystem, name = telemetry.name)
        return result