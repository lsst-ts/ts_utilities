
import QTHelpers
from {name}Enumerations import SummaryStates
from DataCache import DataCache
from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QGridLayout)

class OverviewPageWidget(QWidget):
    def __init__(self, {name}):
        QWidget.__init__(self)
        self.{name} = {name}
        self.layout = QVBoxLayout()
        self.dataLayout = QGridLayout()
        self.layout.addLayout(self.dataLayout)
        self.setLayout(self.layout)
        
        row = 0
        col = 0
        self.summaryStateLabel = QLabel("UNKNOWN")
        self.dataLayout.addWidget(QLabel("Summary State"), row, col)
        self.dataLayout.addWidget(self.summaryStateLabel, row, col + 1)

        self.dataEventSummaryState = DataCache()
        
        self.{name}.subscribeEvent_summaryState(self.processEventSummaryState)
        
    def setPageActive(self, active):
        self.pageActive = active
        if self.pageActive:
            self.updatePage()

    def updatePage(self):
        if not self.pageActive:
            return 

        if self.dataEventSummaryState.hasBeenUpdated():
            data = self.dataEventSummaryState.get()
            state = data.summaryState
            summaryStateText = "UNKNOWN"
            if state == SummaryStates.OfflineState:
                summaryStateText = "Offline"
            elif state == SummaryStates.DisabledState:
                summaryStateText = "Disabled"
            elif state == SummaryStates.EnabledState:
                summaryStateText = "Enabled"
            elif state == SummaryStates.FaultState:
                summaryStateText = "Fault"
            self.summaryStateLabel.setText(summaryStates[state])

    def processEventSummaryState(self, data):
        self.dataEventSummaryState.set(data[-1])