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

import math

from . import utilities


class LinearFunction:
    def __init__(self, m, b):
        self.m = m
        self.b = b

    def evaluate(self, x):
        return self.m * x + self.b


class Poly2Function:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def evaluate(self, x):
        return x * ((x * self.a) + self.b) + self.c


class Poly3Function:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def evaluate(self, x):
        return x * (x * ((x * self.a) + self.b) + self.c) + self.d


class Poly4Function:
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def evaluate(self, x):
        return x * (x * (x * ((x * self.a) + self.b) + self.c) + self.d) + self.e


class Poly5Function:
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def evaluate(self, x):
        return x * (x * (x * (x * ((x * self.a) + self.b) + self.c) + self.d) + self.e) + self.f


class Matrix1x2Function:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def evaluate(self, a, b):
        return a * self.a + b * self.b


class Matrix1x3Function:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def evaluate(self, a, b, c):
        return a * self.a + b * self.b + c * self.c


class Matrix1x4Function:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def evaluate(self, a, b, c, d):
        return a * self.a + b * self.b + c * self.c + d * self.d


class Matrix1x5Function:
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def evaluate(self, a, b, c, d, e):
        return a * self.a + b * self.b + c * self.c + d * self.d + e * self.e


class Matrix1x6Function:
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def evaluate(self, a, b, c, d, e, f):
        return a * self.a + b * self.b + c * self.c + d * self.d + e * self.e + f * self.f


class Matrix1x7Function:
    def __init__(self, a, b, c, d, e, f, g):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g

    def evaluate(self, a, b, c, d, e, f, g):
        return a * self.a + b * self.b + c * self.c + d * self.d + e * self.e + f * self.f + g * self.g


class Matrix1x8Function:
    def __init__(self, a, b, c, d, e, f, g, h):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h

    def evaluate(self, a, b, c, d, e, f, g, h):
        return a * self.a + b * self.b + c * self.c + d * self.d + e * self.e + f * self.f + g * self.g + h * self.h


class AnyBitSetFunction:
    def __init__(self, bitMask):
        self.bitMask = bitMask

    def evaluate(self, x):
        return (x & self.bitMask) != 0


class AllBitSetFunction:
    def __init__(self, bitMask):
        self.bitMask = bitMask

    def evaluate(self, x):
        return (x & self.bitMask) == self.bitMask


class AnyBitNotSetFunction:
    def __init__(self, bitMask):
        self.bitMask = bitMask

    def evaluate(self, x):
        return (x & self.bitMask) != self.bitMask


class AllBitNotSetFunction:
    def __init__(self, bitMask):
        self.bitMask = bitMask

    def evaluate(self, x):
        return (x & self.bitMask) == 0


class MinimumFunction:
    def __init__(self, initialValue, sampleCount):
        self.buffer = utilities.CircularBuffer(initialValue, sampleCount)

    def evaluate(self, x):
        self.buffer.write(x)
        return min(self.buffer.buffer)


class MaximumFunction:
    def __init__(self, initialValue, sampleCount):
        self.buffer = utilities.CircularBuffer(initialValue, sampleCount)

    def evaluate(self, x):
        self.buffer.write(x)
        return max(self.buffer.buffer)


class AverageFunction:
    def __init__(self, initialValue, sampleCount):
        self.buffer = utilities.CircularBuffer(initialValue, sampleCount)
        self.sum = initialValue

    def evaluate(self, x):
        self.sum -= self.buffer.read()
        self.sum += x
        self.buffer.write(x)
        return self.sum / self.buffer.size


class RMSFunction:
    def __init__(self, initialValue, sampleCount):
        self.buffer = utilities.CircularBuffer(initialValue, sampleCount)
        self.sum = initialValue

    def evaluate(self, x):
        value = self.buffer.read()
        self.sum -= value * value
        self.sum += x * x
        self.buffer.write(x)
        return math.sqrt(self.sum / self.buffer.size)


class StdevFunction:
    def __init__(self, initialValue, sampleCount):
        self.buffer = utilities.CircularBuffer(initialValue, sampleCount)
        self.avgSum = initialValue

    def evaluate(self, x):
        value = self.buffer.read()
        self.avgSum -= value
        self.avgSum += x
        self.buffer.write(x)
        avg = self.avgSum / self.buffer.size
        stdevSum = 0.0
        for value in self.buffer.buffer:
            stdevSum += (value - avg) * (value - avg)
        return math.sqrt(stdevSum / self.buffer.size)


class BasicStatisticsFunction:
    def __init__(self, initialValue, sampleCount):
        self.buffer = utilities.CircularBuffer(initialValue, sampleCount)
        self.avgSum = initialValue
        self.rmsSum = initialValue

    def evaluate(self, x):
        value = self.buffer.read()
        self.avgSum -= value
        self.rmsSum -= value * value
        self.avgSum += x
        self.rmsSum += x * x
        self.buffer.write(x)
        minValue = min(self.buffer.buffer)
        maxValue = max(self.buffer.buffer)
        avgValue = self.avgSum / self.buffer.size
        rmsValue = math.sqrt(self.rmsSum / self.buffer.size)
        stdevSum = 0.0
        for value in self.buffer.buffer:
            stdevSum += (value - avgValue) * (value - avgValue)
        stdevValue = math.sqrt(stdevSum / self.buffer.size)
        return minValue, maxValue, avgValue, rmsValue, stdevValue
