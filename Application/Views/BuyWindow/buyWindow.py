import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import sys
import logging
import qdarkstyle
import requests
import time
import traceback
from threading import Thread
from os import path, getcwd

# from Application.configReader import *
from Application.Views.titlebar import tBar
from Theme.dt2 import dt1
from Application.Views.BuyWindow.support import *

class Ui_BuyW(QMainWindow):
    sgTmSubd = pyqtSignal(dict)
    sgTmUnSubd = pyqtSignal(dict)
    sgAppOrderID =  pyqtSignal(int)
    #################################### All Initialization Functions Are Here ################################
    def __init__(self,parent=None):
        super(Ui_BuyW, self).__init__(parent=None)
        try:

            loc1 = getcwd().split('Application')
            ui_login = os.path.join(loc1[0] , 'Resourses','UI','buyWindow.ui')
            uic.loadUi(ui_login, self)
            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
            self.setWindowFlags(flags)
            self.title = tBar('')
            self.headerFrame.layout().addWidget(self.title, 0, 0)
            self.title.setStyleSheet('  border-radius: 4px;')

            ############## Set StyleSheet ######################
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)
            ################### End Section Here ###############
            self.title.sgPoss.connect(self.movWin)
            ####################################################
            self.initVariables()
            self.appOrderIdFprModification = 0


            setAllShortcuts(self)
            self.leMLT.textChanged.connect(lambda:chackMaxMlt(self))



        except:
            print(traceback.print_exc())
    #################################### Ends Here #############################################
    def movWin(self,x,y):
        self.move(self.pos().x()+x,self.pos().y()+y)

    def initVariables(self):
        self.isFresh = True
        self.modifyOIDList = []
        self.leQty.setFocus(True)
        self.mltplr = 1

        self.ticksize = 0.05
        self.lotsize = 0
        self.clist = []


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_BuyW()
    form.show()
    sys.exit(app.exec_())