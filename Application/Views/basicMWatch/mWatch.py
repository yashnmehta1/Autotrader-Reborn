import logging
import sys
import traceback

from os import path, getcwd
import threading
import time
import requests
import json



from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import qdarkstyle
import qtpy

# import numpy as np
# import datatable as dt
# import pandas as pd

# import dill
# import pickle



from Application.Utils.configReader import *
from Theme.dt2 import  dt1


class MarketW_basic(QMainWindow):
    # sgTmSubd=pyqtSignal(dict)
    sgSnapQuote=pyqtSignal(int,int,int)
    sgShowPending= pyqtSignal(str)
    def __init__(self):
        super(MarketW_basic, self).__init__()
        self.setObjectName('MarketWatch')

        #####################################################################
        try:
            loc1 = getcwd().split('Application')
            ui_login = os.path.join(loc1[0] , 'Resourses','UI','MW.ui')
            uic.loadUi(ui_login, self)

            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)
            self.setCentralWidget(self.tableView)

            self.lastSerialNo = 0
            self.onlyPoss =False

            ########################################################################################################################
            # self.tableView.horizontalHeader().sectionClicked.connect(self.llp)
            self.createToolBar()

        except:
            print(traceback.print_exc(),'mwatch')
            logging.error(sys.exc_info()[1])
        ########################################################################################################################

    def createToolBar(self):
        self.leSearch = QLineEdit()
        self.leSearch.setPlaceholderText('Search')
        self.leSearch.setFixedWidth(150)
        self.leSearch.textChanged.connect(self.filterData)

        self.pbClear = QPushButton()
        self.pbClear.setText('Clear')

        self.toolBar.addWidget(self.leSearch)
        self.toolBar.addSeparator()
        self.cxbMore = QCheckBox('More')
        self.toolBar.addWidget(self.pbClear)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.cxbMore)
        self.pbClear.clicked.connect(self.clearFilter)

    def clearFilter(self):
        self.leSearch.setText('')
        self.smodel.setFilterKeyColumn(3)

    def filterData(self):
        self.smodel.setFilterFixedString(self.leSearch.text())





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = MarketW_basic()
    form.show()
    sys.exit(app.exec_())






comment="""
contract master cd 
contract master in database




# # print(a['Token'])
# arrrr=np.where(self.table2 == a['Token'])[0][0]
# print(arrrr)
# for i in range(self.NOC):
#     ind = self.model.index(arrrr, i)
#     self.model.data(index=ind,role=0)
#     self.model.data(index=ind,role=7)
#     self.model.data(index=ind,role=8)

"""