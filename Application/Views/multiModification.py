from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from os import path, getcwd
from Application.Services.Xts.Api.servicesIA import modifyOrder
import qdarkstyle
from Theme.dt2 import dt1
import traceback
# from Resourses.icons import icons_rc
import platform

class Ui_MultiModification(QMainWindow):

    sgFin=pyqtSignal()
    ################################# Intialization Here ##################################################
    def __init__(self):
        super(Ui_MultiModification, self).__init__()

        loc1 = getcwd().split('Application')
        # logDir = loc1[0] + '\\Logs\\%s'%today

        ui_login = path.join(loc1[0], 'Resourses','UI','modifyMultiOrder.ui')
        uic.loadUi(ui_login, self)
        osType = platform.system()
        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)

        self.setWindowFlags(flags)

    def showWindow(self,  modifyArray, instrumentType):
        if (self.isVisible()):
            self.hideWindow()
        orderType = modifyArray[0][4]
        print("orderType multi:", orderType)
        if(orderType == 'StopLimit'):
            self.leModifiedTriggerPrice.setEnabled(True)
        else:
            self.leModifiedTriggerPrice.setEnabled(False)
        self.modifyArray = modifyArray
        self.instrumentType = instrumentType
        self.show()

    def modifyMultipleOrders(self):
        ########### pending
        for i in self.modifyArray:
            modifyOrder(self,i[0],i[7],i[1],i[2],i[3],i[0])

    def hideWindow(self):
        self.modifyArray = []
        self.instrumentType = ''
        self.hide()