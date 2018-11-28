import os

globalCommands = ["abort", "enable", "disable", "standby", "exitControl", "start", "enterControl", "setValue"]
globalEvents = ["settingVersions", "errorCode", "summaryState", "appliedSettingsMatchStart"]

class SALXMLGenerator:
    def generate(self, commands, events, telemetry, enumerations, outputDirectory, ignoreGlobals = True):
        self.ignoreGlobals = ignoreGlobals
        self.outputDirectory = outputDirectory
        self.subsystem = commands[0].subsystem
        self.writeCommands(commands)
        self.writeEvents(enumerations, events)
        self.writeTelemetry(telemetry)
        
    def writeCommands(self, commands):
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
                    if not (self.ignoreGlobals and item.name in globalCommands):
                        commandFile.write(item.createSALXML())
            commandFile.write(footer)          
            
    def writeEvents(self, enumerations, events):
        header = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="http://lsst-sal.tuc.noao.edu/schema/SALEventSet.xsl"?>
<SALEventSet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://lsst-sal.tuc.noao.edu/schema/SALEventSet.xsd">"""
        footer = "\n</SALEventSet>"
        path = os.path.join(self.outputDirectory, "%s_Events.xml" % (self.subsystem))
        with open(path, "w") as eventFile:  
            eventFile.write(header)
            eventFile.write("\n")
            for item in enumerations:
                if len(item.values) > 0:
                    print("Writing enumeration %s" % item.name)
                    eventFile.write("    <Enumeration>%s</Enumeration>\n" % (item.createSALXML()))
            for item in events:
                if item.name != "Event":
                    print("Writing event %s" % item.name)
                    if not (self.ignoreGlobals and item.name in globalEvents):
                        eventFile.write(item.createSALXML())
            eventFile.write(footer)     

    def writeTelemetry(self, telemetry):
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
                    telemetryFile.write(item.createSALXML())
            telemetryFile.write(footer)   
