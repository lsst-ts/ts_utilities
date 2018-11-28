
from {name}Enumerations import SummaryStates, DetailedStates
from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout

class ApplicationStatusWidget(QWidget):
    def __init__(self, {name}):
        QWidget.__init__(self)
        self.{name} = {name}
        self.layout = QVBoxLayout()
        self.statusLayout = QGridLayout()
        self.layout.addLayout(self.statusLayout)
        self.setLayout(self.layout)

        self.summaryStateLabel = QLabel("Offline")

        row = 0
        col = 0
        self.statusLayout.addWidget(QLabel("State"), row, col)
        self.statusLayout.addWidget(self.summaryStateLabel, row, col + 1)
        
        self.{name}.subscribeEvent_summaryState(self.processEventSummaryState)

    def processEventSummaryState(self, data):
        summaryState = data[-1].summaryState
        summaryStateText = "Unknown"
        if summaryState == SummaryStates.DisabledState:
            summaryStateText = "Disabled"
        elif summaryState == SummaryStates.EnabledState:
            summaryStateText = "Enabled"
        elif summaryState == SummaryStates.FaultState:
            summaryStateText = "Fault"
        elif summaryState == SummaryStates.OfflineState:
            summaryStateText = "Offline"
        elif summaryState == SummaryStates.StandbyState:
            summaryStateText = "Standby"

        self.summaryStateLabel.setText(summaryStateText)