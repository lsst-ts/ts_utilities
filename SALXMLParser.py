from SALCommand import *
from SALEvent import *
from SALTelemetry import *
from SALParameter import *
from SALEnumeration import *
import xml.etree.ElementTree

class SALXMLParser:
    def parse(self, genericsPath, commandsPath, eventsPath, telemetryPath):
        return self.parseCommands(commandsPath, genericsPath), self.parseEvents(eventsPath, genericsPath), self.parseTelemetry(telemetryPath, genericsPath), self.parseEnumerations(eventsPath)

    def parseCommands(self, commandsPath, genericsPath):
        generics = self.parseItem(genericsPath, ".//SALCommand", lambda subsystem, version, author, name, parameters: SALCommand(subsystem, version, author, name, parameters))
        commands = self.parseItem(commandsPath, ".//SALCommand", lambda subsystem, version, author, name, parameters: SALCommand(subsystem, version, author, name, parameters))
        for generic in generics:
            generic.subsystem = commands[0].subsystem
        return generics + commands

    def parseEvents(self, eventsPath, genericsPath):
        generics = self.parseItem(genericsPath, ".//SALEvent", lambda subsystem, version, author, name, parameters: SALEvent(subsystem, version, author, name, parameters))
        events = self.parseItem(eventsPath, ".//SALEvent", lambda subsystem, version, author, name, parameters: SALEvent(subsystem, version, author, name, parameters))
        for generic in generics:
            generic.subsystem = events[0].subsystem
        return generics + events

    def parseTelemetry(self, telemetryPath, genericsPath):
        generics = self.parseItem(genericsPath, ".//SALTelemetry", lambda subsystem, version, author, name, parameters: SALTelemetry(subsystem, version, author, name, parameters))
        telemetry = self.parseItem(telemetryPath, ".//SALTelemetry", lambda subsystem, version, author, name, parameters: SALTelemetry(subsystem, version, author, name, parameters))
        for generic in generics:
            generic.subsystem = telemetry[0].subsystem
        return generics + telemetry

    def parseEnumerations(self, path):
        tree = xml.etree.ElementTree.parse(path)
        enumerations = []
        for item in tree.findall(".//Enumeration"):
            fullValues = item.text.split(",")
            tokens = fullValues[0].split("_")
            name = tokens[0]
            values = ["_".join(x.split("_")[1:]) for x in fullValues]
            enumerations.append(SALEnumeration(name, values))
        return enumerations
        
    def parseItem(self, path, element, factory):
        tree = xml.etree.ElementTree.parse(path)
        items = []
        for item in tree.findall(element):
            subsystem = item.find(".//Subsystem").text
            version = item.find(".//Version").text
            author = item.find(".//Author").text
            name = item.find(".//EFDB_Topic").text.split("_")[-1]
            parameters = []
            for parameter in item.findall(".//item"):
                parameterName = parameter.find(".//EFDB_Name").text
                parameterDescription = parameter.find(".//Description").text
                parameterType = parameter.find(".//IDL_Type").text
                parameterUnits = parameter.find(".//Units").text
                parameterCount = parameter.find(".//Count").text
                if parameterType == "string":
                    parameters.append(SALParameterString(parameterName, parameterDescription, parameterType, parameterUnits, parameterCount))
                else:
                    parameters.append(SALParameter(parameterName, parameterDescription, parameterType, parameterUnits, parameterCount))
            items.append(factory(subsystem, version, author, name, parameters))
        return items