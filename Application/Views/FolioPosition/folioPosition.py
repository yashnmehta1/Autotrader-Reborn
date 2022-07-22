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
from Application.Utils.createTables import tables_details_fp
from Theme.dt2 import dt1
import logging

from .support import *

#

class FolioPosition(QMainWindow):
    # sgTmSubd=pyqtSignal(dict)
    sgTMTM=pyqtSignal(str)
    sgCallPOrderBook = pyqtSignal(str)
    sgCallTB = pyqtSignal(int)

    def __init__(self):
        super(FolioPosition, self).__init__()
        try:

            self.filterStr = ''
            self.clientFolios = {}
            self.folioList = ['MANUAL']

            self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source,self.MDKey,self.MDSecret,self.IAKey,self.IASecret,self.client_list,DClient,broadcastMode = readConfig_All()
            #####################################################################

            loc1 = getcwd().split('Application')
            ui_login = os.path.join(loc1[0] , 'Resourses','UI','folioPosition.ui')
            uic.loadUi(ui_login, self)
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)
            #####################################################################
            tables_details_fp(self)
            self.tableView.customContextMenuRequested.connect(lambda:rightClickMenu(self))
            self.pbShow.clicked.connect(lambda:filterData(self))
            self.cbClient.currentIndexChanged.connect(lambda: cbClientChange(self))

        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])


    #################################### Ends Here #############################################


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = FolioPosition()
    form.show()
    sys.exit(app.exec_())
