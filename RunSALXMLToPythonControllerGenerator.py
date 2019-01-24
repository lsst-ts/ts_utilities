from SALXMLParser import *
from SALPYGenerator import *
import os
import sys

def processCommands(namespace, commands, sourceTemplateFile, commandTemplateFile, destinationFile):
    commandTemplate = ""
    with open(commandTemplateFile, "r") as f:
        commandTemplate = f.read()
    subsystem = commands[0].subsystem
    commandDefinitions = ""
    for command in commands:
        name = command.name
        upperName = name[0].upper() + name[1:]
        commandDefinitions = commandDefinitions + "\n" + commandTemplate.replace(">SUBSYSTEM<", subsystem).replace(">NAME<", name).replace(">UPPER_NAME<", upperName)
    with open(sourceTemplateFile, "r") as s:
        with open(destinationFile, "w") as d:
            d.write(s.read().replace(">SUBSYSTEM<", subsystem).replace(">COMMAND_DEFINITIONS<", commandDefinitions).replace(">NAMESPACE<", namespace))

def processContext(namespace, commands, sourceTemplateFile, commandTemplateFile, destinationFile):
    commandTemplate = ""
    with open(commandTemplateFile, "r") as f:
        commandTemplate = f.read()
    subsystem = commands[0].subsystem
    commandDefinitions = ""
    for command in commands:
        name = command.name
        upperName = name[0].upper() + name[1:]
        commandDefinitions = commandDefinitions + "\n" + commandTemplate.replace(">SUBSYSTEM<", subsystem).replace(">NAME<", name).replace(">UPPER_NAME<", upperName)
    with open(sourceTemplateFile, "r") as s:
        with open(destinationFile, "w") as d:
            d.write(s.read().replace(">SUBSYSTEM<", subsystem).replace(">COMMAND_DEFINITIONS<", commandDefinitions).replace(">NAMESPACE<", namespace))

def processController(namespace, commands, sourceTemplateFile, commandTemplateFile, destinationFile):
    commandTemplate = ""
    with open(commandTemplateFile, "r") as f:
        commandTemplate = f.read()
    subsystem = commands[0].subsystem
    commandDefinitions = ""
    for command in commands:
        name = command.name
        upperName = name[0].upper() + name[1:]
        commandDefinitions = commandDefinitions + commandTemplate.replace(">SUBSYSTEM<", subsystem).replace(">NAME<", name).replace(">UPPER_NAME<", upperName)
    commandDefinitions = commandDefinitions[:-1]
    with open(sourceTemplateFile, "r") as s:
        with open(destinationFile, "w") as d:
            d.write(s.read().replace(">SUBSYSTEM<", subsystem).replace(">COMMAND_DEFINITIONS<", commandDefinitions).replace(">NAMESPACE<", namespace))

def processStates(namespace, commands, sourceTemplateFile, commandTemplateFile, destinationFile):
    commandTemplate = ""
    with open(commandTemplateFile, "r") as f:
        commandTemplate = f.read()
    subsystem = commands[0].subsystem
    commandDefinitions = ""
    for command in commands:
        name = command.name
        upperName = name[0].upper() + name[1:]
        commandDefinitions = commandDefinitions + "\n" + commandTemplate.replace(">SUBSYSTEM<", subsystem).replace(">NAME<", name).replace(">UPPER_NAME<", upperName)
    with open(sourceTemplateFile, "r") as s:
        with open(destinationFile, "w") as d:
            d.write(s.read().replace(">SUBSYSTEM<", subsystem).replace(">COMMAND_DEFINITIONS<", commandDefinitions).replace(">NAMESPACE<", namespace))

def processThreads(namespace, commands, sourceTemplateFile, commandTemplateFile, destinationFile):
    commandTemplate = ""
    with open(commandTemplateFile, "r") as f:
        commandTemplate = f.read()
    subsystem = commands[0].subsystem
    commandDefinitions = ""
    for command in commands:
        name = command.name
        upperName = name[0].upper() + name[1:]
        commandDefinitions = commandDefinitions + "\n" + commandTemplate.replace(">SUBSYSTEM<", subsystem).replace(">NAME<", name).replace(">UPPER_NAME<", upperName)
    with open(sourceTemplateFile, "r") as s:
        with open(destinationFile, "w") as d:
            d.write(s.read().replace(">SUBSYSTEM<", subsystem).replace(">COMMAND_DEFINITIONS<", commandDefinitions).replace(">NAMESPACE<", namespace))

if len(sys.argv) != 7:
    print("""
Version: 1.0

Note: If the XML doesn't exist specify None for the path
    
usage: *.py <GenericsPath> <CommandsPath> <EventsPath> <TelemetryPath> <OutputDirectory> <namespace>
example: *.py /tmp/SALGenerics.xml /tmp/tmp_Commands.xml /tmp/tmp_Events.xml /tmp/tmp_Telemetry.xml /tmp/tmpEUI lsst.ts.mt.m1m3.ss""")
else:
    outputDir = sys.argv[5]
    namespace = sys.argv[6]
    tokens = namespace.split(".")
    print(tokens)
    path = os.path.join(outputDir, "python")
    if not os.path.exists(path):
        os.makedirs(path)
    for token in tokens:
        path = os.path.join(path, token)
        if not os.path.exists(path):
            os.makedirs(path)
    if not os.path.exists(os.path.join(outputDir, "tests")):
        os.makedirs(os.path.join(outputDir, "tests"))
    
    parser = SALXMLParser()
    commands, events, telemetry, enumerations = parser.parse(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    generator = SALPYGenerator(commands, events, telemetry, enumerations)
    generator.generate(path)

    templateDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Controller-Template")

    processCommands(namespace, commands, os.path.join(templateDir, "src", "commands.py"), os.path.join(templateDir, "src", "commandTemplate.py"), os.path.join(path, "commands.py"))
    processContext(namespace, commands, os.path.join(templateDir, "src", "context.py"), os.path.join(templateDir, "src", "contextCommandTemplate.py"), os.path.join(path, "context.py"))
    processController(namespace, commands, os.path.join(templateDir, "src", "controller.py"), os.path.join(templateDir, "src", "controllerCommandTemplate.py"), os.path.join(path, "controller.py"))
    processStates(namespace, commands, os.path.join(templateDir, "src", "states.py"), os.path.join(templateDir, "src", "statesCommandTemplate.py"), os.path.join(path, "states.py"))
    processThreads(namespace, commands, os.path.join(templateDir, "src", "threads.py"), os.path.join(templateDir, "src", "threadsCommandTemplate.py"), os.path.join(path, "threads.py"))
    files = [
        [os.path.join(templateDir, "src", "main.py"), os.path.join(path, "main.py")],
        [os.path.join(templateDir, "src", "model.py"), os.path.join(path, "model.py")],
        [os.path.join(templateDir, "src", "run.py"), os.path.join(path, "run.py")],
        [os.path.join(templateDir, "src", "setup.py"), os.path.join(path, "setup.py")],
        [os.path.join(templateDir, "tests", "tests.py"), os.path.join(outputDir, "tests", "tests.py")],
        [os.path.join(templateDir, "src", "limits.py"), os.path.join(path, "limits.py")],
        [os.path.join(templateDir, "src", "functions.py"), os.path.join(path, "functions.py")],
        [os.path.join(templateDir, "src", "domain.py"), os.path.join(path, "domain.py")],
        [os.path.join(templateDir, "src", "utilities.py"), os.path.join(path, "utilities.py")],
        [os.path.join(templateDir, "src", "settings.py"), os.path.join(path, "settings.py")],
    ]
    for file in files:
        source = file[0]
        dest = file[1]
        with open(source, "r") as s:
            with open(dest, "w") as d:
                d.write(s.read().replace(">SUBSYSTEM<", commands[0].subsystem).replace(">NAMESPACE<", namespace))

    