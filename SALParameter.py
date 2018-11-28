class SALParameter:
    template = """
        <item>
            <EFDB_Name>%s</EFDB_Name>
            <Description>%s</Description>
            <IDL_Type>%s</IDL_Type>
            <Units>%s</Units>
            <Count>%s</Count>
        </item>"""
    
    def __init__(self, name, description, type, units, count):
        self.name = name
        self.description = description
        self.type = type
        self.units = units
        self.count = count
        
    def createSALXML(self):
        return self.template % (self.name, self.description, self.type, self.units, self.count)

class SALParameterString:
    template = """
        <item>
            <EFDB_Name>%s</EFDB_Name>
            <Description>%s</Description>
            <IDL_Type>%s</IDL_Type>
            <IDL_Size>%s</IDL_Size>
            <Units>%s</Units>
            <Count>%s</Count>
        </item>"""
    
    def __init__(self, name, description, type, units, count):
        self.name = name
        self.description = description
        self.type = type
        self.units = units
        self.count = count
        
    def createSALXML(self):
        return self.template % (self.name, self.description, self.type, self.count, self.units, '1')

class SALParameterEnumeration:
    template = """
        <item>
            <EFDB_Name>%s</EFDB_Name>
            <Description>%s</Description>
            <IDL_Type>long</IDL_Type>
            <Units>%s</Units>
            <Count>%s</Count>
        </item>"""

    def __init__(self, name, description, enumeration, units, count):
        self.name = name
        self.description = description
        self.enumeration = enumeration
        self.units = units
        self.count = count
        
    def createSALXML(self):
        return self.template % (self.name, self.description, self.units, self.count)