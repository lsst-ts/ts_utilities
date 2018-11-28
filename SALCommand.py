class SALCommand:
    template = """
    <SALCommand>
        <Subsystem>%s</Subsystem>
        <Version>%s</Version>
        <Author>%s</Author>
        <EFDB_Topic>%s</EFDB_Topic>
        <Alias>%s</Alias>
        <Device></Device>
        <Property></Property>
        <Action></Action>
        <Value></Value>
        <Explanation>http://sal.lsst.org</Explanation>%s
    </SALCommand>"""
    
    def __init__(self, subsystem, version, author, name, parameters):
        self.subsystem = subsystem
        self.version = version
        self.author = author
        self.name = name
        self.parameters = parameters
        
    def createSALXML(self):
        topic = "%s_command_%s" % (self.subsystem, self.name)
        alias = self.name
        items = ""
        for parameter in self.parameters:
            items = items + parameter.createSALXML()
        return self.template % (self.subsystem, self.version, self.author, topic, alias, items)