from SALXMLParser import *
from SALPYControllerGenerator import *
from PythonEnumerationGenerator import *
import os
import sys

if len(sys.argv) != 6:
    print("""
Version: 1.0
    
usage: *.py <GenericsPath> <CommandsPath> <EventsPath> <TelemetryPath> <OutputDirectory>
example: *.py /tmp/SALGenerics.xml /tmp/tmp_Commands.xml /tmp/tmp_Events.xml /tmp/tmp_Telemetry.xml /tmp/tmpEUI""")
else:
    parser = SALXMLParser()
    commands, events, telemetry, enumerations = parser.parse(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    generator = PythonEnumerationGenerator()
    generator.generate(commands, events, telemetry, enumerations, sys.argv[5])
    generator = SALPYControllerGenerator(commands, events, telemetry)
    generator.generate(sys.argv[5])

    templateDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Controller-Template")

    files = [
        [os.path.join(templateDir, "Commands.py"), os.path.join(sys.argv[5], "Commands.py")],
        [os.path.join(templateDir, "Context.py"), os.path.join(sys.argv[5], "Context.py")],
        [os.path.join(templateDir, "Controller.py"), os.path.join(sys.argv[5], "Controller.py")],
        [os.path.join(templateDir, "Main.py"), os.path.join(sys.argv[5], "Main.py")],
        [os.path.join(templateDir, "Model.py"), os.path.join(sys.argv[5], "Model.py")],
        [os.path.join(templateDir, "States.py"), os.path.join(sys.argv[5], "States.py")],
        [os.path.join(templateDir, "Threads.py"), os.path.join(sys.argv[5], "Threads.py")]
    ]
    for file in files:
        source = file[0]
        dest = file[1]
        with open(source, "r") as s:
            with open(dest, "w") as d:
                d.write(s.read().replace("{subsystem}", commands[0].subsystem))