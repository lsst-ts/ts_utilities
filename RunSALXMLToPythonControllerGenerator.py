from SALXMLParser import *
from SALPYControllerGenerator import *
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
    parser = SALXMLParser()
    commands, events, telemetry, enumerations = parser.parse(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    generator = PythonEnumerationGenerator()
    generator.generate(commands, events, telemetry, enumerations, outputDir)
    generator = SALPYControllerGenerator(commands, events, telemetry)
    generator.generate(outputDir)

    templateDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Controller-Template")
    

    processCommands(commands, os.path.join(templateDir, "Commands.py"), os.path.join(templateDir, "CommandTemplate.py"), os.path.join(outputDir, "Commands.py"))
    processContext(commands, os.path.join(templateDir, "Context.py"), os.path.join(templateDir, "ContextCommandTemplate.py"), os.path.join(outputDir, "Context.py"))
    processController(commands, os.path.join(templateDir, "Controller.py"), os.path.join(templateDir, "ControllerCommandTemplate.py"), os.path.join(outputDir, "Controller.py"))
    processStates(commands, os.path.join(templateDir, "States.py"), os.path.join(templateDir, "StatesCommandTemplate.py"), os.path.join(outputDir, "States.py"))
    processThreads(commands, os.path.join(templateDir, "Threads.py"), os.path.join(templateDir, "ThreadsCommandTemplate.py"), os.path.join(outputDir, "Threads.py"))
    files = [
        [os.path.join(templateDir, "Main.pyx"), os.path.join(outputDir, "Main.pyx")],
        [os.path.join(templateDir, "Model.py"), os.path.join(outputDir, "Model.py")],
        [os.path.join(templateDir, "Run.py"), os.path.join(outputDir, "Run.py")],
        [os.path.join(templateDir, "Setup.py"), os.path.join(outputDir, "Setup.py")],
    ]
    for file in files:
        source = file[0]
        dest = file[1]
        with open(source, "r") as s:
            with open(dest, "w") as d:
                d.write(s.read().replace("{subsystem}", commands[0].subsystem))

    