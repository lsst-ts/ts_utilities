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

import os
import sys
import time
import threading
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "python"))

import >NAMESPACE<.functions as functions
import >NAMESPACE<.limits as limits
import >NAMESPACE<.main as main
import >NAMESPACE<.salinterface as salinterface
from >NAMESPACE<.salinterface import SummaryStates
import >NAMESPACE<.settings as settings


class >SUBSYSTEM<(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="App")

    def run(self):
        main.run()


class >SUBSYSTEM<Tests(unittest.TestCase):
    def setUp(self):
        self.app = >SUBSYSTEM<()
        self.app.start()
        self.remote = salinterface.>SUBSYSTEM<Remote()
        data = self.waitUntil(self.remote.getNextEvent_summaryState, lambda x: x.summaryState == SummaryStates.StandbyState)
        self.assertEqual(data.summaryState, SummaryStates.StandbyState, "Should be in StandbyState")

    def tearDown(self):
        main.shutdownAction()
        self.remote.close()
        self.app.join()

    def test_stateMachine(self):
        self.remote.issueCommand_start("Default")
        data = self.waitUntil(self.remote.getNextEvent_summaryState, lambda x: x.summaryState == SummaryStates.DisabledState)
        self.assertEqual(data.summaryState, SummaryStates.DisabledState, "Should be in DisabledState")
        self.remote.issueCommand_enable(False)
        data = self.waitUntil(self.remote.getNextEvent_summaryState, lambda x: x.summaryState == SummaryStates.EnabledState)
        self.assertEqual(data.summaryState, SummaryStates.EnabledState, "Should be in EnabledState")
        self.remote.issueCommand_disable(False)
        data = self.waitUntil(self.remote.getNextEvent_summaryState, lambda x: x.summaryState == SummaryStates.DisabledState)
        self.assertEqual(data.summaryState, SummaryStates.DisabledState, "Should be in DisabledState")
        self.remote.issueCommand_standby(False)
        data = self.waitUntil(self.remote.getNextEvent_summaryState, lambda x: x.summaryState == SummaryStates.StandbyState)
        self.assertEqual(data.summaryState, SummaryStates.StandbyState, "Should be in StandbyState")

    def waitUntil(self, action, predicate, timeout=5):
        startTime = time.time()
        result, data = action()
        while not predicate(data) and (time.time() - startTime) < timeout:
            time.sleep(1)
            result, data = action()
        return data


class LimitTests(unittest.TestCase):
    def test_timedLimit(self):
        limit = limits.TimedLimit(10, 3, 5)
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.FAULT))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.FAULT))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.FAULT))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))

    def test_continuousTimedLimit(self):
        limit = limits.ContinuousTimedLimit(1, 3)
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(limits.Limits.FAULT))
        self.assertEqual(limits.Limits.OK, limit.evaluate(limits.Limits.OK))

    def test_notEqualLimit(self):
        limit = limits.NotEqualLimit(limits.Limits.WARNING, 1)
        self.assertEqual(limits.Limits.OK, limit.evaluate(1))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(0))

    def test_equalLimit(self):
        limit = limits.EqualLimit(limits.Limits.FAULT, 2)
        self.assertEqual(limits.Limits.OK, limit.evaluate(0))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(2))

    def test_lessThanLimit(self):
        limit = limits.LessThanLimit(limits.Limits.WARNING, 1)
        self.assertEqual(limits.Limits.OK, limit.evaluate(2))
        self.assertEqual(limits.Limits.OK, limit.evaluate(1))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(0))

    def test_lessThanEqualLimit(self):
        limit = limits.LessThanEqualLimit(limits.Limits.FAULT, 2)
        self.assertEqual(limits.Limits.OK, limit.evaluate(3))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(2))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(1))

    def test_greaterThanLimit(self):
        limit = limits.GreaterThanLimit(limits.Limits.WARNING, 1)
        self.assertEqual(limits.Limits.OK, limit.evaluate(0))
        self.assertEqual(limits.Limits.OK, limit.evaluate(1))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(2))

    def test_greaterThanEqualLimit(self):
        limit = limits.GreaterThanEqualLimit(limits.Limits.FAULT, 2)
        self.assertEqual(limits.Limits.OK, limit.evaluate(1))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(2))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(3))

    def test_notInRangeLimit(self):
        limit = limits.NotInRangeLimit(limits.Limits.WARNING, -1, 1)
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(-2))
        self.assertEqual(limits.Limits.OK, limit.evaluate(-1))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0))
        self.assertEqual(limits.Limits.OK, limit.evaluate(1))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(2))

    def test_inRangeLimit(self):
        limit = limits.InRangeLimit(limits.Limits.FAULT, -1, 1)
        self.assertEqual(limits.Limits.OK, limit.evaluate(-2))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(-1))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(0))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(1))
        self.assertEqual(limits.Limits.OK, limit.evaluate(2))

    def test_notInToleranceLimit(self):
        limit = limits.NotInToleranceLimit(limits.Limits.WARNING, 0, 1)
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(-2))
        self.assertEqual(limits.Limits.OK, limit.evaluate(-1))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0))
        self.assertEqual(limits.Limits.OK, limit.evaluate(1))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(2))

    def test_inToleranceLimit(self):
        limit = limits.InToleranceLimit(limits.Limits.FAULT, 0, 1)
        self.assertEqual(limits.Limits.OK, limit.evaluate(-2))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(-1))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(0))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(1))
        self.assertEqual(limits.Limits.OK, limit.evaluate(2))

    def test_anyBitSetLimit(self):
        limit = limits.AnyBitSetLimit(limits.Limits.WARNING, 0x30)
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x00))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x03))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(0x10))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(0x20))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(0x30))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x40))

    def test_allBitSetLimit(self):
        limit = limits.AllBitSetLimit(limits.Limits.FAULT, 0x30)
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x00))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x03))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x10))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x20))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(0x30))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x40))

    def test_anyBitNotSetLimit(self):
        limit = limits.AnyBitNotSetLimit(limits.Limits.WARNING, 0x30)
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(0x00))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(0x03))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(0x10))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(0x20))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x30))
        self.assertEqual(limits.Limits.WARNING, limit.evaluate(0x40))

    def test_allBitNotSetLimit(self):
        limit = limits.AllBitNotSetLimit(limits.Limits.FAULT, 0x30)
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(0x00))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(0x03))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x10))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x20))
        self.assertEqual(limits.Limits.OK, limit.evaluate(0x30))
        self.assertEqual(limits.Limits.FAULT, limit.evaluate(0x40))


class FunctionTests(unittest.TestCase):
    def test_linearFunction(self):
        fun = functions.LinearFunction(1.5, -1.0)
        self.assertEqual(0.5, fun.evaluate(1.0))

    def test_poly2Function(self):
        fun = functions.Poly2Function(1.0, 2.0, 3.0)
        self.assertEqual(4.25, fun.evaluate(0.5))

    def test_poly3Function(self):
        fun = functions.Poly3Function(1.0, 2.0, 3.0, 4.0)
        self.assertEqual(6.125, fun.evaluate(0.5))

    def test_poly4Function(self):
        fun = functions.Poly4Function(1.0, 2.0, 3.0, 4.0, 5.0)
        self.assertEqual(8.0625, fun.evaluate(0.5))

    def test_poly5Function(self):
        fun = functions.Poly5Function(1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        self.assertEqual(10.03125, fun.evaluate(0.5))

    def test_matrix1x2Function(self):
        fun = functions.Matrix1x2Function(1.0, 2.0)
        self.assertEqual(5.0, fun.evaluate(1.0, 2.0))

    def test_matrix1x3Function(self):
        fun = functions.Matrix1x3Function(1.0, 2.0, 3.0)
        self.assertEqual(14.0, fun.evaluate(1.0, 2.0, 3.0))

    def test_matrix1x4Function(self):
        fun = functions.Matrix1x4Function(1.0, 2.0, 3.0, 4.0)
        self.assertEqual(30.0, fun.evaluate(1.0, 2.0, 3.0, 4.0))

    def test_matrix1x5Function(self):
        fun = functions.Matrix1x5Function(1.0, 2.0, 3.0, 4.0, 5.0)
        self.assertEqual(55.0, fun.evaluate(1.0, 2.0, 3.0, 4.0, 5.0))

    def test_matrix1x6Function(self):
        fun = functions.Matrix1x6Function(1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        self.assertEqual(91.0, fun.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0))

    def test_matrix1x7Function(self):
        fun = functions.Matrix1x7Function(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0)
        self.assertEqual(140.0, fun.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0))

    def test_matrix1x8Function(self):
        fun = functions.Matrix1x8Function(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
        self.assertEqual(204.0, fun.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0))

    def test_anyBitSetFunction(self):
        fun = functions.AnyBitSetFunction(0x30)
        self.assertEqual(False, fun.evaluate(0x00))
        self.assertEqual(False, fun.evaluate(0x03))
        self.assertEqual(True, fun.evaluate(0x10))
        self.assertEqual(True, fun.evaluate(0x20))
        self.assertEqual(True, fun.evaluate(0x30))
        self.assertEqual(False, fun.evaluate(0x40))

    def test_allBitSetFunction(self):
        fun = functions.AllBitSetFunction(0x30)
        self.assertEqual(False, fun.evaluate(0x00))
        self.assertEqual(False, fun.evaluate(0x03))
        self.assertEqual(False, fun.evaluate(0x10))
        self.assertEqual(False, fun.evaluate(0x20))
        self.assertEqual(True, fun.evaluate(0x30))
        self.assertEqual(False, fun.evaluate(0x40))

    def test_anyBitNotSetFunction(self):
        fun = functions.AnyBitNotSetFunction(0x30)
        self.assertEqual(True, fun.evaluate(0x00))
        self.assertEqual(True, fun.evaluate(0x03))
        self.assertEqual(True, fun.evaluate(0x10))
        self.assertEqual(True, fun.evaluate(0x20))
        self.assertEqual(False, fun.evaluate(0x30))
        self.assertEqual(True, fun.evaluate(0x40))

    def test_allBitNotSetFunction(self):
        fun = functions.AllBitNotSetFunction(0x30)
        self.assertEqual(True, fun.evaluate(0x00))
        self.assertEqual(True, fun.evaluate(0x03))
        self.assertEqual(False, fun.evaluate(0x10))
        self.assertEqual(False, fun.evaluate(0x20))
        self.assertEqual(False, fun.evaluate(0x30))
        self.assertEqual(True, fun.evaluate(0x40))

    def test_minimumFunction(self):
        fun = functions.MinimumFunction(0.0, 10)
        self.assertEqual(0.0, fun.evaluate(1.0))
        self.assertEqual(0.0, fun.evaluate(2.0))
        self.assertEqual(0.0, fun.evaluate(3.0))
        self.assertEqual(0.0, fun.evaluate(4.0))
        self.assertEqual(0.0, fun.evaluate(5.0))
        self.assertEqual(0.0, fun.evaluate(6.0))
        self.assertEqual(0.0, fun.evaluate(7.0))
        self.assertEqual(0.0, fun.evaluate(8.0))
        self.assertEqual(0.0, fun.evaluate(9.0))
        self.assertEqual(1.0, fun.evaluate(10.0))
        self.assertEqual(2.0, fun.evaluate(11.0))

    def test_maximumFunction(self):
        fun = functions.MaximumFunction(0.0, 10)
        self.assertEqual(1.0, fun.evaluate(1.0))
        self.assertEqual(2.0, fun.evaluate(2.0))
        self.assertEqual(3.0, fun.evaluate(3.0))
        self.assertEqual(4.0, fun.evaluate(4.0))
        self.assertEqual(5.0, fun.evaluate(5.0))
        self.assertEqual(6.0, fun.evaluate(6.0))
        self.assertEqual(7.0, fun.evaluate(7.0))
        self.assertEqual(8.0, fun.evaluate(8.0))
        self.assertEqual(9.0, fun.evaluate(9.0))
        self.assertEqual(10.0, fun.evaluate(10.0))
        self.assertEqual(11.0, fun.evaluate(11.0))

    def test_averageFunction(self):
        fun = functions.AverageFunction(0.0, 10)
        self.assertEqual(0.1, fun.evaluate(1.0))
        self.assertEqual(0.3, fun.evaluate(2.0))
        self.assertEqual(0.6, fun.evaluate(3.0))
        self.assertEqual(1.0, fun.evaluate(4.0))
        self.assertEqual(1.5, fun.evaluate(5.0))
        self.assertEqual(2.1, fun.evaluate(6.0))
        self.assertEqual(2.8, fun.evaluate(7.0))
        self.assertEqual(3.6, fun.evaluate(8.0))
        self.assertEqual(4.5, fun.evaluate(9.0))
        self.assertEqual(5.5, fun.evaluate(10.0))
        self.assertEqual(6.5, fun.evaluate(11.0))

    def test_rmsFunction(self):
        fun = functions.RMSFunction(0.0, 10)
        self.assertAlmostEqual(0.316, fun.evaluate(1.0), 3)
        self.assertAlmostEqual(0.707, fun.evaluate(2.0), 3)
        self.assertAlmostEqual(1.183, fun.evaluate(3.0), 3)
        self.assertAlmostEqual(1.732, fun.evaluate(4.0), 3)
        self.assertAlmostEqual(2.345, fun.evaluate(5.0), 3)
        self.assertAlmostEqual(3.017, fun.evaluate(6.0), 3)
        self.assertAlmostEqual(3.742, fun.evaluate(7.0), 3)
        self.assertAlmostEqual(4.517, fun.evaluate(8.0), 3)
        self.assertAlmostEqual(5.339, fun.evaluate(9.0), 3)
        self.assertAlmostEqual(6.205, fun.evaluate(10.0), 3)
        self.assertAlmostEqual(7.106, fun.evaluate(11.0), 3)

    def test_stdevFunction(self):
        fun = functions.StdevFunction(0.0, 10)
        self.assertAlmostEqual(0.300, fun.evaluate(1.0), 3)
        self.assertAlmostEqual(0.640, fun.evaluate(2.0), 3)
        self.assertAlmostEqual(1.020, fun.evaluate(3.0), 3)
        self.assertAlmostEqual(1.414, fun.evaluate(4.0), 3)
        self.assertAlmostEqual(1.803, fun.evaluate(5.0), 3)
        self.assertAlmostEqual(2.166, fun.evaluate(6.0), 3)
        self.assertAlmostEqual(2.482, fun.evaluate(7.0), 3)
        self.assertAlmostEqual(2.728, fun.evaluate(8.0), 3)
        self.assertAlmostEqual(2.872, fun.evaluate(9.0), 3)
        self.assertAlmostEqual(2.872, fun.evaluate(10.0), 3)
        self.assertAlmostEqual(2.872, fun.evaluate(11.0), 3)

    def test_basicStatisticsFunction(self):
        fun = functions.BasicStatisticsFunction(0.0, 10)
        value = fun.evaluate(1.0)
        self.assertEqual(0.0, value[0])
        self.assertEqual(1.0, value[1])
        self.assertEqual(0.1, value[2])
        self.assertAlmostEqual(0.316, value[3], 3)
        self.assertAlmostEqual(0.300, value[4], 3)
        value = fun.evaluate(2.0)
        self.assertEqual(0.0, value[0])
        self.assertEqual(2.0, value[1])
        self.assertEqual(0.3, value[2])
        self.assertAlmostEqual(0.707, value[3], 3)
        self.assertAlmostEqual(0.640, value[4], 3)
        value = fun.evaluate(3.0)
        self.assertEqual(0.0, value[0])
        self.assertEqual(3.0, value[1])
        self.assertEqual(0.6, value[2])
        self.assertAlmostEqual(1.183, value[3], 3)
        self.assertAlmostEqual(1.020, value[4], 3)
        value = fun.evaluate(4.0)
        self.assertEqual(0.0, value[0])
        self.assertEqual(4.0, value[1])
        self.assertEqual(1.0, value[2])
        self.assertAlmostEqual(1.732, value[3], 3)
        self.assertAlmostEqual(1.414, value[4], 3)
        value = fun.evaluate(5.0)
        self.assertEqual(0.0, value[0])
        self.assertEqual(5.0, value[1])
        self.assertEqual(1.5, value[2])
        self.assertAlmostEqual(2.345, value[3], 3)
        self.assertAlmostEqual(1.803, value[4], 3)
        value = fun.evaluate(6.0)
        self.assertEqual(0.0, value[0])
        self.assertEqual(6.0, value[1])
        self.assertEqual(2.1, value[2])
        self.assertAlmostEqual(3.017, value[3], 3)
        self.assertAlmostEqual(2.166, value[4], 3)
        value = fun.evaluate(7.0)
        self.assertEqual(0.0, value[0])
        self.assertEqual(7.0, value[1])
        self.assertEqual(2.8, value[2])
        self.assertAlmostEqual(3.742, value[3], 3)
        self.assertAlmostEqual(2.482, value[4], 3)
        value = fun.evaluate(8.0)
        self.assertEqual(0.0, value[0])
        self.assertEqual(8.0, value[1])
        self.assertEqual(3.6, value[2])
        self.assertAlmostEqual(4.517, value[3], 3)
        self.assertAlmostEqual(2.728, value[4], 3)
        value = fun.evaluate(9.0)
        self.assertEqual(0.0, value[0])
        self.assertEqual(9.0, value[1])
        self.assertEqual(4.5, value[2])
        self.assertAlmostEqual(5.339, value[3], 3)
        self.assertAlmostEqual(2.872, value[4], 3)
        value = fun.evaluate(10.0)
        self.assertEqual(1.0, value[0])
        self.assertEqual(10.0, value[1])
        self.assertEqual(5.5, value[2])
        self.assertAlmostEqual(6.205, value[3], 3)
        self.assertAlmostEqual(2.872, value[4], 3)
        value = fun.evaluate(11.0)
        self.assertEqual(2.0, value[0])
        self.assertEqual(11.0, value[1])
        self.assertEqual(6.5, value[2])
        self.assertAlmostEqual(7.106, value[3], 3)
        self.assertAlmostEqual(2.872, value[4], 3)

class IndexMap:
    One = 1
    Two = 2
    Int = 0
    Float = 1
    Str = 2
    Bool = 3

class Foo:
    AnInt = 1
    AFloat = 2.0
    AString = "Hello"
    ABool = False
    AList = [1, 2.0, "3", True]
    ALinearFunc = functions.LinearFunction(1.0, 0.0)
    APoly2Func = functions.Poly2Function(1.0, 2.0, 3.0)
    APoly3Func = functions.Poly3Function(1.0, 2.0, 3.0, 4.0)
    APoly4Func = functions.Poly4Function(1.0, 2.0, 3.0, 4.0, 5.0)
    APoly5Func = functions.Poly5Function(1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
    AMatrix1x2Func = functions.Matrix1x2Function(0.0, 0.0)
    AMatrix1x3Func = functions.Matrix1x3Function(0.0, 0.0, 0.0)
    AMatrix1x4Func = functions.Matrix1x4Function(0.0, 0.0, 0.0, 0.0)
    AMatrix1x5Func = functions.Matrix1x5Function(0.0, 0.0, 0.0, 0.0, 0.0)
    AMatrix1x6Func = functions.Matrix1x6Function(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    AMatrix1x7Func = functions.Matrix1x7Function(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    AMatrix1x8Func = functions.Matrix1x8Function(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    AnAnyBitSetFunc = functions.AnyBitSetFunction(0x00)
    AnAllBitSetFunc = functions.AllBitSetFunction(0xFF)
    AnAnyBitNotSetFunc = functions.AnyBitNotSetFunction(0x30)
    AnAllBitNotSetFunc = functions.AllBitNotSetFunction(0xFE)
    AMinimumFunc = functions.MinimumFunction(0.0, 1)
    AMaximumFunc = functions.MaximumFunction(0.0, 1)
    AnAverageFunc = functions.AverageFunction(0.0, 1)
    ARMSFunc = functions.RMSFunction(0.0, 1)
    AStdevFunc = functions.StdevFunction(0.0, 1)
    ABasicStatisticsFunc = functions.BasicStatisticsFunction(0.0, 1)
    ATimedLim = limits.TimedLimit(5, 4, 5)
    AContinuousTimedLim = limits.ContinuousTimedLimit(4, 5)
    ANotEqualLim = limits.NotEqualLimit(limits.Limits.WARNING, 0)
    AEqualLim = limits.EqualLimit(limits.Limits.WARNING, 0)
    ALessThanLim = limits.LessThanLimit(limits.Limits.WARNING, 0)
    ALessThanEqualLim = limits.LessThanEqualLimit(limits.Limits.WARNING, 0)
    AGreaterThanLim = limits.GreaterThanLimit(limits.Limits.WARNING, 0)
    AGreaterThanEqualLim = limits.GreaterThanEqualLimit(limits.Limits.WARNING, 0)
    ANotInRangeLim = limits.NotInRangeLimit(limits.Limits.WARNING, 0, 0)
    AInRangeLim = limits.InRangeLimit(limits.Limits.WARNING, 0, 0)
    ANotInToleranceLim = limits.NotInToleranceLimit(limits.Limits.WARNING, 0, 1)
    AnInToleranceLim = limits.InToleranceLimit(limits.Limits.WARNING, 0, 0)
    AnAnyBitSetLim = limits.AnyBitSetLimit(limits.Limits.WARNING, 0)
    AnAllBitSetLim = limits.AllBitSetLimit(limits.Limits.WARNING, 1)
    AnAnyBitNotSetLim = limits.AnyBitNotSetLimit(limits.Limits.WARNING, 1)
    AnAllBitNotSetLim = limits.AllBitNotSetLimit(limits.Limits.WARNING, 1)


class SettingsContainer:
    Foo = Foo()


class SettingTests(unittest.TestCase):
    def setUp(self):
        self.indexMap = IndexMap()
        self.settingsContainer = SettingsContainer()
        self.set = settings.Settings(self.indexMap, self.settingsContainer, "/tmp")

    def tearDown(self):
        self.indexMap = IndexMap()
        self.settingsContainer = SettingsContainer()
        self.set = settings.Settings(self.indexMap, self.settingsContainer, "/tmp")

    def test_listValues(self):
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AList" index="Int" type="int" x="42"/>""")
        self.assertTrue(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AList" index="Float" type="float" x="42.2"/>""")

    def test_typeMismatch(self):
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnInt" type="str" x="42.132"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AList" index="Int" type="str" x="42"/>""")
        self.assertFalse(valid)

    def test_intValues(self):
        self.assertEqual(1, self.settingsContainer.Foo.AnInt)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnInt" type="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnInt" type="int" x="42.132"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnInt" type="int" x="abc"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnInt" type="int" x="42"/>""")
        self.assertTrue(valid)
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnInt" type="int" x="42"/>""")
        self.assertTrue(valid)
        self.assertEqual(42, self.settingsContainer.Foo.AnInt)
        self.assertEqual(int, type(self.settingsContainer.Foo.AnInt))

    def test_floatValues(self):
        self.assertEqual(2.0, self.settingsContainer.Foo.AFloat)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AFloat" type="float"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AFloat" type="float" x="42.132"/>""")
        self.assertTrue(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AFloat" type="float" x="abc"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AFloat" type="float" x="42"/>""")
        self.assertTrue(valid)
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AFloat" type="float" x="42.42"/>""")
        self.assertTrue(valid)
        self.assertEqual(42.42, self.settingsContainer.Foo.AFloat)
        self.assertEqual(float, type(self.settingsContainer.Foo.AFloat))

    def test_stringValues(self):
        self.assertEqual("Hello", self.settingsContainer.Foo.AString)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AString" type="str"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AString" type="str" x="42.132"/>""")
        self.assertTrue(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AString" type="str" x="abc"/>""")
        self.assertTrue(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AString" type="str" x="42"/>""")
        self.assertTrue(valid)
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AString" type="str" x="42.42"/>""")
        self.assertTrue(valid)
        self.assertEqual("42.42", self.settingsContainer.Foo.AString)
        self.assertEqual(str, type(self.settingsContainer.Foo.AString))

    def test_boolValues(self):
        self.assertEqual(False, self.settingsContainer.Foo.ABool)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ABool" type="bool"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ABool" type="bool" x="1"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ABool" type="bool" x="abc"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ABool" type="bool" x="t"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ABool" type="bool" x="true"/>""")
        self.assertTrue(valid)
        self.assertEqual(True, self.settingsContainer.Foo.ABool)
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ABool" type="bool" x="false"/>""")
        self.assertTrue(valid)
        self.assertEqual(False, self.settingsContainer.Foo.ABool)
        self.assertEqual(bool, type(self.settingsContainer.Foo.ABool))

    def test_linearFunction(self):
        self.assertEqual(2.0, self.settingsContainer.Foo.ALinearFunc.evaluate(2.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALinearFunc" type="linearfunction"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALinearFunc" type="linearfunction" m="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALinearFunc" type="linearfunction" m="2" b="3"/>""")        
        self.assertTrue(valid)
        self.assertEqual(2.0, self.settingsContainer.Foo.ALinearFunc.evaluate(2.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ALinearFunc" type="linearfunction" m="2" b="3"/>""")        
        self.assertTrue(valid)
        self.assertEqual(7.0, self.settingsContainer.Foo.ALinearFunc.evaluate(2.0))
        self.assertEqual(functions.LinearFunction, type(self.settingsContainer.Foo.ALinearFunc))

    def test_poly2Function(self):
        self.assertEqual(4.25, self.settingsContainer.Foo.APoly2Func.evaluate(0.5))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly2Func" type="poly2function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly2Func" type="poly2function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly2Func" type="poly2function" a="1" b="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly2Func" type="poly2function" a="1" b="2" c="4"/>""")        
        self.assertTrue(valid)
        self.assertEqual(4.25, self.settingsContainer.Foo.APoly2Func.evaluate(0.5))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="APoly2Func" type="poly2function" a="1" b="2" c="4"/>""")        
        self.assertTrue(valid)
        self.assertEqual(5.25, self.settingsContainer.Foo.APoly2Func.evaluate(0.5))
        self.assertEqual(functions.Poly2Function, type(self.settingsContainer.Foo.APoly2Func))

    def test_poly3Function(self):
        self.assertEqual(6.125, self.settingsContainer.Foo.APoly3Func.evaluate(0.5))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly3Func" type="poly3function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly3Func" type="poly3function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly3Func" type="poly3function" a="1" b="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly3Func" type="poly3function" a="1" b="2" c="3"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly3Func" type="poly3function" a="1" b="2" c="3" d="5"/>""")        
        self.assertTrue(valid)
        self.assertEqual(6.125, self.settingsContainer.Foo.APoly3Func.evaluate(0.5))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="APoly3Func" type="poly3function" a="1" b="2" c="3" d="5"/>""")     
        self.assertTrue(valid)
        self.assertEqual(7.125, self.settingsContainer.Foo.APoly3Func.evaluate(0.5))
        self.assertEqual(functions.Poly3Function, type(self.settingsContainer.Foo.APoly3Func))

    def test_poly4Function(self):
        self.assertEqual(8.0625, self.settingsContainer.Foo.APoly4Func.evaluate(0.5))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly4Func" type="poly4function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly4Func" type="poly4function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly4Func" type="poly4function" a="1" b="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly4Func" type="poly4function" a="1" b="2" c="3"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly4Func" type="poly4function" a="1" b="2" c="3" d="4"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly4Func" type="poly4function" a="1" b="2" c="3" d="4" e="6"/>""")        
        self.assertTrue(valid)
        self.assertEqual(8.0625, self.settingsContainer.Foo.APoly4Func.evaluate(0.5))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="APoly4Func" type="poly4function" a="1" b="2" c="3" d="4" e="6"/>""")        
        self.assertTrue(valid)
        self.assertEqual(9.0625, self.settingsContainer.Foo.APoly4Func.evaluate(0.5))
        self.assertEqual(functions.Poly4Function, type(self.settingsContainer.Foo.APoly4Func))

    def test_poly5Function(self):
        self.assertEqual(10.03125, self.settingsContainer.Foo.APoly5Func.evaluate(0.5))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly5Func" type="poly5function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly5Func" type="poly5function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly5Func" type="poly5function" a="1" b="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly5Func" type="poly5function" a="1" b="2" c="3"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly5Func" type="poly5function" a="1" b="2" c="3" d="4"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly5Func" type="poly5function" a="1" b="2" c="3" d="4" e="5"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="APoly5Func" type="poly5function" a="1" b="2" c="3" d="4" e="5" f="7"/>""")        
        self.assertTrue(valid)
        self.assertEqual(10.03125, self.settingsContainer.Foo.APoly5Func.evaluate(0.5))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="APoly5Func" type="poly5function" a="1" b="2" c="3" d="4" e="5" f="7"/>""")        
        self.assertTrue(valid)
        self.assertEqual(11.03125, self.settingsContainer.Foo.APoly5Func.evaluate(0.5))
        self.assertEqual(functions.Poly5Function, type(self.settingsContainer.Foo.APoly5Func))

    def test_matrix1x2Function(self):
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x2Func.evaluate(1.0, 2.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x2Func" type="matrix1x2function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x2Func" type="matrix1x2function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x2Func" type="matrix1x2function" a="1" b="2"/>""")        
        self.assertTrue(valid)
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x2Func.evaluate(1.0, 2.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AMatrix1x2Func" type="matrix1x2function" a="1" b="2"/>""")        
        self.assertTrue(valid)
        self.assertEqual(5.0, self.settingsContainer.Foo.AMatrix1x2Func.evaluate(1.0, 2.0))
        self.assertEqual(functions.Matrix1x2Function, type(self.settingsContainer.Foo.AMatrix1x2Func))

    def test_matrix1x3Function(self):
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x3Func.evaluate(1.0, 2.0, 3.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x3Func" type="matrix1x3function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x3Func" type="matrix1x3function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x3Func" type="matrix1x3function" a="1" b="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x3Func" type="matrix1x3function" a="1" b="2" c="3"/>""")        
        self.assertTrue(valid)
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x3Func.evaluate(1.0, 2.0, 3.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AMatrix1x3Func" type="matrix1x3function" a="1" b="2" c="3"/>""")        
        self.assertTrue(valid)
        self.assertEqual(14.0, self.settingsContainer.Foo.AMatrix1x3Func.evaluate(1.0, 2.0, 3.0))
        self.assertEqual(functions.Matrix1x3Function, type(self.settingsContainer.Foo.AMatrix1x3Func))

    def test_matrix1x4Function(self):
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x4Func.evaluate(1.0, 2.0, 3.0, 4.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x4Func" type="matrix1x4function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x4Func" type="matrix1x4function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x4Func" type="matrix1x4function" a="1" b="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x4Func" type="matrix1x4function" a="1" b="2" c="3"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x4Func" type="matrix1x4function" a="1" b="2" c="3" d="4"/>""")        
        self.assertTrue(valid)
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x4Func.evaluate(1.0, 2.0, 3.0, 4.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AMatrix1x4Func" type="matrix1x4function" a="1" b="2" c="3" d="4"/>""")        
        self.assertTrue(valid)
        self.assertEqual(30.0, self.settingsContainer.Foo.AMatrix1x4Func.evaluate(1.0, 2.0, 3.0, 4.0))
        self.assertEqual(functions.Matrix1x4Function, type(self.settingsContainer.Foo.AMatrix1x4Func))

    def test_matrix1x5Function(self):
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x5Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x5Func" type="matrix1x5function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x5Func" type="matrix1x5function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x5Func" type="matrix1x5function" a="1" b="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x5Func" type="matrix1x5function" a="1" b="2" c="3"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x5Func" type="matrix1x5function" a="1" b="2" c="3" d="4"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x5Func" type="matrix1x5function" a="1" b="2" c="3" d="4" e="5"/>""")        
        self.assertTrue(valid)
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x5Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AMatrix1x5Func" type="matrix1x5function" a="1" b="2" c="3" d="4" e="5"/>""")        
        self.assertTrue(valid)
        self.assertEqual(55.0, self.settingsContainer.Foo.AMatrix1x5Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0))
        self.assertEqual(functions.Matrix1x5Function, type(self.settingsContainer.Foo.AMatrix1x5Func))

    def test_matrix1x6Function(self):
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x6Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x6Func" type="matrix1x6function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x6Func" type="matrix1x6function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x6Func" type="matrix1x6function" a="1" b="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x6Func" type="matrix1x6function" a="1" b="2" c="3"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x6Func" type="matrix1x6function" a="1" b="2" c="3" d="4"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x6Func" type="matrix1x6function" a="1" b="2" c="3" d="4" e="5"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x6Func" type="matrix1x6function" a="1" b="2" c="3" d="4" e="5" f="6"/>""")
        self.assertTrue(valid)
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x6Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AMatrix1x6Func" type="matrix1x6function" a="1" b="2" c="3" d="4" e="5" f="6"/>""")        
        self.assertTrue(valid)
        self.assertEqual(91.0, self.settingsContainer.Foo.AMatrix1x6Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0))
        self.assertEqual(functions.Matrix1x6Function, type(self.settingsContainer.Foo.AMatrix1x6Func))

    def test_matrix1x7Function(self):
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x7Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x7Func" type="matrix1x7function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x7Func" type="matrix1x7function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x7Func" type="matrix1x7function" a="1" b="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x7Func" type="matrix1x7function" a="1" b="2" c="3"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x7Func" type="matrix1x7function" a="1" b="2" c="3" d="4"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x7Func" type="matrix1x7function" a="1" b="2" c="3" d="4" e="5"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x7Func" type="matrix1x7function" a="1" b="2" c="3" d="4" e="5" f="6"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x7Func" type="matrix1x7function" a="1" b="2" c="3" d="4" e="5" f="6" g="7"/>""")
        self.assertTrue(valid)
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x7Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AMatrix1x7Func" type="matrix1x7function" a="1" b="2" c="3" d="4" e="5" f="6" g="7"/>""")        
        self.assertTrue(valid)
        self.assertEqual(140.0, self.settingsContainer.Foo.AMatrix1x7Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0))
        self.assertEqual(functions.Matrix1x7Function, type(self.settingsContainer.Foo.AMatrix1x7Func))

    def test_matrix1x8Function(self):
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x8Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x8Func" type="matrix1x8function"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x8Func" type="matrix1x8function" a="1"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x8Func" type="matrix1x8function" a="1" b="2"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x8Func" type="matrix1x8function" a="1" b="2" c="3"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x8Func" type="matrix1x8function" a="1" b="2" c="3" d="4"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x8Func" type="matrix1x8function" a="1" b="2" c="3" d="4" e="5"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x8Func" type="matrix1x8function" a="1" b="2" c="3" d="4" e="5" f="6"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x8Func" type="matrix1x8function" a="1" b="2" c="3" d="4" e="5" f="6" g="7"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMatrix1x8Func" type="matrix1x8function" a="1" b="2" c="3" d="4" e="5" f="6" g="7" h="8"/>""")
        self.assertTrue(valid)
        self.assertEqual(0.0, self.settingsContainer.Foo.AMatrix1x8Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AMatrix1x8Func" type="matrix1x8function" a="1" b="2" c="3" d="4" e="5" f="6" g="7" h="8"/>""")        
        self.assertTrue(valid)
        self.assertEqual(204.0, self.settingsContainer.Foo.AMatrix1x8Func.evaluate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0))
        self.assertEqual(functions.Matrix1x8Function, type(self.settingsContainer.Foo.AMatrix1x8Func))

    def test_anyBitSetFunction(self):
        self.assertEqual(False, self.settingsContainer.Foo.AnAnyBitSetFunc.evaluate(0x20))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAnyBitSetFunc" type="anybitsetfunction"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAnyBitSetFunc" type="anybitsetfunction" bitMask="0x30"/>""")        
        self.assertTrue(valid)
        self.assertEqual(False, self.settingsContainer.Foo.AnAnyBitSetFunc.evaluate(0x20))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnAnyBitSetFunc" type="anybitsetfunction" bitMask="0x30"/>""")        
        self.assertTrue(valid)
        self.assertEqual(True, self.settingsContainer.Foo.AnAnyBitSetFunc.evaluate(0x20))
        self.assertEqual(functions.AnyBitSetFunction, type(self.settingsContainer.Foo.AnAnyBitSetFunc))

    def test_allBitSetFunction(self):
        self.assertEqual(False, self.settingsContainer.Foo.AnAllBitSetFunc.evaluate(0x30))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAllBitSetFunc" type="allbitsetfunction"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAllBitSetFunc" type="allbitsetfunction" bitMask="0x30"/>""")        
        self.assertTrue(valid)
        self.assertEqual(False, self.settingsContainer.Foo.AnAllBitSetFunc.evaluate(0x30))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnAllBitSetFunc" type="allbitsetfunction" bitMask="0x30"/>""")        
        self.assertTrue(valid)
        self.assertEqual(True, self.settingsContainer.Foo.AnAllBitSetFunc.evaluate(0x30))
        self.assertEqual(functions.AllBitSetFunction, type(self.settingsContainer.Foo.AnAllBitSetFunc))

    def test_anyBitNotSetFunction(self):
        self.assertEqual(False, self.settingsContainer.Foo.AnAnyBitNotSetFunc.evaluate(0x30))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAnyBitNotSetFunc" type="anybitnotsetfunction"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAnyBitNotSetFunc" type="anybitnotsetfunction" bitMask="0x40"/>""")        
        self.assertTrue(valid)
        self.assertEqual(False, self.settingsContainer.Foo.AnAnyBitNotSetFunc.evaluate(0x30))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnAnyBitNotSetFunc" type="anybitnotsetfunction" bitMask="0x40"/>""")        
        self.assertTrue(valid)
        self.assertEqual(True, self.settingsContainer.Foo.AnAnyBitNotSetFunc.evaluate(0x30))
        self.assertEqual(functions.AnyBitNotSetFunction, type(self.settingsContainer.Foo.AnAnyBitNotSetFunc))

    def test_allBitNotSetFunction(self):
        self.assertEqual(False, self.settingsContainer.Foo.AnAllBitNotSetFunc.evaluate(0xFE))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAllBitNotSetFunc" type="allbitnotsetfunction"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAllBitNotSetFunc" type="allbitnotsetfunction" bitMask="0x01"/>""")        
        self.assertTrue(valid)
        self.assertEqual(False, self.settingsContainer.Foo.AnAllBitNotSetFunc.evaluate(0xFE))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnAllBitNotSetFunc" type="allbitnotsetfunction" bitMask="0x01"/>""")        
        self.assertTrue(valid)
        self.assertEqual(True, self.settingsContainer.Foo.AnAllBitNotSetFunc.evaluate(0xFE))
        self.assertEqual(functions.AllBitNotSetFunction, type(self.settingsContainer.Foo.AnAllBitNotSetFunc))

    def test_minimumFunction(self):
        self.assertEqual(5.0, self.settingsContainer.Foo.AMinimumFunc.evaluate(5.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMinimumFunc" type="minimumfunction"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMinimumFunc" type="minimumfunction" sampleCount="2"/>""")        
        self.assertTrue(valid)
        self.assertEqual(4.0, self.settingsContainer.Foo.AMinimumFunc.evaluate(4.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AMinimumFunc" type="minimumfunction" sampleCount="2"/>""")        
        self.assertTrue(valid)
        self.assertEqual(0.0, self.settingsContainer.Foo.AMinimumFunc.evaluate(10.0))
        self.assertEqual(functions.MinimumFunction, type(self.settingsContainer.Foo.AMinimumFunc))

    def test_maximumFunction(self):
        self.assertEqual(5.0, self.settingsContainer.Foo.AMaximumFunc.evaluate(5.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMaximumFunc" type="maximumfunction"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AMaximumFunc" type="maximumfunction" sampleCount="2"/>""")        
        self.assertTrue(valid)
        self.assertEqual(6.0, self.settingsContainer.Foo.AMaximumFunc.evaluate(6.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AMaximumFunc" type="maximumfunction" sampleCount="2"/>""")        
        self.assertTrue(valid)
        self.assertEqual(2.0, self.settingsContainer.Foo.AMaximumFunc.evaluate(2.0))
        self.assertEqual(functions.MaximumFunction, type(self.settingsContainer.Foo.AMaximumFunc))

    def test_averageFuntion(self):
        self.assertEqual(6.0, self.settingsContainer.Foo.AnAverageFunc.evaluate(6.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAverageFunc" type="averagefunction"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAverageFunc" type="averagefunction" sampleCount="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(5.0, self.settingsContainer.Foo.AnAverageFunc.evaluate(5.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnAverageFunc" type="averagefunction" sampleCount="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(2.5, self.settingsContainer.Foo.AnAverageFunc.evaluate(5.0))
        self.assertEqual(functions.AverageFunction, type(self.settingsContainer.Foo.AnAverageFunc))

    def test_rmsFunction(self):
        self.assertEqual(2.0, self.settingsContainer.Foo.ARMSFunc.evaluate(2.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ARMSFunc" type="rmsfunction"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ARMSFunc" type="rmsfunction" sampleCount="2"/>""")        
        self.assertTrue(valid)
        self.assertEqual(5.0, self.settingsContainer.Foo.ARMSFunc.evaluate(5.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ARMSFunc" type="rmsfunction" sampleCount="2"/>""")        
        self.assertTrue(valid)
        self.assertAlmostEqual(3.536, self.settingsContainer.Foo.ARMSFunc.evaluate(5.0), 3)
        self.assertEqual(functions.RMSFunction, type(self.settingsContainer.Foo.ARMSFunc))

    def test_stdevFunction(self):
        self.assertEqual(0.0, self.settingsContainer.Foo.AStdevFunc.evaluate(12.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AStdevFunc" type="stdevfunction"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AStdevFunc" type="stdevfunction" sampleCount="2"/>""")        
        self.assertTrue(valid)
        self.assertEqual(0.0, self.settingsContainer.Foo.AStdevFunc.evaluate(3.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AStdevFunc" type="stdevfunction" sampleCount="2"/>""")        
        self.assertTrue(valid)
        self.assertEqual(1.5, self.settingsContainer.Foo.AStdevFunc.evaluate(3.0))
        self.assertEqual(functions.StdevFunction, type(self.settingsContainer.Foo.AStdevFunc))

    def test_basicStatisticsFunction(self):
        self.assertEqual((5.0, 5.0, 5.0, 5.0, 0.0), self.settingsContainer.Foo.ABasicStatisticsFunc.evaluate(5.0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ABasicStatisticsFunc" type="basicstatisticsfunction"/>""")        
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ABasicStatisticsFunc" type="basicstatisticsfunction" sampleCount="2"/>""")        
        self.assertTrue(valid)
        self.assertEqual((3.0, 3.0, 3.0, 3.0, 0.0), self.settingsContainer.Foo.ABasicStatisticsFunc.evaluate(3.0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ABasicStatisticsFunc" type="basicstatisticsfunction" sampleCount="2"/>""")        
        self.assertTrue(valid)
        value = self.settingsContainer.Foo.ABasicStatisticsFunc.evaluate(3.0)
        self.assertEqual(0.0, value[0])
        self.assertEqual(3.0, value[1])
        self.assertEqual(1.5, value[2])
        self.assertAlmostEqual(2.121, value[3], 3)
        self.assertEqual(1.5, value[4])
        self.assertEqual(functions.BasicStatisticsFunction, type(self.settingsContainer.Foo.ABasicStatisticsFunc))

    def test_timedLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ATimedLim.evaluate(limits.Limits.WARNING))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ATimedLim" type="timedlimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ATimedLim" type="timedlimit" sampleCount="5"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ATimedLim" type="timedlimit" sampleCount="5" warningCount="1"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ATimedLim" type="timedlimit" sampleCount="5" warningCount="1" faultCount="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ATimedLim.evaluate(limits.Limits.WARNING))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ATimedLim" type="timedlimit" sampleCount="5" warningCount="1" faultCount="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.WARNING, self.settingsContainer.Foo.ATimedLim.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.ATimedLim.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.TimedLimit, type(self.settingsContainer.Foo.ATimedLim))

    def test_continuousTimedLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AContinuousTimedLim.evaluate(limits.Limits.WARNING))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AContinuousTimedLim" type="continuoustimedlimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AContinuousTimedLim" type="continuoustimedlimit" warningCount="1"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AContinuousTimedLim" type="continuoustimedlimit" warningCount="1" faultCount="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AContinuousTimedLim.evaluate(limits.Limits.WARNING))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AContinuousTimedLim" type="continuoustimedlimit" sampleCount="5" warningCount="1" faultCount="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.WARNING, self.settingsContainer.Foo.AContinuousTimedLim.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.AContinuousTimedLim.evaluate(limits.Limits.WARNING))
        self.assertEqual(limits.ContinuousTimedLimit, type(self.settingsContainer.Foo.AContinuousTimedLim))

    def test_notEqualLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ANotEqualLim.evaluate(0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotEqualLim" type="notequallimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotEqualLim" type="notequallimit" dataType="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotEqualLim" type="notequallimit" dataType="int" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotEqualLim" type="notequallimit" dataType="int" limit="FAULT" level="1"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ANotEqualLim.evaluate(0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ANotEqualLim" type="notequallimit" dataType="int" limit="FAULT" level="1"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.ANotEqualLim.evaluate(0))
        self.assertEqual(limits.NotEqualLimit, type(self.settingsContainer.Foo.ANotEqualLim))

    def test_equalLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AEqualLim.evaluate(1))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AEqualLim" type="equallimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AEqualLim" type="equallimit" dataType="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AEqualLim" type="equallimit" dataType="int" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AEqualLim" type="equallimit" dataType="int" limit="FAULT" level="1"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AEqualLim.evaluate(1))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AEqualLim" type="equallimit" dataType="int" limit="FAULT" level="1"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.AEqualLim.evaluate(1))
        self.assertEqual(limits.EqualLimit, type(self.settingsContainer.Foo.AEqualLim))

    def test_lessThanLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ALessThanLim.evaluate(1))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALessThanLim" type="lessthanlimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALessThanLim" type="lessthanlimit" dataType="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALessThanLim" type="lessthanlimit" dataType="int" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALessThanLim" type="lessthanlimit" dataType="int" limit="FAULT" level="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ALessThanLim.evaluate(1))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ALessThanLim" type="lessthanlimit" dataType="int" limit="FAULT" level="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.ALessThanLim.evaluate(1))
        self.assertEqual(limits.LessThanLimit, type(self.settingsContainer.Foo.ALessThanLim))

    def test_lessThanEqualLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ALessThanEqualLim.evaluate(1))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALessThanEqualLim" type="lessthanequallimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALessThanEqualLim" type="lessthanequallimit" dataType="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALessThanEqualLim" type="lessthanequallimit" dataType="int" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ALessThanEqualLim" type="lessthanequallimit" dataType="int" limit="FAULT" level="1"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ALessThanEqualLim.evaluate(1))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ALessThanEqualLim" type="lessthanequallimit" dataType="int" limit="FAULT" level="1"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.ALessThanEqualLim.evaluate(1))
        self.assertEqual(limits.LessThanEqualLimit, type(self.settingsContainer.Foo.ALessThanEqualLim))

    def test_greaterThanLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AGreaterThanLim.evaluate(-1))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AGreaterThanLim" type="greaterthanlimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AGreaterThanLim" type="greaterthanlimit" dataType="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AGreaterThanLim" type="greaterthanlimit" dataType="int" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AGreaterThanLim" type="greaterthanlimit" dataType="int" limit="FAULT" level="-2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AGreaterThanLim.evaluate(-1))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AGreaterThanLim" type="greaterthanlimit" dataType="int" limit="FAULT" level="-2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.AGreaterThanLim.evaluate(-1))
        self.assertEqual(limits.GreaterThanLimit, type(self.settingsContainer.Foo.AGreaterThanLim))

    def test_greaterThanEqualLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AGreaterThanEqualLim.evaluate(-1))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AGreaterThanEqualLim" type="greaterthanequallimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AGreaterThanEqualLim" type="greaterthanequallimit" dataType="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AGreaterThanEqualLim" type="greaterthanequallimit" dataType="int" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AGreaterThanEqualLim" type="greaterthanequallimit" dataType="int" limit="FAULT" level="-1"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AGreaterThanEqualLim.evaluate(-1))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AGreaterThanEqualLim" type="greaterthanequallimit" dataType="int" limit="FAULT" level="-1"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.AGreaterThanEqualLim.evaluate(-1))
        self.assertEqual(limits.GreaterThanEqualLimit, type(self.settingsContainer.Foo.AGreaterThanEqualLim))

    def test_notInRangeLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ANotInRangeLim.evaluate(0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotInRangeLim" type="notinrangelimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotInRangeLim" type="notinrangelimit" dataType="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotInRangeLim" type="notinrangelimit" dataType="int" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotInRangeLim" type="notinrangelimit" dataType="int" limit="FAULT" lowLevel="1"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotInRangeLim" type="notinrangelimit" dataType="int" limit="FAULT" lowLevel="1" highLevel="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ANotInRangeLim.evaluate(0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ANotInRangeLim" type="notinrangelimit" dataType="int" limit="FAULT" lowLevel="1" highLevel="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.ANotInRangeLim.evaluate(-1))
        self.assertEqual(limits.NotInRangeLimit, type(self.settingsContainer.Foo.ANotInRangeLim))

    def test_inRangeLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AInRangeLim.evaluate(10))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AInRangeLim" type="inrangelimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AInRangeLim" type="inrangelimit" dataType="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AInRangeLim" type="inrangelimit" dataType="int" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AInRangeLim" type="inrangelimit" dataType="int" limit="FAULT" lowLevel="9"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AInRangeLim" type="inrangelimit" dataType="int" limit="FAULT" lowLevel="9" highLevel="11"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AInRangeLim.evaluate(10))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AInRangeLim" type="inrangelimit" dataType="int" limit="FAULT" lowLevel="9" highLevel="11"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.AInRangeLim.evaluate(10))
        self.assertEqual(limits.InRangeLimit, type(self.settingsContainer.Foo.AInRangeLim))

    def test_notInToleranceLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ANotInToleranceLim.evaluate(0))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotInToleranceLim" type="notintolerancelimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotInToleranceLim" type="notintolerancelimit" dataType="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotInToleranceLim" type="notintolerancelimit" dataType="int" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotInToleranceLim" type="notintolerancelimit" dataType="int" limit="FAULT" level="1"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="ANotInToleranceLim" type="notintolerancelimit" dataType="int" limit="FAULT" level="1" tolerance="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.ANotInToleranceLim.evaluate(0))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="ANotInToleranceLim" type="notintolerancelimit" dataType="int" limit="FAULT" level="3" tolerance="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.ANotInToleranceLim.evaluate(0))
        self.assertEqual(limits.NotInToleranceLimit, type(self.settingsContainer.Foo.ANotInToleranceLim))

    def test_inToleranceLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AnInToleranceLim.evaluate(-10))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnInToleranceLim" type="intolerancelimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnInToleranceLim" type="intolerancelimit" dataType="int"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnInToleranceLim" type="intolerancelimit" dataType="int" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnInToleranceLim" type="intolerancelimit" dataType="int" limit="FAULT" level="1"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnInToleranceLim" type="intolerancelimit" dataType="int" limit="FAULT" level="1" tolerance="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AnInToleranceLim.evaluate(-10))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnInToleranceLim" type="intolerancelimit" dataType="int" limit="FAULT" level="-10" tolerance="2"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.AnInToleranceLim.evaluate(-10))
        self.assertEqual(limits.InToleranceLimit, type(self.settingsContainer.Foo.AnInToleranceLim))

    def test_anyBitSetLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AnAnyBitSetLim.evaluate(4))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAnyBitSetLim" type="anybitsetlimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAnyBitSetLim" type="anybitsetlimit" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAnyBitSetLim" type="anybitsetlimit" limit="FAULT" bitMask="0x04"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AnAnyBitSetLim.evaluate(4))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnAnyBitSetLim" type="anybitsetlimit" limit="FAULT" bitMask="0x04"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.AnAnyBitSetLim.evaluate(4))
        self.assertEqual(limits.AnyBitSetLimit, type(self.settingsContainer.Foo.AnAnyBitSetLim))

    def test_allBitSetLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AnAllBitSetLim.evaluate(4))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAllBitSetLim" type="allbitsetlimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAllBitSetLim" type="allbitsetlimit" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAllBitSetLim" type="allbitsetlimit" limit="FAULT" bitMask="0x04"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AnAllBitSetLim.evaluate(4))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnAllBitSetLim" type="allbitsetlimit" limit="FAULT" bitMask="0x04"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.AnAllBitSetLim.evaluate(4))
        self.assertEqual(limits.AllBitSetLimit, type(self.settingsContainer.Foo.AnAllBitSetLim))

    def test_anyBitNotSetLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AnAnyBitNotSetLim.evaluate(1))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAnyBitNotSetLim" type="anybitnotsetlimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAnyBitNotSetLim" type="anybitnotsetlimit" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAnyBitNotSetLim" type="anybitnotsetlimit" limit="FAULT" bitMask="0x04"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AnAnyBitNotSetLim.evaluate(1))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnAnyBitNotSetLim" type="anybitnotsetlimit" limit="FAULT" bitMask="0x04"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.AnAnyBitNotSetLim.evaluate(1))
        self.assertEqual(limits.AnyBitNotSetLimit, type(self.settingsContainer.Foo.AnAnyBitNotSetLim))

    def test_allBitNotSetLimit(self):
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AnAllBitNotSetLim.evaluate(1))
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAllBitNotSetLim" type="allbitnotsetlimit"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAllBitNotSetLim" type="allbitnotsetlimit" limit="FAULT"/>""")
        self.assertFalse(valid)
        valid = self.set.loadTempSettings(True, """<Setting object="Foo" field="AnAllBitNotSetLim" type="allbitnotsetlimit" limit="FAULT" bitMask="0x04"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.OK, self.settingsContainer.Foo.AnAllBitNotSetLim.evaluate(1))
        valid = self.set.loadTempSettings(False, """<Setting object="Foo" field="AnAllBitNotSetLim" type="allbitnotsetlimit" limit="FAULT" bitMask="0x04"/>""")
        self.assertTrue(valid)
        self.assertEqual(limits.Limits.FAULT, self.settingsContainer.Foo.AnAllBitNotSetLim.evaluate(1))
        self.assertEqual(limits.AllBitNotSetLimit, type(self.settingsContainer.Foo.AnAllBitNotSetLim))

if __name__ == '__main__':
    unittest.main()
