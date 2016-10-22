# -*- coding: utf-8 -*-
"""
@author: kidyhg1412@sina.com
"""

# Week 5 GUI Select
from PyQt4 import QtGui, QtCore

from testweek5_gui_plot import PlotData

###############################################################################
class ConfigureDialog(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.setWindowTitle("Configure Data")
        self.resize(350, 200)
        
        #----------------------------------------------------------------------
        DataRange = QtGui.QLabel("Data Range")
        
        StartDate = QtGui.QLabel("Start Date")
        self.StartDateSelected = QtGui.QDateEdit(QtCore.QDate(2015, 10, 1))
        self.StartDateSelected.setDisplayFormat("yyyy-MM-dd")
        self.StartDateSelected.setCalendarPopup(True)
        
        EndDate = QtGui.QLabel("End Date")
        self.EndDateSelected = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.EndDateSelected.setDisplayFormat("yyyy-MM-dd")
        self.EndDateSelected.setCalendarPopup(True)
        self.EndDateSelected.setMaximumDate(QtCore.QDate.currentDate())

        DataSet = QtGui.QLabel("Data Set")
        
        self.DataOpen = QtGui.QCheckBox("open")
        self.DataClose = QtGui.QCheckBox("close")
        self.DataHigh = QtGui.QCheckBox("high")
        self.DataLow = QtGui.QCheckBox("low")
        self.DataVolume = QtGui.QCheckBox("volume")

        OkButton = QtGui.QPushButton("Ok")
        OkButton.setFixedWidth(100)
        OkButton.setToolTip("Press ok to plot")
        CloseButton = QtGui.QPushButton("Close")
        CloseButton.setFixedWidth(100)

        #----------------------------------------------------------------------
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(DataRange)
        hbox1.addWidget(DataSet)

        vbox1 = QtGui.QVBoxLayout()
        vbox1.addWidget(StartDate)
        vbox1.addWidget(self.StartDateSelected)
        vbox1.addWidget(EndDate)
        vbox1.addWidget(self.EndDateSelected)

        vbox2 = QtGui.QVBoxLayout()
        vbox2.addWidget(self.DataOpen)
        vbox2.addWidget(self.DataClose)
        vbox2.addWidget(self.DataHigh)
        vbox2.addWidget(self.DataLow)
        vbox2.addWidget(self.DataVolume)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addLayout(vbox1)
        hbox2.addLayout(vbox2)

        hbox3 = QtGui.QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(OkButton)
        hbox3.addWidget(CloseButton)
        hbox3.addStretch(1)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)

        #----------------------------------------------------------------------
        OkButton.clicked.connect(self.onOkButton)
        CloseButton.clicked.connect(self.onCloseButton)

    def onTransferCode(self, code):
        self.plotcode = code

    def onOkButton(self):
        start = self.StartDateSelected.date()
        start = start.toPyDate()
        end = self.EndDateSelected.date()
        end = end.toPyDate()

        drawlist = []
        if self.DataOpen.checkState():
            drawlist.append("open")
        if self.DataClose.checkState():
            drawlist.append("close")
        if self.DataHigh.checkState():
            drawlist.append("high")
        if self.DataLow.checkState():
            drawlist.append("low")
        if self.DataVolume.checkState():
            drawlist.append("volume")

        if drawlist:
            PlotData(self.plotcode, start, end, drawlist)
        else:
            QtGui.QMessageBox.information(self, "Waring", "Please select the data set")

    def onCloseButton(self):
        self.close()
        self.destroy()

###############################################################################
def ConfigureData(code):
    condialog = ConfigureDialog()
    condialog.onTransferCode(code)
    return condialog
