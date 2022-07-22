from PyQt5.QtCore import QObject,QFile,pyqtSignal,pyqtSlot,Qt,QSortFilterProxyModel,QTimer
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from os import path, getcwd
from .support import *
import qtpy
import qdarkstyle

from Application.Utils.configReader import readConfig_All,refresh
from Application.Views.Models.tableTB import ModelTB
from Theme.dt2 import dt1
from Application.Views.titlebar import tBar
# from ENTRY.buyWindow import Ui_BuyW
# from ENTRY.sellWindow import Ui_SellW

import traceback
import logging
import time
import sys
import pandas as pd
import datatable as dt
import numpy as np
import requests
import platform
from Application.Utils.createTables import tables_details_tb
from Application.Utils.updation import updateGetTradeApi

class TradeBook(QMainWindow):
    def __init__(self,parent=None):
        try:

            super(TradeBook, self).__init__(parent=None)
            self.list1 = []
            self.rcount = 0
            self.sortColumn = 0
            self.sortOrder = 0

            refresh(self)

            loc1 = getcwd().split('Application')
            ui_login = path.join(loc1[0] , 'Resourses','UI','Tradebook.ui')
            uic.loadUi(ui_login, self)

            self.csvPath = path.join(loc1[0], 'Resourses','Trades.txt')

            osType = platform.system()
            if(osType=='Darwin'):
                flags = Qt.WindowFlags( Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            else:
                flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint )
            self.setWindowFlags(flags)
            self.title = tBar('TradeBook')
            self.headerFrame.layout().addWidget(self.title, 0, 0)
            self.title.sgPoss.connect(self.movWin)
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()

            self.setStyleSheet(dt1)
            tables_details_tb(self)

            self.createShortcuts()
            self.connectAllSlots()
            QSizeGrip(self.frameGrip)

        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())

    def connectAllSlots(self):
        self.pbCsv.clicked.connect(lambda:create_trade_csv(self))
        self.bt_min.clicked.connect(self.hide)
        self.bt_close.clicked.connect(self.hide)
        # self.pbGetTrade.clicked.connect(self.get_Trades)
        # self.tableView.horizontalHeader().sectionClicked.connect(self.getSortClues)
        self.leSearch.textChanged.connect(lambda:changeFilter(self))

    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.hide)


    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = TradeBook()
    form.show()
    sys.exit(app.exec_())
