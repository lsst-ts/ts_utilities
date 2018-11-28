import os

class CppEnumerationGenerator:
    def generate(self, commands, events, telemetry, enumerations, outputDirectory, ignoreGlobals = True):
        self.ignoreGlobals = ignoreGlobals
        self.outputDirectory = outputDirectory
        self.subsystem = commands[0].subsystem
        self.writeCPPEnumerations(enumerations)

    def writeCPPEnumerations(self, enumerations):
        items = {}
        for enumeration in enumerations:
            name = enumeration.name
            values = enumeration.values
            items[name] = []
            for value in values:
                items[name].append(value)
        format = """struct {name} {{
    enum Type {{
{values}
    }};
}};
"""
        path = os.path.join(self.outputDirectory, "%s_cppEnumerations.h" % (self.subsystem))
        with open(path, "w") as file:
            for item in items:
                name = item
                values = items[item]
                itemFormat = "        {value} = {subsystem}::{subsystem}_shared_{name}_{value}"
                if "Flags" in name or "IndexMap" in name:
                    itemFormat = itemFormat + " - 1"
                itemFormat = itemFormat + ",\n"
                textValues = ""
                for value in values:
                    textValues = textValues + itemFormat.format(value = value, subsystem = self.subsystem, name = name)
            
                file.write(format.format(name = name, values = textValues))