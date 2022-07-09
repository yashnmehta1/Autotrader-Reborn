from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5 import uic
import qdarkstyle
import qtpy
from Resourses.icons import icons_rc
from Theme.dt2 import dt1

from Application.Utils.configReader import readConfig_All,writeURL,refresh
from os import  getcwd,path

import logging
import traceback

import sys
import threading
import numpy as np
import pandas as pd


class Ui_Login(QFrame):
    ################################# Intialization Here ##################################################
    def __init__(self):
        super(Ui_Login, self).__init__()
        try:
            loc1 = getcwd().split('Application')
            ui_login =path.join( loc1[0] , 'Resourses','UI','Login.ui')
            uic.loadUi(ui_login, self)
            ############## Set StyleSheet ######################
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5() #do not comment
            self.setStyleSheet(dt1)
            ################### End Section Here ###############

            ############## labelImage ######################
            bgImg = path.join(loc1[0] , 'Resourses','icons','icons','Untitled2.png')
            self.pixmap = QPixmap(bgImg)
            self.a_logo.setPixmap(self.pixmap)
            ############## End Section Here ######################

            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
            self.setWindowFlags(flags)

            self.MDheaders, self.IAheaders, self.MDtoken, self.IAToken,self.URL,self.userID,self.Source,\
            self.MDKey,self.MDSecret,self.IAKey,self.IASecret, self.clist, self.DClient, self.broadcastMode = readConfig_All()
            ####################################################################


            ####################################################################

            self.populateData()
            self.slotCreation()
            self.pbNext.hide()


            writeURL(self.cbServer.currentText())


        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])


    def setClient(self):
        self.client=self.leClient.text()

    def setDefaultClient(self):
        if(self.cbAPIType.currentText()=='IBT'):
            self.leClient.setEnabled(True)
            self.leClient.setText(self.userID)

        elif(self.cbAPIType.currentText()=='PRO'):
            self.leClient.setEnabled(False)
            self.leClient.setText('*****')
        elif (self.cbAPIType.currentText() == 'TWS-S'):
            self.leClient.setText('')
            self.leClient.setEnabled(True)
        self.client = self.leClient.text()

    def changeConfigs(self):
        writeURL(self.cbServer.currentText())
        # self.MDSocket.refresh_config()

    def slotCreation(self):
        try:
            self.cbServer.currentIndexChanged.connect(self.changeConfigs)
            self.pbSave.clicked.connect(self.saveBaseConfig)
            self.pbSave.clicked.connect(self.revertConfig)
            self.cbAPIType.currentIndexChanged.connect(self.setDefaultClient)
            self.leClient.textChanged.connect(self.setClient)

            self.quitSc = QShortcut(QKeySequence('Esc'), self)
            self.quitSc.activated.connect(sys.exit)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def updateMDstatus(self,a):
        try:
            self.lbMDStatus.setText(a)
        except:
            logging.error(sys.exc_info()[1])

    def updateIAstatus(self,a):
        try:
            self.lbIAStatus.setText(a)
        except:
            logging.error(sys.exc_info()[1])

    def saveBaseConfig(self):
        pass
    def revertConfig(self):
        pass


    def populateData(self):
        self.lb_loginId.setText(self.userID)
        self.lb_ia_appKey.setText(self.IAKey)
        self.lb_md_appKey.setText(self.MDKey)
        self.lb_ia_secretKey.setText(self.IASecret)
        self.lb_md_secretKey.setText(self.MDSecret)
        self.leClient.setText(self.userID)
        self.leUID.setText('HMT_' + self.userID)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_Login()
    form.show()
    sys.exit(app.exec_())