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
        format = """

class {name}:
{values}"""
        path = os.path.join(self.outputDirectory, "%sEnumerations.py" % (self.subsystem))
        with open(path, "w") as file:
            file.write("import SALPY_{subsystem}\n\n\n".format(subsystem=self.subsystem))
            file.write("class SummaryStates:\n")
            file.write("    OfflineState = SALPY_{subsystem}.SAL__STATE_OFFLINE\n".format(subsystem=self.subsystem))
            file.write("    StandbyState = SALPY_{subsystem}.SAL__STATE_STANDBY\n".format(subsystem=self.subsystem))
            file.write("    DisabledState = SALPY_{subsystem}.SAL__STATE_DISABLED\n".format(subsystem=self.subsystem))
            file.write("    EnabledState = SALPY_{subsystem}.SAL__STATE_ENABLED\n".format(subsystem=self.subsystem))
            file.write("    FaultState = SALPY_{subsystem}.SAL__STATE_FAULT\n".format(subsystem=self.subsystem))
            for item in items:
                if item == "SummaryStates":
                    continue
                name = item
                values = items[item]
                itemFormat = "    {value} = SALPY_{subsystem}.{subsystem}_shared_{name}_{value}"
                if "Flags" in name or "IndexMap" in name:
                    itemFormat = itemFormat + " - 1"
                itemFormat = itemFormat + "\n"
                textValues = ""
                for value in values:
                    textValues = textValues + itemFormat.format(value=value, subsystem=self.subsystem, name=name)
                file.write(format.format(name=name, values=textValues))