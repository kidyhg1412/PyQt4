# -*- coding: utf-8 -*-
"""
@author: kidyhg1412@sina.com
"""

# Week 5 GUI Main
import sys
from PyQt4 import QtGui, QtCore
import urllib.request
import re

from testweek5_gui_select import ConfigureData

###############################################################################
def main():
    app = QtGui.QApplication(sys.argv)
    stockw = StockWindow()
    stockw.show()
    sys.exit(app.exec_())

###############################################################################
class StockWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.setWindowTitle("Dow Jones Industrial Average(^DJI)")
        self.resize(500, 600)
        self.center()
        
        #----------------------------------------------------------------------
        QuitAction = QtGui.QAction("Exit", self)
        QuitAction.setShortcut("Ctrl+Q")
        QuitAction.setStatusTip("Terminal the program")
        QuitAction.triggered.connect(self.onQuit)

        AboutAction = QtGui.QAction("About", self)
        AboutAction.setShortcut("Ctrl+I")
        AboutAction.setStatusTip("Information about this program")
        AboutAction.triggered.connect(self.onAbout)

        MainMenu = self.menuBar()
        MainMenu.setNativeMenuBar(False)
        FileMenu = MainMenu.addMenu("File")
        FileMenu.addAction(AboutAction)
        FileMenu.addAction(QuitAction)

        #----------------------------------------------------------------------
        sb = QtGui.QStatusBar()
        sb.setFixedHeight(18)
        self.setStatusBar(sb)        
        self.statusBar().showMessage("Ready")
        
        #----------------------------------------------------------------------
        sw = StockWidget()
        self.setCentralWidget(sw)
        self.connect(sw, QtCore.SIGNAL("ReplyQuit"), self.onQuit)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, 
                  (screen.height() - size.height())/2)
        
    def onAbout(self):
        QtGui.QMessageBox.about(self, "Information", "Powered by kidyhg1412@sina.com")
        
    def onQuit(self):
        self.close()
        self.destroy()
        
###############################################################################        
class StockWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        StockCodelabel = QtGui.QLabel("Stock Code: ")
        StockCodetext = QtGui.QLineEdit("AAPL")
        QuitButton = QtGui.QPushButton("Quit")
        QuitButton.setFixedWidth(100)
        RefreshButton = QtGui.QPushButton("Refresh")
        RefreshButton.setFixedWidth(100)

        #----------------------------------------------------------------------
        self.StockTable = QtGui.QTableWidget()
        self.StockTable.setColumnCount(3)
        self.StockTable.setHorizontalHeaderLabels(["Symbol", "Name", "Last Price"])
        self.StockTable.setColumnWidth(0, 120)
        self.StockTable.setColumnWidth(1, 210)
        self.StockTable.setColumnWidth(2, 120)
        
        #----------------------------------------------------------------------
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(StockCodelabel)
        hbox1.addWidget(StockCodetext)
        hbox1.addStretch(1)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(QuitButton)
        hbox2.addWidget(RefreshButton)
        hbox2.addStretch(1)

        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(self.StockTable)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        #----------------------------------------------------------------------
        QuitButton.clicked.connect(self.onQuitButton)
        RefreshButton.clicked.connect(self.onRefreshButton)
        self.StockTable.cellDoubleClicked.connect(self.onCellDoubleClicked)

    def onQuitButton(self):
        reply = QtGui.QMessageBox.question(self, "Message", 
                                           "Are you sure to quit?", 
                                           QtGui.QMessageBox.Yes, 
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.emit(QtCore.SIGNAL("ReplyQuit"))
        else:
            pass

    def onRefreshButton(self):
        success = False
        while(not success):
            try:
                dStr = urllib.request.urlopen('https://hk.finance.yahoo.com/q/cp?s=%5EDJI%27').read()
                getdStr = dStr.decode()
                self.Top30 = re.findall('<tr><td class="yfnc_tabledata1"><b><a href=".*?">(.*?)</a></b></td><td class="yfnc_tabledata1">(.*?)</td>.*?<b>(.*?)</b>.*?</tr>', getdStr)
                success = True
                self.onStockShow()
            except:
                reply = QtGui.QMessageBox.critical(self, "Error", 
                                                   "Unable to download, retry or not?",
                                                   QtGui.QMessageBox.Yes, 
                                                   QtGui.QMessageBox.No)

                if reply == QtGui.QMessageBox.Yes:
                    continue
                else:
                    break

    def onStockShow(self):
        rowNumber = len(self.Top30)
        columnNumber = len(self.Top30[0])
        self.StockTable.setRowCount(rowNumber)
        self.StockTable.setColumnCount(columnNumber)
        self.StockTable.setHorizontalHeaderLabels(["Symbol", "Name", "Last Price"])
        for i in range(rowNumber):
            for j in range(columnNumber):
                StockItem = QtGui.QTableWidgetItem(self.Top30[i][j].replace("&amp;", "&"))
                self.StockTable.setItem(i, j, StockItem)
        self.StockTable.setShowGrid(True)
        self.StockTable.setAlternatingRowColors(True)
        self.StockTable.verticalHeader().setVisible(False)
        self.StockTable.setEditTriggers(QtGui.QTableWidget().NoEditTriggers)
        self.StockTable.setSelectionBehavior(QtGui.QTableWidget().SelectRows)
        self.StockTable.setToolTip("Double click to configure")

    def onCellDoubleClicked(self, celli, cellj):
        code = self.StockTable.item(celli, 0).text()
        self.configureDialog = ConfigureData(code)
        self.configureDialog.show()

###############################################################################
if __name__ == "__main__":
    main()
