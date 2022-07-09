from PyQt5.QtCore import QObject,QFile,pyqtSignal,pyqtSlot,Qt,QSortFilterProxyModel,QTimer
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from os import path, getcwd

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
        self.pbCsv.clicked.connect(self.create_trade_csv)
        self.bt_min.clicked.connect(self.hide)
        self.bt_close.clicked.connect(self.hide)
        # self.pbGetTrade.clicked.connect(self.get_Trades)
        self.tableView.horizontalHeader().sectionClicked.connect(self.getSortClues)
        self.leSearch.textChanged.connect(self.changeFilter)

    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.hide)

    def changeFilter(self,a):
        self.smodelT.setFilterFixedString(a)

    def getSortClues(self,a):
        self.sortOrder = self.smodelT.sortOrder()
        self.sortColumn =self.smodelT.sortColumn()

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)

    def filtr(self):
        try:
            self.smodelT.setFilterFixedString(self.listView.selectedIndexes()[0].data())
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())


    def create_trade_csv(self):
        try:
            name = QFileDialog.getSaveFileName(self, 'Save File')
            np.savetxt(name[0], self.ApiTrade, delimiter=',')
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())


    def get_csv(self):
        np.savetxt(self.csvPath,self.ApiTrade,delimiter=',')
        # self.ApiTrade.tofile("foo.csv", sep=",")



    def get_Trades(self):
        try:
            url = self.URL + '/interactive/orders/trades'
            req = requests.request("GET", url, headers=self.IAheaders)
            data_p = req.json()

            if(data_p['result'] != []):
                for j,i in enumerate(data_p['result']):
                    try:
                        if (int(i['ExchangeInstrumentID']) in self.cntrcts.keys()):
                            ins = self.cntrcts[(i['ExchangeInstrumentID'])]
                        else:
                            fltr = np.asarray([i['ExchangeInstrumentID']])
                            ah = self.Contract_df[np.in1d(self.Contract_df[:, 2], fltr)][0]
                            ins = [ah[4],ah[3],ah[6],ah[7],ah[8],ah[11],ah[14],ah[9],ah[0],ah[5]]
                            self.cntrcts[int(i['ExchangeInstrumentID'])] = ins
                    except:
                        logging.error(sys.exc_info()[1])
                        print(traceback.print_exc())
                        # ins = ['', '', '', '', '']


                    if(j==0):
                        ApiTrade= np.array([[i['ClientID'], i['ExchangeInstrumentID'], ins[0],
                                             ins[1],ins[2], ins[3], ins[4],i['OrderSide'].replace('BUY','Buy').replace('SELL','Sell'),
                                             i['AppOrderID'],i['OrderType'], i['LastTradedQuantity'], i['OrderStatus'],
                                             i['OrderAverageTradedPrice'],i['ExchangeTransactTime'], i['OrderUniqueIdentifier'],
                                             i['ExchangeOrderID']],[i['LastTradedPrice']]])
                    else:
                        trades= np.array([[i['ClientID'], i['ExchangeInstrumentID'], ins[0],
                                           ins[1],ins[2], ins[3], ins[4],i['OrderSide'].replace('BUY','Buy').replace('SELL','Sell'),
                                           i['AppOrderID'],i['OrderType'], i['LastTradedQuantity'], i['OrderStatus'],
                                           i['OrderAverageTradedPrice'],i['ExchangeTransactTime'], i['OrderUniqueIdentifier'],
                                           i['ExchangeOrderID']],[i['LastTradedPrice']]])
                        ApiTrade = np.vstack([ApiTrade, trades])
            else:
                ApiTrade =np.empty((0,16))

            self.modelT = ModelTB(ApiTrade, self.heads)
            # self.TradeW.smodelT = QSortFilterProxyModel()
            self.smodelT.setSourceModel(self.modelT)
            self.tableView.setModel(self.smodelT)

        except:
            print(traceback.print_exc())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = TradeBook()
    form.show()
    sys.exit(app.exec_())
