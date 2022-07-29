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

from Application.Utils.createTables import tables_details_np
import pandas as pd
import datatable as dt
import numpy  as np

from Application.Utils.configReader import readConfig_All,refresh
from Application.Views.Models.tableNP import ModelPosition

from Theme.dt2 import dt1

from .support import *


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

            tables_details_np(self)
            # self.tables_details()
            self.tableView.horizontalHeader().sectionMoved.connect(print)
            self.tableView.customContextMenuRequested.connect(lambda:rightClickMenu(self))
            createShortcuts(self)
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



    #################################### Ends Here #############################################


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = NetPosition()
    form.show()
    sys.exit(app.exec_())
