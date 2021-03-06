from PyQt5.QtCore import QObject,QFile,pyqtSignal,pyqtSlot,Qt,QSortFilterProxyModel,QTimer
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import *
from PyQt5 import uic
from os import path, getcwd
import qtpy
import qdarkstyle
import sys
import pandas as pd
import datatable as dt
import numpy  as np
import requests
import json

from Application.Views.BuyWindow.buyWindow import Ui_BuyW
from Application.Views.SellWindow.sellWindow import Ui_SellW
from Application.Views.SnapQuote.snapQuote import Ui_snapQ
from Application.Utils.dbConnection import  *
from Application.Utils.configReader import readConfig_All
from Application.Views.Models.tableFP import ModelPosition
from Application.Views.SManager.support import updatePbBGColor_stretegies,updatePbBGColor_filter
from Theme.dt2 import dt1
import logging

from Application.Stretegies.TSpecial import TSpecial

class Manager(QMainWindow):
    # sgTmSubd=pyqtSignal(dict)
    sgTMTM=pyqtSignal(str)
    sgCallPOrderBook = pyqtSignal(str)
    sgCallTB = pyqtSignal(int)

    def __init__(self):
        super(Manager, self).__init__()
        try:


            #####################################################################
            loc1 = getcwd().split('Application')
            ui_login = os.path.join(loc1[0] , 'Resourses','UI','sManager.ui')
            uic.loadUi(ui_login, self)
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)

            self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source,self.MDKey,self.MDSecret,self.IAKey,self.IASecret,self.client_list,DClient,broadcastMode = readConfig_All()
            self.tables_details()

            ########################################################################################################################


            self.lastSelectedStretegy = self.pbStradle
            self.lastSelectedFilter = self.pbFAll

            self.stretegyList = []

            self.pbStradle.clicked.connect(lambda :updatePbBGColor_stretegies(self,'Stradle'))
            self.pbBox.clicked.connect(lambda :updatePbBGColor_stretegies(self,'Box'))
            self.pbPairSell.clicked.connect(lambda :updatePbBGColor_stretegies(self,'PairSell'))
            self.pbPairSellAdv.clicked.connect(lambda :updatePbBGColor_stretegies(self,'PairSellAdv'))
            self.pbTSpecial.clicked.connect(lambda :updatePbBGColor_stretegies(self,'TSpecial'))
            self.pbJodiATM.clicked.connect(lambda :updatePbBGColor_stretegies(self,'JodiATM'))

            self.pbFAll.clicked.connect(lambda :updatePbBGColor_filter(self,'All'))
            self.pbFActive.clicked.connect(lambda :updatePbBGColor_filter(self,'Active'))
            self.pbFStop.clicked.connect(lambda :updatePbBGColor_filter(self,'Stop'))

            ########################################################################################################################
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def changeDayNet(self):
        if(self.rb1.isChecked()):
            self.DayNet = 'DAY'
            self.tableView.setModel(self.smodelFPD)
        elif(self.rb2.isChecked()):
            self.DayNet = 'NET'
            self.tableView.setModel(self.smodelFP)
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

            self.heads = ['SerialNo',
                          'UserID','ClientID','FolioNo','S_type', 'symbol',
                          'MTM','SL','TSL','FutureP','NQty_CE','NQty_PE','Trend'
                          ]
            self.lastSerialNo = 0
            self.table =  np.empty((20000, 25),dtype=object)
            #############################################################################################################
            #############################################
            self.modelFP = ModelPosition(self.table,self.heads)
            self.smodelFP = QSortFilterProxyModel()
            self.smodelFP.setSourceModel(self.modelFP)

            self.smodelFP.setDynamicSortFilter(False)
            self.smodelFP.setFilterKeyColumn(4)
            self.smodelFP.setFilterCaseSensitivity(False)

            self.tableView.setModel(self.smodelFP)


            self.tableView.horizontalHeader().setSectionsMovable(True)
            self.tableView.verticalHeader().setSectionsMovable(True)
            self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
            self.tableView.customContextMenuRequested.connect(self.rightClickMenu)
            self.tableView.setDragDropMode(self.tableView.InternalMove)
            self.tableView.setDragDropOverwriteMode(False)


        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])


    def filtr(self):
        try:
            self.smodelFP.setFilterFixedString(self.listView.selectedIndexes()[0].data())
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])




    def rightClickMenu(self,position):
        try:
            a=(self.tableView.selectedIndexes()[0].data())
            menu = QMenu()
            squareAction = menu.addAction("Square")
            # cancelAction = menu.addAction("Cancel")
            action = menu.exec_(self.tableView.mapToGlobal(position))
            if action == squareAction:
                pass
        except:
            print(sys.exc_info()[1])


    #################################### Ends Here #############################################



    def refresh_config(self):
        try:
            self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source,self.MDKey,self.MDSecret,self.IAKey,self.IASecret,self.client_list,DClient,broadcastMode = readConfig_All()
        except:
            logging.error(sys.exc_info()[1])


    def llp(self,a):
        self.sortOrder = self.smodelFP.sortOrder()
        self.sortColumn =self.smodelFP.sortColumn()

        self.sortOrderD = self.smodelFPD.sortOrder()
        self.sortColumnD =self.smodelFPD.sortColumn()

        self.smodelFP.setFilterKeyColumn(self.sortColumn)
        self.smodelFPD.setFilterKeyColumn(self.sortColumnD)

    def filterData(self,a):
        self.filterStr = a
        self.smodelFP.setFilterFixedString(self.filterStr)
        self.smodelFPD.setFilterFixedString(self.filterStr)

    def clearFilter(self):
        self.filterStr = ''
        self.smodelFPD.setFilterFixedString('')



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Manager()
    form.show()
    sys.exit(app.exec_())
