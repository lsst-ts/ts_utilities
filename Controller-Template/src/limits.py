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

import enum

from . import utilities


class Limits(enum.Enum):
    NONE = 0
    OK = 1
    WARNING = 2
    FAULT = 3


class TimedLimit:
    def __init__(self, sampleCount, warningCount, faultCount):
        self.buffer = utilities.CircularBuffer(Limits.OK, sampleCount)
        self.warningCount = warningCount
        self.faultCount = faultCount
        self.warnings = 0
        self.faults = 0

    def evaluate(self, limit):
        oldLimit = self.buffer.read()
        if oldLimit == Limits.WARNING:
            self.warnings -= 1
        elif oldLimit == Limits.FAULT:
            self.faults -= 1
        self.buffer.write(limit)
        if limit == Limits.WARNING:
            self.warnings += 1
        elif limit == Limits.FAULT:
            self.faults += 1
        if self.faults > 0:
            return Limits.FAULT
        if self.warnings >= self.faultCount:
            return Limits.FAULT
        if self.warnings >= self.warningCount:
            return Limits.WARNING
        return Limits.OK


class ContinuousTimedLimit:
    def __init__(self, warningCount, faultCount):
        self.warningCount = warningCount
        self.faultCount = faultCount
        self.warnings = 0
        self.faults = 0

    def evaluate(self, limit):
        if limit == Limits.OK:
            self.warnings = 0
            self.faults = 0
        elif limit == Limits.WARNING:
            self.warnings += 1
        elif limit == Limits.FAULT:
            self.faults += 1
        if self.faults > 0:
            return Limits.FAULT
        if self.warnings >= self.faultCount:
            return Limits.FAULT
        if self.warnings >= self.warningCount:
            return Limits.WARNING
        return Limits.OK


class NotEqualLimit:
    def __init__(self, limit: Limits, level):
        self.limit = limit
        self.level = level

    def evaluate(self, x):
        if x != self.level:
            return self.limit
        return Limits.OK


class EqualLimit:
    def __init__(self, limit: Limits, level):
        self.limit = limit
        self.level = level

    def evaluate(self, x):
        if x == self.level:
            return self.limit
        return Limits.OK


class LessThanLimit:
    def __init__(self, limit: Limits, level):
        self.limit = limit
        self.level = level

    def evaluate(self, x):
        if x < self.level:
            return self.limit
        return Limits.OK


class LessThanEqualLimit:
    def __init__(self, limit: Limits, level):
        self.limit = limit
        self.level = level

    def evaluate(self, x):
        if x <= self.level:
            return self.limit
        return Limits.OK


class GreaterThanLimit:
    def __init__(self, limit: Limits, level):
        self.limit = limit
        self.level = level

    def evaluate(self, x):
        if x > self.level:
            return self.limit
        return Limits.OK


class GreaterThanEqualLimit:
    def __init__(self, limit: Limits, level):
        self.limit = limit
        self.level = level

    def evaluate(self, x):
        if x >= self.level:
            return self.limit
        return Limits.OK


class NotInRangeLimit:
    def __init__(self, limit: Limits, lowLevel, highLevel):
        self.limit = limit
        self.lowLevel = lowLevel
        self.highLevel = highLevel

    def evaluate(self, x):
        if x < self.lowLevel or x > self.highLevel:
            return self.limit
        return Limits.OK


class InRangeLimit:
    def __init__(self, limit: Limits, lowLevel, highLevel):
        self.limit = limit
        self.lowLevel = lowLevel
        self.highLevel = highLevel

    def evaluate(self, x):
        if x >= self.lowLevel and x <= self.highLevel:
            return self.limit
        return Limits.OK


class NotInToleranceLimit:
    def __init__(self, limit: Limits, level, tolerance):
        self.limit = limit
        self.lowLevel = level - tolerance
        self.highLevel = level + tolerance

    def evaluate(self, x):
        if x < self.lowLevel or x > self.highLevel:
            return self.limit
        return Limits.OK


class InToleranceLimit:
    def __init__(self, limit: Limits, level, tolerance):
        self.limit = limit
        self.lowLevel = level - tolerance
        self.highLevel = level + tolerance

    def evaluate(self, x):
        if x >= self.lowLevel and x <= self.highLevel:
            return self.limit
        return Limits.OK


class AnyBitSetLimit:
    def __init__(self, limit: Limits, bitMask):
        self.limit = limit
        self.bitMask = bitMask

    def evaluate(self, x):
        if (x & self.bitMask) != 0:
            return self.limit
        return Limits.OK


class AllBitSetLimit:
    def __init__(self, limit: Limits, bitMask):
        self.limit = limit
        self.bitMask = bitMask

    def evaluate(self, x):
        if (x & self.bitMask) == self.bitMask:
            return self.limit
        return Limits.OK


class AnyBitNotSetLimit:
    def __init__(self, limit: Limits, bitMask):
        self.limit = limit
        self.bitMask = bitMask

    def evaluate(self, x):
        if (x & self.bitMask) != self.bitMask:
            return self.limit
        return Limits.OK


class AllBitNotSetLimit:
    def __init__(self, limit: Limits, bitMask):
        self.limit = limit
        self.bitMask = bitMask

    def evaluate(self, x):
        if (x & self.bitMask) == 0:
            return self.limit
        return Limits.OK
