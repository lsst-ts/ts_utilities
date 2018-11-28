from SALXMLParser import *
from SALPYRemoteGenerator import *
from PythonEnumerationGenerator import *
import os
import sys

if len(sys.argv) != 6:
    print("""
Version: 1.0

Note: If the XML doesn't exist specify None for the path
    
usage: *.py <GenericsPath> <CommandsPath> <EventsPath> <TelemetryPath> <OutputDirectory>
example: *.py /tmp/SALGenerics.xml /tmp/tmp_Commands.xml /tmp/tmp_Events.xml /tmp/tmp_Telemetry.xml /tmp/tmpEUI""")
else:
    parser = SALXMLParser()
    commands, events, telemetry, enumerations = parser.parse(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    generator = PythonEnumerationGenerator()
    generator.generate(commands, events, telemetry, enumerations, sys.argv[5])
    generator = SALPYRemoteGenerator(commands, events, telemetry)
    generator.generate(sys.argv[5])

    templateDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EUI-Template")

    files = [
        [os.path.join(templateDir, "ApplicationControlWidget.py"), os.path.join(sys.argv[5], "ApplicationControlWidget.py")],
        [os.path.join(templateDir, "ApplicationPaginationWidget.py"), os.path.join(sys.argv[5], "ApplicationPaginationWidget.py")],
        [os.path.join(templateDir, "ApplicationStatusWidget.py"), os.path.join(sys.argv[5], "ApplicationStatusWidget.py")],
        [os.path.join(templateDir, "DataCache.py"), os.path.join(sys.argv[5], "DataCache.py")],
        [os.path.join(templateDir, "EUI.py"), os.path.join(sys.argv[5], "EUI.py")],
        [os.path.join(templateDir, "OverviewPageWidget.py"), os.path.join(sys.argv[5], "OverviewPageWidget.py")],
        [os.path.join(templateDir, "QTHelpers.py"), os.path.join(sys.argv[5], "QTHelpers.py")]
    ]
    for file in files:
        source = file[0]
        dest = file[1]
        with open(source, "r") as s:
            with open(dest, "w") as d:
                d.write(s.read().replace("{name}", commands[0].subsystem))