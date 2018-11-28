from SALXMLParser import *
from PythonEnumerationGenerator import *
import os
import sys

if len(sys.argv) != 6:
    print("""
Version: 1.0
    
usage: *.py <GenericsPath> <CommandsPath> <EventsPath> <TelemetryPath> <OutputDirectory>
example: *.py /tmp/SALGenerics.xml /tmp/Commands.xml /tmp/Events.xml /tmp/Telemetry.xml /tmp""")
else:
    ignoreGlobals = sys.argv[5] == "T"
    parser = SALXMLParser()
    commands, events, telemetry, enumerations = parser.parse(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    generator = PythonEnumerationGenerator()
    generator.generate(commands, events, telemetry, enumerations, sys.argv[5])