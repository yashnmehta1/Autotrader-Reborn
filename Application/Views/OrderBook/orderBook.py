import time
import traceback
import sys
from os import path, getcwd
from PyQt5.QtCore import QObject,QFile,pyqtSignal,pyqtSlot,Qt,QSortFilterProxyModel,QTimer
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import qdarkstyle
import qtpy

import logging
import pandas as pd
import datatable as dt
import requests
import numpy as np
from Application.Utils.dbConnection import  *
from Application.Utils.configReader import readConfig_All
from Application.Views.Models.tableOrder import ModelOB
from Theme.dt2 import dt1
import logging
from Application.Views.titlebar import tBar
from Application.Utils.createTables import tables_details_ob



class OrderBook(QMainWindow):
    # sgTmSubd=pyqtSignal(dict)

    def __init__(self,parent=None):
        try:
            super(OrderBook, self).__init__(parent=None)

            self.rcount = 0
            self.lastSerialNo = 0
            self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source,self.MDKey,self.MDSecret,self.IAKey,self.IASecret,self.client_list,DClient,broadcastMode = readConfig_All()
            #####################################################################

            loc1 = getcwd().split('Application')
            ui_login = os.path.join(loc1[0] ,'Resourses','UI','orderBook.ui')
            uic.loadUi(ui_login, self)

            flags = Qt.WindowFlags( Qt.FramelessWindowHint)
            self.setWindowFlags(flags)


            self.title = tBar('OrderBook')
            self.headerFrame.layout().addWidget(self.title, 0, 0)
            self.title.sgPoss.connect(self.movWin)
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)
            tables_details_ob(self)
            self.actionCSV.triggered.connect(self.create_trade_csv)
            self.leSearch = QLineEdit()
            self.leSearch.setPlaceholderText('Search')
            self.leSearch.setFixedWidth(150)
            self.createShortcuts()
            self.connectAllSlots()
            QSizeGrip(self.frameGrip)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())

    def connectAllSlots(self):
        self.bt_close.clicked.connect(self.hide)
        self.bt_min.clicked.connect(self.hide)

    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.hide)

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)

    def filtr(self):
        try:
            self.smodelT.setFilterFixedString(self.listView.selectedIndexes()[0].data())
            # print(self.listView.selectedIndexes()[0].data())
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())

    def updateGetApi(self,data):
        try:
            self.ApiOrder = data
            self.modelO = ModelOB(self.ApiOrder,self.heads)
            self.smodelO.setSourceModel(self.modelO)
            self.tableView.setModel(self.smodelO)
            self.rcount = self.ApiOrder.shape[0]

        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())



    def refresh_config(self):
        try:
            self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source ,self.MDKey,self.MDSecret,self.IAKey,self.IASecret,self.client_list,DClient,broadcastMode= readConfig_All()
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())

    def create_trade_csv(self):
        try:
            name = QFileDialog.getSaveFileName(self, 'Save File')
            self.ApiTrade.to_csv(name[0])
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = OrderBook()
    form.show()
    sys.exit(app.exec_())
