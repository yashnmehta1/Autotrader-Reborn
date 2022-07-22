import traceback
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Resourses.icons import icons_rc
from os import path, getcwd
import qdarkstyle
from Theme.dt2 import dt1
from Application.Views.titlebar import tBar
import time
from Application.Services.Xts.Api.servicesIA import cancel_order
from Application.Views.Models import tableO
from Application.Utils.configReader import *
from Application.Utils.createTables import tables_details_pob
from Application.Utils.animations import showSnapFrame,hideSnapFrame,showSnapFrame1
from Application.Views.PendingOrder.support import *
from Application.Views.BuyWindow.buyWindow import Ui_BuyW
from Application.Views.SellWindow.sellWindow import Ui_SellW
import json
import requests
import logging
import sys
import numpy as np
import threading

class PendingOrder(QMainWindow):
    ################################# Intialization Here ##################################################
    def __init__(self,parent=None):
        super(PendingOrder, self).__init__()

        loc1 = getcwd().split('Application')
        ui_login = os.path.join (loc1[0] , 'Resourses','UI','pendingOrderBook.ui')
        uic.loadUi(ui_login, self)
        self.setStyleSheet(dt1)



        self.createObjects()

        self.leSearch = QLineEdit()
        self.leSearch.setPlaceholderText('Search')
        self.leSearch.setFixedWidth(150)

        self.pbClear = QPushButton()
        self.pbClear.setText('Clear')

        self.toolBar.addWidget(self.leSearch)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.pbClear)

        self.subToken = 0
        self.isSnapQuotOpen = False
        self.lastSerialNo = 0
        self.filterStr = ''
        self.modifyOIDList =[]
        self.visibleColumns = 23
        self.createShortcuts()
        self.createSlots()


    def pppi(self):
        self.tableView.setColumnHidden(10, True)
    def createObjects(self):
        tables_details_pob(self)

    def createShortcuts(self):
        self.tableView.shortcut_modify = QShortcut(QKeySequence('Shift+F2'), self.tableView)
        self.tableView.shortcut_modify.setContext(Qt.WidgetWithChildrenShortcut)
        self.tableView.shortcut_modify.activated.connect(lambda: ModifyOrder(self))

        self.tableView.slideRifgtSM = QShortcut(QKeySequence('Esc'), self.tableView)
        self.tableView.slideRifgtSM.setContext(Qt.WidgetWithChildrenShortcut)
        self.tableView.slideRifgtSM.activated.connect(lambda: hideSnapFrame(self))

        self.tableView.delt = QShortcut(QKeySequence('Del'), self.tableView)
        self.tableView.delt.setContext(Qt.WidgetWithChildrenShortcut)
        self.tableView.delt.activated.connect(lambda:CancelOrder(self))

        # self.tableView.shortcut_modify = QShortcut(QKeySequence('Shift+F2'), self.tableView)
        # self.tableView.shortcut_modify.setContext(Qt.WidgetWithChildrenShortcut)
        # self.tableView.shortcut_modify.activated.connect(self.ModifyOrder)


    def createSlots(self):
        self.tableView.doubleClicked.connect(lambda:showSnapQ(self))
        self.pbShowSQ.clicked.connect(lambda : showSnapFrame1(self))
        self.pbClear.clicked.connect(lambda: clearFilter(self))
        self.leSearch.textChanged.connect(lambda:filterData(self))



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = PendingOrder()
    form.show()

    sys.exit(app.exec_())