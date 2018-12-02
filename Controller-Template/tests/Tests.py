import sys
import os
import threading
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import Main
import {subsystem}Remote
from {subsystem}Enumerations import SummaryStates
import time

class {subsystem}(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = "App")
        
    def run(self):
        Main.run()

class {subsystem}Tests(unittest.TestCase):
    def setUp(self):
        self.app = {subsystem}()
        self.app.start()
        self.remote = {subsystem}Remote.{subsystem}Remote()
        data = self.waitUntil(self.remote.getNextEvent_summaryState, lambda x: x.summaryState == SummaryStates.StandbyState)
        self.assertEqual(data.summaryState, SummaryStates.StandbyState, "Should be in StandbyState")
        
    def tearDown(self):
        Main.shutdownAction()
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

    def waitUntil(self, action, predicate, timeout = 5):
        startTime = time.time()
        result, data = action()
        while not predicate(data) and (time.time() - startTime) < timeout:
            time.sleep(1)
            result, data = action()
        return data

if __name__ == '__main__':
    unittest.main()