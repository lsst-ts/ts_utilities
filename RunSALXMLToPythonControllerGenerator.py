from SALXMLParser import *
from SALPYControllerGenerator import *
from SALPYRemoteGenerator import *
from PythonEnumerationGenerator import *
import os
import sys

def processCommands(commands, sourceTemplateFile, commandTemplateFile, destinationFile):
    commandTemplate = ""
    with open(commandTemplateFile, "r") as f:
        commandTemplate = f.read()
    subsystem = commands[0].subsystem
    commandDefinitions = ""
    for command in commands:
        name = command.name
        upperName = name[0].upper() + name[1:]
        commandDefinitions = commandDefinitions + "\n" + commandTemplate.format(subsystem = subsystem, name = name, upperName = upperName)
    with open(sourceTemplateFile, "r") as s:
        with open(destinationFile, "w") as d:
            d.write(s.read().replace("{subsystem}", subsystem).replace("{commandDefinitions}", commandDefinitions))

def processContext(commands, sourceTemplateFile, commandTemplateFile, destinationFile):
    commandTemplate = ""
    with open(commandTemplateFile, "r") as f:
        commandTemplate = f.read()
    subsystem = commands[0].subsystem
    commandDefinitions = ""
    for command in commands:
        name = command.name
        upperName = name[0].upper() + name[1:]
        commandDefinitions = commandDefinitions + "\n" + commandTemplate.format(subsystem = subsystem, name = name, upperName = upperName)
    with open(sourceTemplateFile, "r") as s:
        with open(destinationFile, "w") as d:
            d.write(s.read().replace("{subsystem}", subsystem).replace("{commandDefinitions}", commandDefinitions))

def processController(commands, sourceTemplateFile, commandTemplateFile, destinationFile):
    commandTemplate = ""
    with open(commandTemplateFile, "r") as f:
        commandTemplate = f.read()
    subsystem = commands[0].subsystem
    commandDefinitions = ""
    for command in commands:
        name = command.name
        upperName = name[0].upper() + name[1:]
        commandDefinitions = commandDefinitions + commandTemplate.format(subsystem = subsystem, name = name, upperName = upperName)
    commandDefinitions = commandDefinitions[:-1]
    with open(sourceTemplateFile, "r") as s:
        with open(destinationFile, "w") as d:
            d.write(s.read().replace("{subsystem}", subsystem).replace("{commandDefinitions}", commandDefinitions))

def processStates(commands, sourceTemplateFile, commandTemplateFile, destinationFile):
    commandTemplate = ""
    with open(commandTemplateFile, "r") as f:
        commandTemplate = f.read()
    subsystem = commands[0].subsystem
    commandDefinitions = ""
    for command in commands:
        name = command.name
        upperName = name[0].upper() + name[1:]
        commandDefinitions = commandDefinitions + "\n" + commandTemplate.format(subsystem = subsystem, name = name, upperName = upperName)
    with open(sourceTemplateFile, "r") as s:
        with open(destinationFile, "w") as d:
            d.write(s.read().replace("{subsystem}", subsystem).replace("{commandDefinitions}", commandDefinitions))

def processThreads(commands, sourceTemplateFile, commandTemplateFile, destinationFile):
    commandTemplate = ""
    with open(commandTemplateFile, "r") as f:
        commandTemplate = f.read()
    subsystem = commands[0].subsystem
    commandDefinitions = ""
    for command in commands:
        name = command.name
        upperName = name[0].upper() + name[1:]
        commandDefinitions = commandDefinitions + "\n" + commandTemplate.format(subsystem = subsystem, name = name, upperName = upperName)
    with open(sourceTemplateFile, "r") as s:
        with open(destinationFile, "w") as d:
            d.write(s.read().replace("{subsystem}", subsystem).replace("{commandDefinitions}", commandDefinitions))

if len(sys.argv) != 6:
    print("""
Version: 1.0

Note: If the XML doesn't exist specify None for the path
    
usage: *.py <GenericsPath> <CommandsPath> <EventsPath> <TelemetryPath> <OutputDirectory>
example: *.py /tmp/SALGenerics.xml /tmp/tmp_Commands.xml /tmp/tmp_Events.xml /tmp/tmp_Telemetry.xml /tmp/tmpEUI""")
else:
    outputDir = sys.argv[5]
    if not os.path.exists(os.path.join(outputDir, "src")):
        os.makedirs(os.path.join(outputDir, "src"))
    if not os.path.exists(os.path.join(outputDir, "tests")):
        os.makedirs(os.path.join(outputDir, "tests"))
    
    parser = SALXMLParser()
    commands, events, telemetry, enumerations = parser.parse(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    generator = PythonEnumerationGenerator()
    generator.generate(commands, events, telemetry, enumerations, os.path.join(outputDir, "src"))
    generator = SALPYControllerGenerator(commands, events, telemetry)
    generator.generate(os.path.join(outputDir, "src"))
    generator.generate(os.path.join(outputDir, "tests"))
    generator = SALPYRemoteGenerator(commands, events, telemetry)
    generator.generate(os.path.join(outputDir, "tests"))

    templateDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Controller-Template")

    processCommands(commands, os.path.join(templateDir, "src", "Commands.py"), os.path.join(templateDir, "src", "CommandTemplate.py"), os.path.join(outputDir, "src", "Commands.py"))
    processContext(commands, os.path.join(templateDir, "src", "Context.py"), os.path.join(templateDir, "src", "ContextCommandTemplate.py"), os.path.join(outputDir, "src", "Context.py"))
    processController(commands, os.path.join(templateDir, "src", "Controller.py"), os.path.join(templateDir, "src", "ControllerCommandTemplate.py"), os.path.join(outputDir, "src", "Controller.py"))
    processStates(commands, os.path.join(templateDir, "src", "States.py"), os.path.join(templateDir, "src", "StatesCommandTemplate.py"), os.path.join(outputDir, "src", "States.py"))
    processThreads(commands, os.path.join(templateDir, "src", "Threads.py"), os.path.join(templateDir, "src", "ThreadsCommandTemplate.py"), os.path.join(outputDir, "src", "Threads.py"))
    files = [
        [os.path.join(templateDir, "src", "Main.py"), os.path.join(outputDir, "src", "Main.py")],
        [os.path.join(templateDir, "src", "Model.py"), os.path.join(outputDir, "src", "Model.py")],
        [os.path.join(templateDir, "src", "Run.py"), os.path.join(outputDir, "src", "Run.py")],
        [os.path.join(templateDir, "src", "Setup.py"), os.path.join(outputDir, "src", "Setup.py")],
        [os.path.join(templateDir, "tests", "Tests.py"), os.path.join(outputDir, "tests", "Tests.py")],
    ]
    for file in files:
        source = file[0]
        dest = file[1]
        with open(source, "r") as s:
            with open(dest, "w") as d:
                d.write(s.read().replace("{subsystem}", commands[0].subsystem))

    