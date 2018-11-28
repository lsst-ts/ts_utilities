from SALXMLParser import *
from SALPYRemoteGenerator import *
import os
import sys

if len(sys.argv) != 6:
    print("""
Version: 1.0
    
Note: If the XML doesn't exist specify None for the path

usage: *.py <GenericsPath> <CommandsPath> <EventsPath> <TelemetryPath> <OutputDirectory>
example: *.py /tmp/SALGenerics.xml /tmp/tmp_Commands.xml /tmp/tmp_Events.xml /tmp/tmp_Telemetry.xml /tmp""")
else:
    parser = SALXMLParser()
    commands, events, telemetry, enumerations = parser.parse(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    generator = PythonEnumerationGenerator()
    generator.generate(commands, events, telemetry, enumerations, sys.argv[5])
    generator = SALPYRemoteGenerator(commands, events, telemetry)
    generator.generate(sys.argv[5])