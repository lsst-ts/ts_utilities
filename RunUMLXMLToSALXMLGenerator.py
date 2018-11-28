from UMLXMLParser import *
from SALXMLGenerator import *
import os
import sys

if len(sys.argv) != 6:
    print("""
Version: 1.0
    
usage: *.py <SubSystem> <SALVersion> <UMLFile> <OutputDirectory> <IgnoreGlobals(T/F)>
example: *.py m2ms 3.5.0 D:\Temp\SALTemp.xml D:\Temp T

Notes:
    1. Commands must be a direct child of a package named Command
    2. Commands must not be named Command, otherwise it will be ignored
    3. Events must be a direct child of a package named Event
    4. Events must not be named Event, otherwise it will be ignored
    5. Telemetry must be a direct child of a package named Telemetry
    6. Telemetry must not be named Telemetry, otherwise it will be ignored
    7. If you want parameters to have units defined, create a new tag named 'unit'""")
else:
    ignoreGlobals = sys.argv[5] == "T"
    parser = UMLXMLParser()
    commands, events, telemetry, enumerations = parser.parse(sys.argv[1], sys.argv[2], sys.argv[3])
    generator = SALXMLGenerator()
    generator.generate(commands, events, telemetry, enumerations, sys.argv[4], sys.argv[5] == "T")