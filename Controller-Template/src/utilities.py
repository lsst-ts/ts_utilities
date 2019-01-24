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


class CircularBuffer:
    def __init__(self, defaultValue, size):
        self.size = size
        self.buffer = [defaultValue] * size
        self.writeIndex = 0
        self.readIndex = 0

    def write(self, value):
        self.buffer[self.writeIndex] = value
        self.writeIndex += 1
        if self.writeIndex >= self.size:
            self.writeIndex = 0
        
    def read(self):
        value = self.buffer[self.readIndex]
        self.readIndex += 1
        if self.readIndex >= self.size:
            self.readIndex = 0
        return value
