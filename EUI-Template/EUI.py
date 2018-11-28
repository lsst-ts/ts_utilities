#!/usr/bin/python3
# -'''- coding: utf-8 -'''-

import sys
import time

from {name}Remote import {name}Remote

from ApplicationControlWidget import ApplicationControlWidget
from ApplicationStatusWidget import ApplicationStatusWidget
from ApplicationPaginationWidget import ApplicationPaginationWidget

from OverviewPageWidget import OverviewPageWidget

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import (QApplication, QVBoxLayout, QDialog, QHBoxLayout)

class EUI(QDialog):
    def __init__(self, {name}, parent=None):
        super(EUI, self).__init__(parent)
        self.{name} = {name}
        self.layout = QVBoxLayout()
        self.topLayerLayout = QHBoxLayout()
        self.applicationControl = ApplicationControlWidget({name})
        self.topLayerLayout.addWidget(self.applicationControl)
        self.applicationStatus = ApplicationStatusWidget({name})
        self.topLayerLayout.addWidget(self.applicationStatus)
        self.middleLayerLayout = QHBoxLayout()
        self.applicationPagination = ApplicationPaginationWidget({name})
        self.applicationPagination.addPage("Overview", OverviewPageWidget({name}))
        self.middleLayerLayout.addWidget(self.applicationPagination)
        self.bottomLayerLayout = QHBoxLayout()
        self.layout.addLayout(self.topLayerLayout)
        self.layout.addLayout(self.middleLayerLayout)
        self.layout.addLayout(self.bottomLayerLayout)
        self.setLayout(self.layout)

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create EUI
    {name} = {name}Remote()
    eui = EUI({name})
    eui.show()
    # Create {name} Telemetry & Event Loop
    telemetryEventLoopTimer = QTimer()
    telemetryEventLoopTimer.timeout.connect({name}.runSubscriberChecks)
    telemetryEventLoopTimer.start(500)
    # Run the main Qt loop
    app.exec_()
    # Clean up {name} Telemetry & Event Loop
    telemetryEventLoopTimer.stop()
    # Close application
    sys.exit()