from SALCommand import *
from SALEvent import *
from SALTelemetry import *
from SALParameter import *
from SALEnumeration import *
import xml.etree.ElementTree

globalCommands = ["abort", "enable", "disable", "standby", "exitControl", "start", "enterControl", "setValue"]
globalEvents = ["settingVersions", "errorCode", "summaryState", "appliedSettingsMatchStart"]
salTypes = ["short", "long", "long long", "unsigned short", "unsigned long", "unsigned long long", "float", "double", "char", "boolean", "octet", "string", "byte", "int"]

class UMLXMLParser:       
    def parse(self, subsystem, version, umlFile):
        self.subsystem = subsystem
        self.version = version
        self.prepareFile(umlFile)
        return self.getCommands(), self.getEvents(), self.getTelemetry(), self.getEnumerations()

    def prepareFile(self, umlFile):
        tempUMLFile = umlFile + ".tmp"
        with open(tempUMLFile, "w") as tempFile:
            with open(umlFile, "r") as inputFile:
                for line in inputFile:
                    tempFile.write(line.replace("<UML:", "<").replace("</UML:", "</").replace("xmi:id","xmiid").replace("xmi:Extension", "xmiExtension").replace("xmi:type", "xmitype"))
        self.uml = xml.etree.ElementTree.parse(tempUMLFile)

    def getCommands(self):
        commands = {}
        for item in self.getCommandList():
            commands[item] = self.createSALCommand(item)
            
        result = []
        for command in sorted([x for x in commands]):
            result.append(commands[command])
        return result
        
    def getEvents(self):
        events = {}
        for item in self.getEventList():
            events[item] = self.createSALEvent(item)

        result = []
        for event in sorted([x for x in events]):
            result.append(events[event])
        return result
        
    def getTelemetry(self):
        telemetry = {}
        for item in self.getTelemetryList():
            telemetry[item] = self.createSALTelemetry(item)
        result = []
        for telem in sorted([x for x in telemetry]):
            result.append(telemetry[telem])
        return result

    def getEnumerations(self):
        enumerations = {}
        for item in self.getEnumerationList():
            enumerations[item] = self.createSALEnumeration(item)
        result = []
        for enumeration in sorted([x for x in enumerations]):
            result.append(enumerations[enumeration])
        return result
        
    def createSALCommand(self, command):
        basePath = ".//packagedElement[@name='SAL interface']/packagedElement[@name='Command']/packagedElement[@name='%s']/ownedAttribute" % (command)
        author = ""
        parameters = []
        for parameter in self.getCommandParameterList(command):
            parameters.append(self.createSALParameter("Command", command, parameter))
        return SALCommand(self.subsystem, self.version, author, command, parameters)
        
    def createSALEvent(self, event):
        basePath = ".//packagedElement[@name='SAL interface']/packagedElement[@name='Event']/packagedElement[@name='%s']/ownedAttribute" % (event)
        author = ""
        parameters = []
        for parameter in self.getEventParameterList(event):
            parameters.append(self.createSALParameter("Event", event, parameter))
        return SALEvent(self.subsystem, self.version, author, event, parameters)
        
    def createSALTelemetry(self, telemetry):
        basePath = ".//packagedElement[@name='SAL interface']/packagedElement[@name='Telemetry']/packagedElement[@name='%s']/ownedAttribute" % (telemetry)
        author = ""
        parameters = []
        for parameter in self.getTelemetryParameterList(telemetry):
            parameters.append(self.createSALParameter("Telemetry", telemetry, parameter))
        return SALTelemetry(self.subsystem, self.version, author, telemetry, parameters)

    def createSALEnumeration(self, enumeration):
        name = enumeration
        values = self.getEnumerationValues(name)
        return SALEnumeration(name, values)

    def createSALParameter(self, type, command, parameter):
        basePath = ".//packagedElement[@name='SAL interface']/packagedElement[@name='%s']/packagedElement[@name='%s']/ownedAttribute[@name='%s']%s" % (type, command, parameter,'%s')
        typePath = basePath % "/type/xmiExtension/referenceExtension"
        description = ""
        type = self.getValueByName(self.uml.find(typePath), "referentPath", "UNDEFINED")
        
        if type is "UNDEFINED":
            typeID = self.getValueByName(self.uml.find(basePath % ""), "type", "UNDEFINED")
            type = self.typeIDtoType(typeID)
        else:
            length = len(type)
            lastIndex = type.rfind(':')
            type = type[-(length-lastIndex-1):] 

        units = self.uml.find(basePath % "/defaultValue/body")
        if units is not None:
            units = units.text
        units = "" if units is None else units
		
        if type == "string":
            count = self.getValueByName(self.uml.find(basePath % "/upperValue"),"value", "1")
            return SALParameterString(parameter, description, type, units, count)
        elif type in salTypes:
            count = self.getValueByName(self.uml.find(basePath % "/upperValue"),"value", "1")
            return SALParameter(parameter, description, type, units, count)
        elif self.typeIsEnumeration(type):
            count = self.getValueByName(self.uml.find(basePath % "/upperValue"),"value", "1")
            return SALParameterEnumeration(parameter, description, type, units, count)
        else:
            print("BAD TYPE: %s" % type)
            self.error = True
            return 0
                    
    def getCommandList(self):
        return [command.get("name") for command in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Command']/packagedElement")]
  
    def getCommandParameterList(self, command):
        return [parameter.get("name") for parameter in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Command']/packagedElement[@name='%s']/ownedAttribute" % command)]

    def getEventList(self):
        return [event.get("name") for event in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Event']/packagedElement")]
        
    def getEventParameterList(self, event):
        return [parameter.get("name") for parameter in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Event']/packagedElement[@name='%s']/ownedAttribute" % event)]
                
    def getTelemetryList(self):
        return [telemetry.get("name") for telemetry in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Telemetry']/packagedElement")]
        
    def getTelemetryParameterList(self, telemetry):
        return [parameter.get("name") for parameter in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Telemetry']/packagedElement[@name='%s']/ownedAttribute" % telemetry)]      
        
    def getEnumerationList(self):
        return [enum.get("name") for enum in self.uml.findall(".//packagedElement[@name='Enumerations']/packagedElement[@xmitype='uml:Enumeration']")]
        
    def getEnumerationValues(self, enumeration):
        return [value.get("name") for value in self.uml.findall(".//packagedElement[@name='Enumerations']/packagedElement[@name='%s']/ownedLiteral" % enumeration)]

    def getValue(self, node, default):
        return node.get("value") if node is not None else default

    def getValueByName(self, node, value, default):
        return node.get(value) if node is not None else default

    def typeIDtoType(self, typeID):
        path = ".//packagedElement[@name='IDL Datatype']/packagedElement[@xmiid='%s']" % typeID 
        node = self.uml.find(path)
        if node is not None:
            return node.get("name")
        else:
            path = ".//packagedElement[@name='Enumerations']/packagedElement[@xmiid='%s']" % typeID
            node = self.uml.find(path)
            if node is not None:
                return node.get("name")
            else:
                return "UNKNOWN"
        
    def typeIsEnumeration(self, name):
        path = ".//packagedElement[@name='Enumerations']/packagedElement[@name='%s']" % name
        node = self.uml.find(path)
        return node.get("xmitype") == "uml:Enumeration" if node is not None else False     
