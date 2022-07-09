import sys
import traceback
from os import path, getcwd
import logging

import requests
import json

from PyQt5.QtCore import QObject,QFile,pyqtSignal,pyqtSlot,Qt,QSortFilterProxyModel,QTimer
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import *
from PyQt5 import uic

import qtpy
import qdarkstyle


import pandas as pd
import datatable as dt
import numpy  as np

from Application.Utils.configReader import readConfig_All,refresh
from Application.Views.Models.tableNP import ModelPosition

from Theme.dt2 import dt1




class ProxyModel (QSortFilterProxyModel): #Custom Proxy Model
    def __init__(self):
        super(ProxyModel,self).__init__()
        self.onlyPoss = False

    def filterAcceptsRow(self, row, parent):
        if(self.onlyPoss == True):
            if(self.sourceModel().index(row, 7, parent).data() != 0 ):
                return True
            else:
                return False
        else:
            return True

class NetPosition(QMainWindow):
    # sgTmSubd=pyqtSignal(dict)
    sgTMTM=pyqtSignal(str)
    sgCallPOrderBook = pyqtSignal(str)
    sgCallTB = pyqtSignal(int)

    def __init__(self):
        super(NetPosition, self).__init__()
        try:

            self.onlyPoss = False
            self.filterStr = ''
            self.DayNet = 'NET'
            refresh(self)
            #####################################################################

            loc1 = getcwd().split('Application')
            ui_login = path.join(loc1[0] , 'Resourses','UI','netPosition.ui')
            uic.loadUi(ui_login, self)

            self.lastSerialNo = 0
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)


            self.tables_details()
            self.tableView.horizontalHeader().sectionMoved.connect(print)

            # self.CreateToolBar()

            ########################################################################################################################
            # self.tableView.shortcut_buy = QShortcut(QKeySequence('F1'), self.tableView)
            # self.tableView.shortcut_buy.setContext(Qt.WidgetWithChildrenShortcut)
            # self.tableView.shortcut_buy.activated.connect(self.showBuy)
            #
            # self.tableView.shortcut_sell = QShortcut(QKeySequence('F2'), self.tableView)
            # self.tableView.shortcut_sell.setContext(Qt.WidgetWithChildrenShortcut)
            # self.tableView.shortcut_sell.activated.connect(self.showSell)
            #
            # self.tableView.shortcut_buy1 = QShortcut(QKeySequence('+'), self.tableView)
            # self.tableView.shortcut_buy1.setContext(Qt.WidgetWithChildrenShortcut)
            # self.tableView.shortcut_buy1.activated.connect(self.showBuy)
            #
            # self.tableView.shortcut_sell1 = QShortcut(QKeySequence('-'), self.tableView)
            # self.tableView.shortcut_sell1.setContext(Qt.WidgetWithChildrenShortcut)
            # self.tableView.shortcut_sell1.activated.connect(self.showSell)
            #
            # self.tableView.call_pending_ob = QShortcut(QKeySequence('F3'), self.tableView)
            # self.tableView.call_pending_ob.setContext(Qt.WidgetWithChildrenShortcut)
            # self.tableView.call_pending_ob.activated.connect(self.orderRaise)
            #
            # self.tableView.call_TB = QShortcut(QKeySequence('F8'), self.tableView)
            # self.tableView.call_TB.setContext(Qt.WidgetWithChildrenShortcut)
            # self.tableView.call_TB.activated.connect(self.showTB)
            #
            #
            # self.tableView.shortcut_snapQuote = QShortcut(QKeySequence('F5'), self.tableView)
            # self.tableView.shortcut_snapQuote.setContext(Qt.WidgetWithChildrenShortcut)
            # self.tableView.shortcut_snapQuote.activated.connect(self.snapQuoteRequested)
            #
            # # self.rb1.toggled.connect(self.changeDayNet)
            #
            # # self.tableView.horizontalHeader().sectionClicked.connect(self.llp)

            ########################################################################################################################
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def changeDayNet(self):
        if(self.rb1.isChecked()):
            self.DayNet = 'DAY'
            self.tableView.setModel(self.smodelPD)

        elif(self.rb2.isChecked()):
            self.DayNet = 'NET'

            self.tableView.setModel(self.smodelP)
            self.rcount = self.Apipos.shape[0]

    def orderRaise(self):
        token = int(self.tableView.selectedIndexes()[3].data())
        self.sgCallPOrderBook.emit(str(token))


    def showTB(self):
        token = int(self.tableView.selectedIndexes()[3].data())
        self.sgCallTB.emit(token)



    def tables_details(self):
        try:
            #############################################################################################################

            self.heads = ['UserID',
                          'ClientID','Segment','ExchangeInstrumentID', 'TradingSymbol', 'symbol',
                          'Expiry','Stike_price','C/P','Quantity', 'MTM',
                          'LTP', 'RealizedMTM','NetAmount','AvgPrice','lotsize',
                          'maxQ','AssetToken','SerialNo','OpenQty','OpenAmt']

            self.Apipos =  np.empty((1000, 19),dtype=object)
            self.sectionDict={}
            for j,i in enumerate(self.heads):
                self.sectionDict[j]=i
            #############################################################################################################

            #############################################
            self.modelP = ModelPosition(self.Apipos,self.heads)
            self.smodelP = ProxyModel()
            self.smodelP.setSourceModel(self.modelP)

            self.smodelP.setDynamicSortFilter(False)
            self.smodelP.setFilterKeyColumn(4)
            self.smodelP.setFilterCaseSensitivity(False)

            self.tableView.setModel(self.smodelP)


            self.tableView.horizontalHeader().setSectionsMovable(True)
            self.tableView.verticalHeader().setSectionsMovable(True)
            self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
            self.tableView.customContextMenuRequested.connect(self.rightClickMenu)
            # self.tableView.setStyleSheet(
            #     'background-color: rgb(50, 50, 50);selection-background-color: transparent;color: rgb(245, 245, 245);')
            self.tableView.setDragDropMode(self.tableView.InternalMove)
            # self.tableView.horizontalHeader().setStyleSheet('color : black')
            self.tableView.setDragDropOverwriteMode(False)
            # a=QtWidgets.QtableView.horizontalHeader()
            # a.moveSection()
            self.tableView.setColumnWidth(0,0)
            self.tableView.setColumnWidth(2,0)
            self.tableView.setColumnWidth(3,0)
            self.tableView.setColumnWidth(14,0)
            self.tableView.setColumnWidth(15,0)
            self.tableView.setColumnWidth(16,0)

            # self.tableView.clicked.connect(self.tvs6)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])


    def filtr(self):
        try:
            self.smodelP.setFilterFixedString(self.listView.selectedIndexes()[0].data())
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])



    def CreateToolBar(self):
        try:
            self.pbSquare = QPushButton('SquareAll')
            # self.pbSquare.clicked.connect(self.squareAll)
            self.toolBar.addWidget(self.pbSquare)
            self.toolBar.addSeparator()

            self.rb1 =QRadioButton('DAY')
            self.rb2 = QRadioButton('NET')
            self.cbFolio = QComboBox()
            self.cbFolio.setMinimumWidth(150)

            self.cbSymbol = QComboBox()
            self.cbSymbol.setMinimumWidth(150)
            self.cbExp = QComboBox()
            self.cbExp.setMinimumWidth(100)
            self.cbStrike = QComboBox()
            self.cbStrike.setMinimumWidth(100)
            self.cbOtype = QComboBox()
            # self.cbOtype.setMinimumWidth(100)

            self.leSearch = QLineEdit()
            self.leSearch.setPlaceholderText('Search')
            self.leSearch.textChanged.connect(self.filterData)

            self.pbClear = QPushButton('Clear')
            self.pbClear.clicked.connect(self.clearFilter)


            self.opencheckbox = QCheckBox('OnlyOpen')
            self.toolBar.addWidget(self.rb1)

            self.toolBar.addSeparator()

            self.toolBar.addWidget(self.rb2)

            self.toolBar.addWidget(self.opencheckbox)
            self.opencheckbox.stateChanged.connect(self.setOnlyPosFlag)
            self.toolBar.addSeparator()
            self.toolBar.addWidget(self.leSearch)

            self.pbGetPos = QPushButton('GET POS')
            self.toolBar.addSeparator()
            self.toolBar.addWidget(self.pbGetPos)
            # self.pbGetPos.clicked.connect(print)

        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def setOnlyPosFlag(self):
        try:
            print('in setOnlyPosFlag ')
            self.onlyPoss = self.opencheckbox.isChecked()
            self.smodelP.onlyPoss = self.onlyPoss
            self.smodelP.setFilterFixedString('')
        except:
            print(traceback.print_exc())



    def rightClickMenu(self,position):
        try:
            a=(self.tableView.selectedIndexes()[0].data())
            menu = QMenu()
            squareAction = menu.addAction("Square")
            # cancelAction = menu.addAction("Cancel")
            action = menu.exec_(self.tableView.mapToGlobal(position))
            if action == squareAction:
                abc=self.tableView.selectedIndexes()
                noOfcolumnsinNetPoss = self.Apipos.shape[1]

                lent=int((len(abc))/noOfcolumnsinNetPoss)
                print('lent',lent)
                for i in range(lent):

                    token = abc[1 + (noOfcolumnsinNetPoss*i)].data()
                    qty = int(abc[7 + (noOfcolumnsinNetPoss*i)].data())
                    Maxqty = int(abc[13 + (noOfcolumnsinNetPoss*i)].data())

                    print(token,qty)

                    if(qty>0):
                        absQty = abs(qty)

                        orderSide = 'SELL'
                        while absQty > Maxqty :

                            self.PlaceOrder(token,orderSide,Maxqty,0)
                            absQty = absQty - Maxqty
                        self.PlaceOrder(token, orderSide, absQty, 0)

                    elif(qty<0):
                        absQty = abs(qty)
                        orderSide = 'BUY'
                        while absQty > Maxqty :
                            self.PlaceOrder(token,orderSide,Maxqty,0)
                            absQty = absQty - Maxqty
                        self.PlaceOrder(token, orderSide, absQty, 0)

        except:
            print(sys.exc_info()[1])


    #################################### Ends Here #############################################

    def filterData(self,a):
        self.filterStr = a
        self.smodelP.setFilterFixedString(self.filterStr)
        self.smodelPD.setFilterFixedString(self.filterStr)

    def clearFilter(self):
        self.filterStr = ''
        self.smodelPD.setFilterFixedString('')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = NetPosition()
    form.show()
    sys.exit(app.exec_())
