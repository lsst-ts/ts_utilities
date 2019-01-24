import os

class SALPYGenerator:
    template = """# This file is part of {subsystem}.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.Controller

import time

import SALPY_{subsystem}


class {subsystem}Controller:
    def __init__(self, index=0):
        self.sal = SALPY_{subsystem}.SAL_{subsystem}(index)
        self.sal.setDebugLevel(0)
{controllerCommandInitializers}
{controllerEventInitializers}
{controllerTelemetryInitializers}
{controllerCommandSubscriptionInitializers}
{controllerEventPreviousDataInitializers}
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
{controllerCommandDefinitions}{controllerEventDefinitions}{controllerTelemetryDefinitions}

class {subsystem}Remote:
    def __init__(self, index=0):
        self.sal = SALPY_{subsystem}.SAL_{subsystem}(index)
        self.sal.setDebugLevel(0)
{remoteCommandInitializers}
{remoteEventInitializers}
{remoteTelemetryInitializers}
{remoteEventSubscriptionInitializers}
{remoteTelemetrySubscriptionInitializers}
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
{remoteCommandDefinitions}{remoteEventDefinitions}{remoteTelemetryDefinitions}"""
    
    def __init__(self, commands, events, telemetry, enumerations):
        self.commands = commands
        self.events = events
        self.telemetry = telemetry
        self.enumerations = enumerations
        self.subsystem = self.commands[0].subsystem

    def generate(self, outputDirectory):
        text = self.template.format(
            subsystem=self.commands[0].subsystem,
            controllerCommandInitializers=self.getControllerCommandInitializers(),
            controllerCommandSubscriptionInitializers=self.getControllerCommandSubscriptionInitializers(),
            controllerEventInitializers=self.getControllerEventInitializers(),
            controllerTelemetryInitializers=self.getControllerTelemetryInitializers(),
            controllerCommandDefinitions=self.getControllerCommandDefinitions(),
            controllerEventDefinitions=self.getControllerEventDefinitions(),
            controllerTelemetryDefinitions=self.getControllerTelemetryDefinitions(),
            emptyMap="{}",
            controllerEventPreviousDataInitializers=self.getControllerEventPreviousDataInitializers(),
            remoteCommandInitializers=self.getRemoteCommandInitializers(),
            remoteEventInitializers=self.getRemoteEventInitializers(),
            remoteTelemetryInitializers=self.getRemoteTelemetryInitializers(),
            remoteCommandDefinitions=self.getRemoteCommandDefinitions(),
            remoteEventDefinitions=self.getRemoteEventDefinitions(),
            remoteTelemetryDefinitions=self.getRemoteTelemetryDefinitions(),
            remoteEventSubscriptionInitializers=self.getRemoteEventSubscriptionInitializers(),
            remoteTelemetrySubscriptionInitializers=self.getRemoteTelemetrySubscriptionInitializers(),
        )
        path = os.path.join(outputDirectory, "salinterface.py")
        with open(path, "w") as file:  
            file.write(text)
            self.writePythonEnumerations(file, self.enumerations)

    def writePythonEnumerations(self, file, enumerations):
        items = {}
        for enumeration in enumerations:
            name = enumeration.name
            values = enumeration.values
            items[name] = []
            for value in values:
                items[name].append(value)
        format = """

class {name}:
{values}"""
        file.write("\n\n")
        file.write("class SummaryStates:\n")
        file.write("    OfflineState = SALPY_{subsystem}.SAL__STATE_OFFLINE\n".format(subsystem=self.subsystem))
        file.write("    StandbyState = SALPY_{subsystem}.SAL__STATE_STANDBY\n".format(subsystem=self.subsystem))
        file.write("    DisabledState = SALPY_{subsystem}.SAL__STATE_DISABLED\n".format(subsystem=self.subsystem))
        file.write("    EnabledState = SALPY_{subsystem}.SAL__STATE_ENABLED\n".format(subsystem=self.subsystem))
        file.write("    FaultState = SALPY_{subsystem}.SAL__STATE_FAULT\n".format(subsystem=self.subsystem))
        for item in items:
            if item == "SummaryStates":
                continue
            name = item
            values = items[item]
            itemFormat = "    {value} = SALPY_{subsystem}.{subsystem}_shared_{name}_{value}"
            if "Flags" in name or "IndexMap" in name:
                itemFormat = itemFormat + " - 1"
            itemFormat = itemFormat + "\n"
            textValues = ""
            for value in values:
                textValues = textValues + itemFormat.format(value=value, subsystem=self.subsystem, name=name)
            file.write(format.format(name=name, values=textValues))

    def getControllerCommandInitializers(self):
        template = "        self.sal.salProcessor(\"{subsystem}_command_{name}\")\n"
        result = ""
        for command in self.commands:
            result = result + template.format(subsystem = command.subsystem, name = command.name)
        return result

    def getControllerCommandSubscriptionInitializers(self):
        template = "        self.commandSubscribers_{name} = []\n"
        result = ""
        for event in self.commands:
            result = result + template.format(name = event.name)
        return result

    def getControllerCommandDefinitions(self):
        template = """
    def acceptCommand_{name}(self):
        data = SALPY_{subsystem}.{subsystem}_command_{name}C()
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
            
    def getControllerEventInitializers(self):
        template = "        self.sal.salEventPub(\"{subsystem}_logevent_{name}\")\n"
        result = ""
        for event in self.events:
            result = result + template.format(subsystem = event.subsystem, name = event.name)
        return result

    def getControllerEventPreviousDataInitializers(self):
        template = "        self.previousEvent_{name} = SALPY_{subsystem}.{subsystem}_logevent_{name}C()\n"
        result = ""
        for event in self.events:
            result = result + template.format(subsystem = event.subsystem, name = event.name)
        return result

    def getControllerEventDefinitions(self):
        template = """
    def logEvent_{name}(self, {parameters}, priority=0):
        data = SALPY_{subsystem}.{subsystem}_logevent_{name}C()
{setParameters}
        self.previousEvent_{name} = data
        return self.sal.logEvent_{name}(data, priority)

    def tryLogEvent_{name}(self, {parameters}, priority=0):
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
    
    def getControllerTelemetryInitializers(self):
        template = "        self.sal.salTelemetryPub(\"{subsystem}_{name}\")\n"
        result = ""
        for telemetry in self.telemetry:
            result = result + template.format(subsystem = telemetry.subsystem, name = telemetry.name)
        return result

    def getControllerTelemetryDefinitions(self):
        template = """
    def putSample_{name}(self, {parameters}):
        data = SALPY_{subsystem}.{subsystem}_{name}C()
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

    def getRemoteCommandInitializers(self):
        template = "        self.sal.salCommand(\"{subsystem}_command_{name}\")\n"
        result = ""
        for command in self.commands:
            result = result + template.format(subsystem = command.subsystem, name = command.name)
        return result

    def getRemoteCommandDefinitions(self):
        template = """
    def issueCommand_{name}(self, {parameters}):
        data = SALPY_{subsystem}.{subsystem}_command_{name}C()
{setParameters}
        return self.sal.issueCommand_{name}(data)

    def getResponse_{name}(self):
        data = SALPY_{subsystem}.{subsystem}_ackcmdC()
        result = self.sal.getResponse_{name}(data)
        return result, data

    def waitForCompletion_{name}(self, cmdId, timeoutInSeconds=10):
        waitResult = self.sal.waitForCompletion_{name}(cmdId, timeoutInSeconds)
        #ackResult, ack = self.getResponse_{name}()
        #return waitResult, ackResult, ack
        return waitResult

    def issueCommandThenWait_{name}(self, {parameters}, timeoutInSeconds=10):
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
            
    def getRemoteEventInitializers(self):
        template = "        self.sal.salEvent(\"{subsystem}_logevent_{name}\")\n"
        result = ""
        for event in self.events:
            result = result + template.format(subsystem = event.subsystem, name = event.name)
        return result
        
    def getRemoteEventSubscriptionInitializers(self):
        template = "        self.eventSubscribers_{name} = []\n"
        result = ""
        for event in self.events:
            result = result + template.format(name = event.name)
        return result

    def getRemoteEventDefinitions(self):
        template = """
    def getNextEvent_{name}(self):
        data = SALPY_{subsystem}.{subsystem}_logevent_{name}C()
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
    
    def getRemoteTelemetryInitializers(self):
        template = "        self.sal.salTelemetrySub(\"{subsystem}_{name}\")\n"
        result = ""
        for telemetry in self.telemetry:
            result = result + template.format(subsystem = telemetry.subsystem, name = telemetry.name)
        return result
        
    def getRemoteTelemetrySubscriptionInitializers(self):
        template = "        self.telemetrySubscribers_{name} = []\n"
        result = ""
        for telemetry in self.telemetry:
            result = result + template.format(name = telemetry.name)
        return result

    def getRemoteTelemetryDefinitions(self):
        template = """
    def getNextSample_{name}(self):
        data = SALPY_{subsystem}.{subsystem}_{name}C()
        result = self.sal.getNextSample_{name}(data)
        return result, data

    def getSample_{name}(self):
        data = SALPY_{subsystem}.{subsystem}_{name}C()
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