import os
import sys
import xml.etree.ElementTree

ignoreGlobals = True
isForLabVIEW = False
globalCommands = ["abort", "enable", "disable", "standby", "exitControl", "start", "enterControl", "setValue"]
globalEvents = ["settingVersions", "errorCode", "summaryState", "appliedSettingsMatchStart"]
salTypes = ["short", "long", "long long", "unsigned short", "unsigned long", "unsigned long long", "float", "double", "char", "boolean", "octet", "string", "byte", "int"]

class UMLXMLParser:
    def __init__(self):
        self.error = False

    def Open(self, subsystem, version, umlFile):
        print("Creating temporary file")
        tempUMLFile = umlFile + ".tmp"
        print(tempUMLFile)
        with open(tempUMLFile, "w") as tempFile:
            with open(umlFile, "r") as inputFile:
                for line in inputFile:
                    tempFile.write(line.replace("<UML:", "<").replace("</UML:", "</").replace("xmi:id","xmiid").replace("xmi:Extension", "xmiExtension").replace("xmi:type", "xmitype"))

        self.subsystem = subsystem
        self.version = version
        self.uml = xml.etree.ElementTree.parse(tempUMLFile)
        
    def Parse(self, outputDirectory):
        print("Parsing temporary file")       
        self.outputDirectory = outputDirectory
        commands = self.GetCommands()
        events = self.GetEvents()
        telemetry = self.GetTelemetry()
        self.WriteCommands(commands)
        self.WriteEvents(self.GetEnumerationList(), events)
        self.WriteTelemetry(telemetry)
        self.salpywrapper = SALPYWrapper()
        for command in commands:
            self.salpywrapper.addCommand(command)
        for event in events:
            self.salpywrapper.addEvent(event)
        for telem in telemetry:
            self.salpywrapper.addTelemetry(telem)
        path = os.path.join(self.outputDirectory, "%s.py" % (self.subsystem))
        with open(path, "w") as wrapperFile:
            wrapperFile.write(self.salpywrapper.getClass())
        self.WriteCPPEnumerations()
        if self.error:
            print("ERROR DURING PARSING")
        else:
            print("Completed succesfully")
        
    def WriteCommands(self, commands):
        header = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="http://lsst-sal.tuc.noao.edu/schema/SALCommandSet.xsl"?>
<SALCommandSet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://lsst-sal.tuc.noao.edu/schema/SALCommandSet.xsd">"""
        footer = "\n</SALCommandSet>"
        path = os.path.join(self.outputDirectory, "%s_Commands.xml" % (self.subsystem))
        with open(path, "w") as commandFile:  
            commandFile.write(header)
            for item in commands:
                if item.name != "Command":
                    print("Writing command %s" % item.name)
                    if not (ignoreGlobals and item.name in globalCommands):
                        commandFile.write(item.CreateSALXML())
            commandFile.write(footer)          
            
    def WriteEvents(self, enumerations, events):
        header = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="http://lsst-sal.tuc.noao.edu/schema/SALEventSet.xsl"?>
<SALEventSet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://lsst-sal.tuc.noao.edu/schema/SALEventSet.xsd">"""
        footer = "\n</SALEventSet>"
        path = os.path.join(self.outputDirectory, "%s_Events.xml" % (self.subsystem))
        with open(path, "w") as eventFile:  
            eventFile.write(header)
            eventFile.write("\n")
            print("enumerations: %s " % enumerations)
            for item in enumerations:
                values = self.GetEnumerationValues("", item)
                if len(values) > 0:
                    eventFile.write("    <Enumeration>%s</Enumeration>\n" % (self.GetEnumerationValues("", item)))
            for item in events:
                if item.name != "Event":
                    print("Writing event %s" % item.name)
                    if not (ignoreGlobals and item.name in globalEvents):
                        try:
                            eventFile.write(item.CreateSALXML())
                        except Exception as e: 
                            print(item.CreateSALXML())
                            print("Possible error for documentation in model for: %s", item.name)
                            print(e)
                            exit()
            eventFile.write(footer)     

    def WriteTelemetry(self, telemetry):
        header = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="http://lsst-sal.tuc.noao.edu/schema/SALTelemetrySet.xsl"?>
<SALTelemetrySet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://lsst-sal.tuc.noao.edu/schema/SALTelemetrySet.xsd">"""
        footer = "\n</SALTelemetrySet>"
        path = os.path.join(self.outputDirectory, "%s_Telemetry.xml" % (self.subsystem))
        with open(path, "w") as telemetryFile:  
            telemetryFile.write(header)
            for item in telemetry:
                if item.name != "Telemetry":
                    print("Writing telemetry %s" % item.name)
                    telemetryFile.write(item.CreateSALXML())
            telemetryFile.write(footer)   

    def WriteCPPEnumerations(self):
        enumerations = self.GetEnumerationList()
        items = {}
        for enumeration in enumerations:
            values = self.GetEnumerationValues("", enumeration).split(",")
            for value in values:
                tokens = value.split("_")
                if tokens[0] not in items:
                    items[tokens[0]] = []
                items[tokens[0]].append(tokens[1])
        format = """struct {name} {{
    enum Type {{
{values}
    }};
}};
"""
        path = os.path.join(self.outputDirectory, "%s_cpp.h" % (self.subsystem))
        with open(path, "w") as file:
            for item in items:
                name = item
                values = items[item]
                itemFormat = "        {value} = {subsystem}::{subsystem}_shared_{name}_{value}"
                if "Flags" in name or "IndexMap" in name:
                    itemFormat = itemFormat + " - 1"
                itemFormat = itemFormat + ",\n"
                textValues = ""
                for value in values:
                    textValues = textValues + itemFormat.format(value = value, subsystem = self.subsystem, name = name)
            
                file.write(format.format(name = name, values = textValues))

    def GetCommands(self):
        commands = {}
        for item in self.GetCommandList():
            commands[item] = self.CreateSALCommand(item)
            
        result = []
        for command in sorted([x for x in commands]):
            result.append(commands[command])
        return result
        
    def GetEvents(self):
        events = {}
        for item in self.GetEventList():
            events[item] = self.CreateSALEvent(item)

        result = []
        for event in sorted([x for x in events]):
            result.append(events[event])
        return result
        
    def GetTelemetry(self):
        telemetry = {}
        for item in self.GetTelemetryList():
            telemetry[item] = self.CreateSALTelemetry(item)
        result = []
        for telem in sorted([x for x in telemetry]):
            result.append(telemetry[telem])
        return result
        
    def CreateSALCommand(self, command):
        basePath = ".//packagedElement[@name='SAL interface']/packagedElement[@name='Command']/packagedElement[@name='%s']/ownedAttribute" % (command)
        author = ""
        parameters = []
        for parameter in self.GetCommandParameterList(command):
            parameters.append(self.CreateSALParameter("Command", command, parameter))
        return SALCommand(self.subsystem, self.version, author, command, parameters)
        
    def CreateSALEvent(self, event):
        basePath = ".//packagedElement[@name='SAL interface']/packagedElement[@name='Event']/packagedElement[@name='%s']/ownedAttribute" % (event)
        author = ""
        parameters = []
        for parameter in self.GetEventParameterList(event):
            parameters.append(self.CreateSALParameter("Event", event, parameter))
        return SALEvent(self.subsystem, self.version, author, event, parameters)
        
    def CreateSALTelemetry(self, telemetry):
        basePath = ".//packagedElement[@name='SAL interface']/packagedElement[@name='Telemetry']/packagedElement[@name='%s']/ownedAttribute" % (telemetry)
        author = ""
        parameters = []
        for parameter in self.GetTelemetryParameterList(telemetry):
            parameters.append(self.CreateSALParameter("Telemetry", telemetry, parameter))
        return SALTelemetry(self.subsystem, self.version, author, telemetry, parameters)

    def CreateSALParameter(self, type, command, parameter):
        basePath = ".//packagedElement[@name='SAL interface']/packagedElement[@name='%s']/packagedElement[@name='%s']/ownedAttribute[@name='%s']%s" % (type, command, parameter,'%s')
        typePath = basePath % "/type/xmiExtension/referenceExtension"
        description = ""
        type = self.GetValueByName(self.uml.find(typePath), "referentPath", "UNDEFINED")
        
        if type is "UNDEFINED":
            typeID = self.GetValueByName(self.uml.find(basePath % ""), "type", "UNDEFINED")
            type = self.TypeIDtoType(typeID)
        else:
            length = len(type)
            lastIndex = type.rfind(':')
            type = type[-(length-lastIndex-1):] 

        units = self.uml.find(basePath % "/defaultValue/body")
        if units is not None:
            units = units.text
        units = "" if units is None else units
		
        if type == "string":
            count = self.GetValueByName(self.uml.find(basePath % "/upperValue"),"value", "1")
            return SALParameterString(parameter, description, type, units, count)
        elif type in salTypes:
            count = self.GetValueByName(self.uml.find(basePath % "/upperValue"),"value", "1")
            return SALParameter(parameter, description, type, units, count)
        elif self.TypeIsEnumeration(type):
            count = self.GetValueByName(self.uml.find(basePath % "/upperValue"),"value", "1")
            return SALParameterEnumeration(parameter, description, type, units, count, self.GetEnumerationValues(parameter + "_", type))
        else:
            print("BAD TYPE: %s" % type)
            self.error = True
            return 0
                    
    def GetCommandList(self):
        return [command.get("name") for command in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Command']/packagedElement")]
  
    def GetCommandParameterList(self, command):
        return [parameter.get("name") for parameter in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Command']/packagedElement[@name='%s']/ownedAttribute" % command)]

    def GetEventList(self):
        return [event.get("name") for event in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Event']/packagedElement")]
        
    def GetEventParameterList(self, event):
        return [parameter.get("name") for parameter in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Event']/packagedElement[@name='%s']/ownedAttribute" % event)]
                
    def GetTelemetryList(self):
        return [telemetry.get("name") for telemetry in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Telemetry']/packagedElement")]
        
    def GetTelemetryParameterList(self, telemetry):
        return [parameter.get("name") for parameter in self.uml.findall(".//packagedElement[@name='SAL interface']/packagedElement[@name='Telemetry']/packagedElement[@name='%s']/ownedAttribute" % telemetry)]      
        
    def GetEnumerationList(self):
        return [enum.get("name") for enum in self.uml.findall(".//packagedElement[@name='Enumerations']/packagedElement[@xmitype='uml:Enumeration']")]
        
    def GetEnumerationValues(self, field, enumeration):
        names = ["%s%s_%s" % (field, enumeration, value.get("name")) for value in self.uml.findall(".//packagedElement[@name='Enumerations']/packagedElement[@name='%s']/ownedLiteral" % enumeration)]
        return ",".join(names)

    def GetValue(self, node, default):
        return node.get("value") if node is not None else default

    def GetValueByName(self, node, value, default):
        return node.get(value) if node is not None else default

    def TypeIDtoType(self, typeID):
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
        
    def TypeIsEnumeration(self, name):
        path = ".//packagedElement[@name='Enumerations']/packagedElement[@name='%s']" % name
        node = self.uml.find(path)
        return node.get("xmitype") == "uml:Enumeration" if node is not None else False     
        
#if len(sys.argv) != 7:
#    print("""
#Version: 1.2
#    
#usage: *.py <SubSystem> <SALVersion> <UMLFile> <OutputDirectory> <IgnoreGlobals(T/F)> <isForLabVIEW(T/F)>
#example: *.py m2ms 3.5.0 D:\Temp\SALTemp.xml D:\Temp T F
#
#Notes:
#    1. Commands must be a direct child of a package named Command
#    2. Commands must not be named Command, otherwise it will be ignored
#    3. Events must be a direct child of a package named Event
#    4. Events must not be named Event, otherwise it will be ignored
#    5. Telemetry must be a direct child of a package named Telemetry
#    6. Telemetry must not be named Telemetry, otherwise it will be ignored
#    7. If you want parameters to have units defined, create a new tag named 'unit'""")
#else:
#    ignoreGlobals = sys.argv[5] == "T"
#    isForLabVIEW = sys.argv[6] == "T"
#    print("Executing UML XMI 2.5 from MagicDraw to SAL XML")
#    print("UML Parser")
#    uml = UMLParser()
#    print("Opening XML Model")
#    uml.Open(sys.argv[1], sys.argv[2], sys.argv[3])
#    print("Parsing")
#    uml.Parse(sys.argv[4])
