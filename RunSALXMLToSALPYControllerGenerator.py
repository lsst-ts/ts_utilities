from SALXMLParser import *
from SALPYControllerGenerator import *
import os
import sys

if len(sys.argv) != 6:
    print("""
Version: 1.0
    
usage: *.py <GenericsPath> <CommandsPath> <EventsPath> <TelemetryPath> <OutputDirectory>
example: *.py /tmp/SALGenerics.xml /tmp/tmp_Commands.xml /tmp/tmp_Events.xml /tmp/tmp_Telemetry.xml /tmp""")
else:
    parser = SALXMLParser()
    commands, events, telemetry, enumerations = parser.parse(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    generator = SALPYControllerGenerator(commands, events, telemetry)
    generator.generate(sys.argv[5])