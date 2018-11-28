class SALEnumeration:
    def __init__(self, name, values):
        self.name = name
        self.values = values

    def createSALXML(self):
        return ",".join([("%s_%s" % (self.name, x)) for x in self.values])