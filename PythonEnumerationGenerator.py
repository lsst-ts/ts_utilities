import os

class PythonEnumerationGenerator:
    def generate(self, commands, events, telemetry, enumerations, outputDirectory):
        self.outputDirectory = outputDirectory
        self.subsystem = commands[0].subsystem
        self.writePythonEnumerations(enumerations)

    def writePythonEnumerations(self, enumerations):
        items = {}
        for enumeration in enumerations:
            name = enumeration.name
            values = enumeration.values
            items[name] = []
            for value in values:
                items[name].append(value)
        format = """class {name}:
{values}
"""
        path = os.path.join(self.outputDirectory, "%sEnumerations.py" % (self.subsystem))
        with open(path, "w") as file:
            file.write("from SALPY_{subsystem} import *\n\n".format(subsystem = self.subsystem))
            file.write("class SummaryStates:\n")
            file.write("    OfflineState = SAL__STATE_OFFLINE\n")
            file.write("    StandbyState = SAL__STATE_STANDBY\n")
            file.write("    DisabledState = SAL__STATE_DISABLED\n")
            file.write("    EnabledState = SAL__STATE_ENABLED\n")
            file.write("    FaultState = SAL__STATE_FAULT\n\n")
            for item in items:
                if item == "SummaryStates":
                    continue
                name = item
                values = items[item]
                itemFormat = "    {value} = {subsystem}_shared_{name}_{value}"
                if "Flags" in name or "IndexMap" in name:
                    itemFormat = itemFormat + " - 1"
                itemFormat = itemFormat + "\n"
                textValues = ""
                for value in values:
                    textValues = textValues + itemFormat.format(value = value, subsystem = self.subsystem, name = name)
                file.write(format.format(name = name, values = textValues))