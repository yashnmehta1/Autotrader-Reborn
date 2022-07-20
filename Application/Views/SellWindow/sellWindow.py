
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Application.Views.titlebar import tBar
from Application.Views.SellWindow.support import *


import qdarkstyle

import traceback
import sys
import logging
import requests
from os import path, getcwd
from threading import Thread
from Theme.dt2 import dt1
#
# from Application.configReader import readConfig_All,config_location



class Ui_SellW(QMainWindow):
    sgTmSubd=pyqtSignal(dict)
    sgTmUnSubd=pyqtSignal(dict)
    sgAppOrderID =  pyqtSignal(int)


    ######################### All Initializers Here ##########################
    def __init__(self,parent=None):
        super(Ui_SellW, self).__init__(parent=None)
        self.ticksize = 0.05
        self.lotsize = 0

        self.clist = []

        try:
            loc11 = getcwd().split('Application')
            ui_login =path.join(loc11[0], 'Resourses','UI','sellWindow.ui')
            uic.loadUi(ui_login, self)
            #

            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
            self.setWindowFlags(flags)


            self.title = tBar('')
            self.headerFrame.layout().addWidget(self.title, 0, 0)
            ############## Set StyleSheet ######################
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)
            ################### End Section Here ###############

            # self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source,market_data_appKey,market_data_secretKey,ia_appKey,ia_secretKey,clist,DClient,broadcastMode = readConfig_All()

            self.slist = ['MANUAL']
            self.isFresh =True
            self.modifyOIDList = []

            self.quitSc = QShortcut(QKeySequence('Esc'), self)
            self.quitSc.activated.connect(self.hide)


            self.Buysc = QShortcut(QKeySequence('F1'), self)
            self.Buysc.activated.connect(self.hide)

            setAllShortcuts(self)
            self.connectAllSlots()

            self.uid = 100000
            self.leQty.setFocus(True)
            self.title.sgPoss.connect(self.movWin)


        except:

            print(traceback.print_exc())
            logging.error(sys.exc_info())
    ####################################### Ends Here ##############################

    ######################################## All Functions Here ########################
    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)

    def connectAllSlots(self):
        self.bt_min.clicked.connect(self.hide)
        self.bt_close.clicked.connect(self.hide)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_SellW()
    form.show()
    sys.exit(app.exec_())