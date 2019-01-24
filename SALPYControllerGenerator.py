import os

class SALPYControllerGenerator:
    template = """import time
from SALPY_{subsystem} import *

class {subsystem}Controller:
    def __init__(self, index = 0):
        self.sal = SAL_{subsystem}(index)
        self.sal.setDebugLevel(0)
{commandInitializers}
{eventInitializers}
{telemetryInitializers}
{commandSubscriptionInitializers}
{eventPreviousDataInitializers}
        self.topicsSubscribedToo = {emptyMap}

    def close(self):
        time.sleep(1)
        self.sal.salShutdown()

    def flush(self, action):
        result, data = action()
        while result >= 0:
            result, data = action()
            
    def checkForSubscriber(self, action, subscribers):
        result, data = action()
        if result > 0:
            for subscriber in subscribers:
                subscriber(result, data)
            
    def runSubscriberChecks(self):
        for subscribedTopic in self.topicsSubscribedToo:
            action = self.topicsSubscribedToo[subscribedTopic][0]
            subscribers = self.topicsSubscribedToo[subscribedTopic][1]
            self.checkForSubscriber(action, subscribers)

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
        text = self.template.format(subsystem = self.commands[0].subsystem, commandInitializers = self.getCommandInitializers(), commandSubscriptionInitializers = self.getCommandSubscriptionInitializers(), eventInitializers = self.getEventInitializers(), telemetryInitializers = self.getTelemetryInitializers(), commandDefinitions = self.getCommandDefinitions(), eventDefinitions = self.getEventDefinitions(), telemetryDefinitions = self.getTelemetryDefinitions(), emptyMap = "{}", eventPreviousDataInitializers = self.getEventPreviousDataInitializers())
        path = os.path.join(outputDirectory, "%sController.py" % (self.commands[0].subsystem))
        with open(path, "w") as file:  
            file.write(text)

    def getCommandInitializers(self):
        template = "        self.sal.salProcessor(\"{subsystem}_command_{name}\")\n"
        result = ""
        for command in self.commands:
            result = result + template.format(subsystem = command.subsystem, name = command.name)
        return result

    def getCommandSubscriptionInitializers(self):
        template = "        self.commandSubscribers_{name} = []\n"
        result = ""
        for event in self.commands:
            result = result + template.format(name = event.name)
        return result

    def getCommandDefinitions(self):
        template = """
    def acceptCommand_{name}(self):
        data = {subsystem}_command_{name}C()
        result = self.sal.acceptCommand_{name}(data)
        return result, data

    def ackCommand_{name}(self, cmdId, ackCode, errorCode, description):
        return self.sal.ackCommand_{name}(cmdId, ackCode, errorCode, description)

    def subscribeCommand_{name}(self, action):
        self.commandSubscribers_{name}.append(action)
        if "command_{name}" not in self.topicsSubscribedToo:
            self.topicsSubscribedToo["command_{name}"] = [self.acceptCommand_{name}, self.commandSubscribers_{name}]
"""
        result = ""
        for command in self.commands:
            result = result + template.format(subsystem = command.subsystem, name = command.name)
        return result
            
    def getEventInitializers(self):
        template = "        self.sal.salEventPub(\"{subsystem}_logevent_{name}\")\n"
        result = ""
        for event in self.events:
            result = result + template.format(subsystem = event.subsystem, name = event.name)
        return result

    def getEventPreviousDataInitializers(self):
        template = "        self.previousEvent_{name} = {subsystem}_logevent_{name}C()\n"
        result = ""
        for event in self.events:
            result = result + template.format(subsystem = event.subsystem, name = event.name)
        return result

    def getEventDefinitions(self):
        template = """
    def logEvent_{name}(self, {parameters}, priority = 0):
        data = {subsystem}_logevent_{name}C()
{setParameters}
        self.previousEvent_{name} = data
        return self.sal.logEvent_{name}(data, priority)

    def tryLogEvent_{name}(self, {parameters}, priority = 0):
        anythingChanged = False
{checkParameters}
        if anythingChanged:
            return self.logEvent_{name}({parameters}, priority)
        return 0
"""
        parameterTemplate = "{name}, "
        setParameterTemplate = "        data.{name} = {name}\r\n"
        setArrayParameterTemplate = """        for i in range({count}):
            data.{name}[i] = {name}[i]
"""
        checkParameterTemplate = "        anythingChanged = anythingChanged or self.previousEvent_{eventName}.{parameterName} != {parameterName}\r\n"
        checkArrayParameterTemplate = """        for i in range({count}):
            anythingChanged = anythingChanged or self.previousEvent_{eventName}.{parameterName}[i] != {parameterName}[i]
"""
        result = ""
        for event in self.events:
            parameters = ""
            setParameters = ""
            checkParameters = ""
            for parameter in event.parameters:
                parameters = parameters + parameterTemplate.format(name = parameter.name)
                if int(parameter.count) > 1 and parameter.type != "string":
                    setParameters = setParameters + setArrayParameterTemplate.format(name = parameter.name, count = parameter.count)
                    checkParameters = checkParameters + checkArrayParameterTemplate.format(eventName = event.name, parameterName = parameter.name, count = parameter.count)
                else:
                    setParameters = setParameters + setParameterTemplate.format(name = parameter.name)
                    checkParameters = checkParameters + checkParameterTemplate.format(eventName = event.name, parameterName = parameter.name)
            result = result + template.format(subsystem = event.subsystem, name = event.name, parameters = parameters[:-2], setParameters = setParameters, checkParameters = checkParameters)
        return result
    
    def getTelemetryInitializers(self):
        template = "        self.sal.salTelemetryPub(\"{subsystem}_{name}\")\n"
        result = ""
        for telemetry in self.telemetry:
            result = result + template.format(subsystem = telemetry.subsystem, name = telemetry.name)
        return result

    def getTelemetryDefinitions(self):
        template = """
    def putSample_{name}(self, {parameters}):
        data = {subsystem}_{name}C()
{setParameters}
        return self.sal.putSample_{name}(data)
"""
        parameterTemplate = "{name}, "
        setParameterTemplate = "        data.{name} = {name}\r\n"
        setArrayParameterTemplate = """        for i in range({count}):
            data.{name}[i] = {name}[i]
"""
        result = ""
        for telem in self.telemetry:
            parameters = ""
            setParameters = ""
            for parameter in telem.parameters:
                parameters = parameters + parameterTemplate.format(name = parameter.name)
                if int(parameter.count) > 1 and parameter.type != "string":
                    setParameters = setParameters + setArrayParameterTemplate.format(name = parameter.name, count = parameter.count)
                else:
                    setParameters = setParameters + setParameterTemplate.format(name = parameter.name)
            result = result + template.format(subsystem = telem.subsystem, name = telem.name, parameters = parameters[:-2], setParameters = setParameters)
        return result