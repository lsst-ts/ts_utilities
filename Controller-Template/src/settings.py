# This file is part of >SUBSYSTEM<.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import os
import xml.etree.ElementTree

from . import domain
from . import functions
from . import limits

class Settings(object):
    def __init__(self, indexMap, settingContainer, settingDirectory: str):
        self.settingDirectory = settingDirectory
        self.settingSet = None
        self.settingVersion = None
        self.log = logging.getLogger("Settings")
        self.indexMap = indexMap
        self.settingContainer = settingContainer

    def setSettingSet(self, set, version):
        previousSettingSet = self.settingSet
        previousSettingVersion = self.settingVersion
        self.settingSet = set
        self.settingVersion = version
        if not os.path.isfile(self.getSettingSetPath()):
            self.log.error(f"Setting Set {set} Version {version} does not exist.")
            self.settingSet = previousSettingSet
            self.settingVersion = previousSettingVersion
            return False
        return True

    def settingSetApplied(self):
        return self.settingSet is not None and self.settingVersion is not None

    def getDefaultSettingPath(self):
        return os.path.join(self.settingDirectory, "defaultSettings.xml")

    def getSettingSetPath(self):
        return os.path.join(self.settingDirectory, f"{self.settingSet}-{self.settingVersion:06d}.xml")

    def loadTempSettings(self, simulate, text):
        tree = xml.etree.ElementTree.fromstring(f"<Settings>{text}</Settings>")
        return self.loadAllSettingsFromTree(simulate, tree)

    def loadAllSettings(self, simulate, filePath):
        tree = xml.etree.ElementTree.parse(filePath)
        return self.loadAllSettingsFromTree(simulate, tree)

    def loadAllSettingsFromTree(self, simulate, tree):
        valid = True
        for item in tree.findall("./Setting"):
            objValid, obj = self.getAttribute(item, "object", True)
            if not objValid or not hasattr(self.settingContainer, obj):
                self.log.error(f"Unknown setting object {obj}.")
                valid = False
                continue
            theObj = getattr(self.settingContainer, obj)
            
            fieldValid, field = self.getAttribute(item, "field", True)
            if not fieldValid or not hasattr(theObj, field):
                self.log.error(f"Unknown field {field} in object {obj}.")
                valid = False
                continue
            theField = getattr(theObj, field)

            if type(theField) is not str and hasattr(theField, "__len__"):
                indexValid, index = self.getAttribute(item, "index", True)
                if indexValid and hasattr(self.indexMap, index):
                    index = getattr(self.indexMap, index)
                elif indexValid:
                    indexValid, index = self.getIntAttribute(item, "index", True)

                if not indexValid:
                    self.log.error(f"Unknown index {index} for field {field} in object {obj}.")
                    valid = False
                    continue

                settingValid, setting = self.getSetting(item, True)
                if settingValid:
                    fieldType = type(theField[index])
                    settingType = type(setting)
                    if fieldType == settingType:
                        if not simulate:
                            theField[index] = setting
                    else:
                        self.log.error(f"Setting type {settingType.__name__} does not match the expected {fieldType.__name__} type for {field} in {obj} at index {index}.")
                        valid = False
                        continue
                else:
                    valid = False
                    continue
            else:
                settingValid, setting = self.getSetting(item, True)
                if settingValid:
                    fieldType = type(theField)
                    settingType = type(setting)
                    if fieldType == settingType:
                        if not simulate:
                            setattr(theObj, field, setting)
                    else:
                        self.log.error(f"Setting type {settingType.__name__} does not match the expected {fieldType.__name__} type for {field} in {obj}.")
                        valid = False
                        continue
                else:
                    valid = False
                    continue
        return valid

    def loadDefaultSettings(self, simulate):
        filePath = self.getDefaultSettingPath()
        if os.path.isfile(filePath):
            return self.loadAllSettings(simulate, filePath)
        self.log.error(f"Could not load default settings from {filePath}.")
        return False

    def loadSetSettings(self, simulate):
        valid = self.loadDefaultSettings(simulate)
        filePath = self.getSettingSetPath()
        if os.path.isfile(filePath):
            return valid and self.loadAllSettings(simulate, filePath)
        self.log.error(f"Could not load setting set from {filePath}.")
        return False

    def loadStateSettings(self, simulate, state):
        valid = self.loadSetSettings(simulate)
        filePath = self.getSettingSetStatePath(state)
        if os.path.isfile(filePath):
            return valid and self.loadAllSettings(simulate, filePath)
        return valid

    def getSetting(self, item, valid):
        valid, type = self.getAttribute(item, "type", valid)
        type = type.lower()
        if type == "str":
            valid, x = self.getAttribute(item, "x", valid)
            return valid, x
        elif type == "int":
            valid, x = self.getIntAttribute(item, "x", valid)
            return valid, x
        elif type == "float":
            valid, x = self.getFloatAttribute(item, "x", valid)
            return valid, x
        elif type == "bool":
            valid, x = self.getBoolAttribute(item, "x", valid)
            return valid, x
        elif type == "linearfunction":
            valid, m = self.getFloatAttribute(item, "m", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            return valid, functions.LinearFunction(m, b)
        elif type == "poly2function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            valid, c = self.getFloatAttribute(item, "c", valid)
            return valid, functions.Poly2Function(a, b, c)
        elif type == "poly3function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            valid, c = self.getFloatAttribute(item, "c", valid)
            valid, d = self.getFloatAttribute(item, "d", valid)
            return valid, functions.Poly3Function(a, b, c, d)
        elif type == "poly4function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            valid, c = self.getFloatAttribute(item, "c", valid)
            valid, d = self.getFloatAttribute(item, "d", valid)
            valid, e = self.getFloatAttribute(item, "e", valid)
            return valid, functions.Poly4Function(a, b, c, d, e)
        elif type == "poly5function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            valid, c = self.getFloatAttribute(item, "c", valid)
            valid, d = self.getFloatAttribute(item, "d", valid)
            valid, e = self.getFloatAttribute(item, "e", valid)
            valid, f = self.getFloatAttribute(item, "f", valid)
            return valid, functions.Poly5Function(a, b, c, d, e, f)
        elif type == "matrix1x2function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            return valid, functions.Matrix1x2Function(a, b)
        elif type == "matrix1x3function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            valid, c = self.getFloatAttribute(item, "c", valid)
            return valid, functions.Matrix1x3Function(a, b, c)
        elif type == "matrix1x4function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            valid, c = self.getFloatAttribute(item, "c", valid)
            valid, d = self.getFloatAttribute(item, "d", valid)
            return valid, functions.Matrix1x4Function(a, b, c, d)
        elif type == "matrix1x5function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            valid, c = self.getFloatAttribute(item, "c", valid)
            valid, d = self.getFloatAttribute(item, "d", valid)
            valid, e = self.getFloatAttribute(item, "e", valid)
            return valid, functions.Matrix1x5Function(a, b, c, d, e)
        elif type == "matrix1x6function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            valid, c = self.getFloatAttribute(item, "c", valid)
            valid, d = self.getFloatAttribute(item, "d", valid)
            valid, e = self.getFloatAttribute(item, "e", valid)
            valid, f = self.getFloatAttribute(item, "f", valid)
            return valid, functions.Matrix1x6Function(a, b, c, d, e, f)
        elif type == "matrix1x7function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            valid, c = self.getFloatAttribute(item, "c", valid)
            valid, d = self.getFloatAttribute(item, "d", valid)
            valid, e = self.getFloatAttribute(item, "e", valid)
            valid, f = self.getFloatAttribute(item, "f", valid)
            valid, g = self.getFloatAttribute(item, "g", valid)
            return valid, functions.Matrix1x7Function(a, b, c, d, e, f, g)
        elif type == "matrix1x8function":
            valid, a = self.getFloatAttribute(item, "a", valid)
            valid, b = self.getFloatAttribute(item, "b", valid)
            valid, c = self.getFloatAttribute(item, "c", valid)
            valid, d = self.getFloatAttribute(item, "d", valid)
            valid, e = self.getFloatAttribute(item, "e", valid)
            valid, f = self.getFloatAttribute(item, "f", valid)
            valid, g = self.getFloatAttribute(item, "g", valid)
            valid, h = self.getFloatAttribute(item, "h", valid)
            return valid, functions.Matrix1x8Function(a, b, c, d, e, f, g, h)
        elif type == "anybitsetfunction":
            valid, bitMask = self.getIntAttribute(item, "bitMask", valid)
            return valid, functions.AnyBitSetFunction(bitMask)
        elif type == "allbitsetfunction":
            valid, bitMask = self.getIntAttribute(item, "bitMask", valid)
            return valid, functions.AllBitSetFunction(bitMask)
        elif type == "anybitnotsetfunction":
            valid, bitMask = self.getIntAttribute(item, "bitMask", valid)
            return valid, functions.AnyBitNotSetFunction(bitMask)
        elif type == "allbitnotsetfunction":
            valid, bitMask = self.getIntAttribute(item, "bitMask", valid)
            return valid, functions.AllBitNotSetFunction(bitMask)
        elif type == "minimumfunction":
            valid, sampleCount = self.getIntAttribute(item, "sampleCount", valid)
            return valid, functions.MinimumFunction(0.0, sampleCount)
        elif type == "maximumfunction":
            valid, sampleCount = self.getIntAttribute(item, "sampleCount", valid)
            return valid, functions.MaximumFunction(0.0, sampleCount)
        elif type == "averagefunction":
            valid, sampleCount = self.getIntAttribute(item, "sampleCount", valid)
            return valid, functions.AverageFunction(0.0, sampleCount)
        elif type == "rmsfunction":
            valid, sampleCount = self.getIntAttribute(item, "sampleCount", valid)
            return valid, functions.RMSFunction(0.0, sampleCount)
        elif type == "stdevfunction":
            valid, sampleCount = self.getIntAttribute(item, "sampleCount", valid)
            return valid, functions.StdevFunction(0.0, sampleCount)
        elif type == "basicstatisticsfunction":
            valid, sampleCount = self.getIntAttribute(item, "sampleCount", valid)
            return valid, functions.BasicStatisticsFunction(0.0, sampleCount)
        elif type == "timedlimit":
            valid, sampleCount = self.getIntAttribute(item, "sampleCount", valid)
            valid, warningCount = self.getIntAttribute(item, "warningCount", valid)
            valid, faultCount = self.getIntAttribute(item, "faultCount", valid)
            return valid, limits.TimedLimit(sampleCount, warningCount, faultCount)
        elif type == "continuoustimedlimit":
            valid, warningCount = self.getIntAttribute(item, "warningCount", valid)
            valid, faultCount = self.getIntAttribute(item, "faultCount", valid)
            return valid, limits.ContinuousTimedLimit(warningCount, faultCount)
        elif type == "notequallimit":
            valid, getNumericAttribute = self.getNumericAttribute(item, "dataType", valid)
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, level = getNumericAttribute(item, "level", valid)
            return valid, limits.NotEqualLimit(limit, level)
        elif type == "equallimit":
            valid, getNumericAttribute = self.getNumericAttribute(item, "dataType", valid)
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, level = getNumericAttribute(item, "level", valid)
            return valid, limits.EqualLimit(limit, level)
        elif type == "lessthanlimit":
            valid, getNumericAttribute = self.getNumericAttribute(item, "dataType", valid)
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, level = getNumericAttribute(item, "level", valid)
            return valid, limits.LessThanLimit(limit, level)
        elif type == "lessthanequallimit":
            valid, getNumericAttribute = self.getNumericAttribute(item, "dataType", valid)
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, level = getNumericAttribute(item, "level", valid)
            return valid, limits.LessThanEqualLimit(limit, level)
        elif type == "greaterthanlimit":
            valid, getNumericAttribute = self.getNumericAttribute(item, "dataType", valid)
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, level = getNumericAttribute(item, "level", valid)
            return valid, limits.GreaterThanLimit(limit, level)
        elif type == "greaterthanequallimit":
            valid, getNumericAttribute = self.getNumericAttribute(item, "dataType", valid)
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, level = getNumericAttribute(item, "level", valid)
            return valid, limits.GreaterThanEqualLimit(limit, level)
        elif type == "notinrangelimit":
            valid, getNumericAttribute = self.getNumericAttribute(item, "dataType", valid)
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, lowLevel = getNumericAttribute(item, "lowLevel", valid)
            valid, highLevel = getNumericAttribute(item, "highLevel", valid)
            return valid, limits.NotInRangeLimit(limit, lowLevel, highLevel)
        elif type == "inrangelimit":
            valid, getNumericAttribute = self.getNumericAttribute(item, "dataType", valid)
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, lowLevel = getNumericAttribute(item, "lowLevel", valid)
            valid, highLevel = getNumericAttribute(item, "highLevel", valid)
            return valid, limits.InRangeLimit(limit, lowLevel, highLevel)
        elif type == "notintolerancelimit":
            valid, getNumericAttribute = self.getNumericAttribute(item, "dataType", valid)
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, level = getNumericAttribute(item, "level", valid)
            valid, tolerance = getNumericAttribute(item, "tolerance", valid)
            return valid, limits.NotInToleranceLimit(limit, level, tolerance)
        elif type == "intolerancelimit":
            valid, getNumericAttribute = self.getNumericAttribute(item, "dataType", valid)
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, level = getNumericAttribute(item, "level", valid)
            valid, tolerance = getNumericAttribute(item, "tolerance", valid)
            return valid, limits.InToleranceLimit(limit, level, tolerance)
        elif type == "anybitsetlimit":
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, bitMask = self.getIntAttribute(item, "bitMask", valid)
            return valid, limits.AnyBitSetLimit(limit, bitMask)
        elif type == "allbitsetlimit":
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, bitMask = self.getIntAttribute(item, "bitMask", valid)
            return valid, limits.AllBitSetLimit(limit, bitMask)
        elif type == "anybitnotsetlimit":
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, bitMask = self.getIntAttribute(item, "bitMask", valid)
            return valid, limits.AnyBitNotSetLimit(limit, bitMask)
        elif type == "allbitnotsetlimit":
            valid, limit = self.getLimitAttribute(item, "limit", valid)
            valid, bitMask = self.getIntAttribute(item, "bitMask", valid)
            return valid, limits.AllBitNotSetLimit(limit, bitMask)
        self.log.error(f"Unknown type {type} for tag {item.tag}.")
        return False, None

    def getAttribute(self, item, attribute, valid):
        result = item.get(attribute, None)
        if result is not None:
            return valid, result
        self.log.error(f"Expected attribute {attribute} on tag {item.tag} not found.")
        return False, result

    def getFloatAttribute(self, item, attribute, valid):
        valid, result = self.getAttribute(item, attribute, valid)
        try:
            if valid:
                return valid, float(result)
            return valid, 0.0
        except:
            self.log.error(f"Invalid float value {result} for attribute {attribute} on tag {item.tag}.")
            return False, 0.0

    def getIntAttribute(self, item, attribute, valid):
        valid, result = self.getAttribute(item, attribute, valid)
        try:
            if valid:
                if result.startswith("0x"):
                    return valid, int(result, 16)
                else:
                    return valid, int(result)
            return valid, 0
        except:
            self.log.error(f"Invalid int value {result} for attribute {attribute} on tag {item.tag}.")
            return False, 0

    def getBoolAttribute(self, item, attribute, valid):
        valid, result = self.getAttribute(item, attribute, valid)
        if valid:
            if result.upper() == "TRUE":
                return valid, True
            elif result.upper() == "FALSE":
                return valid, False
        self.log.error(f"Invalid bool value {result} for attribute {attribute} on tag {item.tag}.")
        return False, False

    def getLimitAttribute(self, item, attribute, valid):
        valid, result = self.getAttribute(item, attribute, valid)
        if valid:
            if result.upper() == "WARNING":
                return valid, limits.Limits.WARNING
            elif result.upper() == "FAULT":
                return valid, limits.Limits.FAULT
            elif result.upper() == "OK":
                return valid, limits.Limits.OK
            self.log.error(f"Unknown limit {result}, expecting one of the following OK, WARNING, FAULT.")
        return False, limits.Limits.NONE

    def getNumericAttribute(self, item, attribute, valid):
        valid, result = self.getAttribute(item, attribute, valid)
        if valid:
            if result.upper() == "INT":
                return valid, self.getIntAttribute
            elif result.upper() == "FLOAT":
                return valid, self.getFloatAttribute
            elif result.upper() == "BOOL":
                return valid, self.getBoolAttribute
            self.log.error(f"Unknown numeric {result}, expecting either INT, FLOAT, or BOOL.")
        return False, self.getIntAttribute

    def loadSettings(self, action, stagingSettings, productionSettings, filePath):
        valid, _ = action(stagingSettings, filePath)
        if valid:
            valid, _ = action(productionSettings, filePath)
        return valid
