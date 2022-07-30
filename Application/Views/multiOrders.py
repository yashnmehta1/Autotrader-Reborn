from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from os import path, getcwd
import numpy as np
from Application.Services.Xts.Api.servicesIA import modifyOrder
import qdarkstyle
from Theme.dt2 import dt1
import traceback
# from Resourses.icons import icons_rc
import platform
import datatable as dt

class Ui_MultiOrders(QWidget):

    sgFin=pyqtSignal()
    ################################# Intialization Here ##################################################
    def __init__(self):
        super(Ui_MultiOrders, self).__init__()

        loc1 = getcwd().split('Application')
        # logDir = loc1[0] + '\\Logs\\%s'%today

        ui_login = path.join(loc1[0], 'Resourses','UI','multiOrder.ui')
        uic.loadUi(ui_login, self)
        osType = platform.system()
        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)

        self.setWindowFlags(flags)
        self.connectSlot();

        self.createShortcuts()

    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.hide)

    def showWindow(self,noOfSelectedRecord, indexes ):
        if (self.isVisible()):
            self.hideWindow()

        statingPoint = 0
        print("len indexes : ", len(indexes))
        print("************************* ")
        multiOrdersArray = np.zeros((0, 5), dtype=object)
        for i in range(noOfSelectedRecord):

           array1 = dt.Frame([[AppOrderId],
                               [clientId], [token], [orderSide], [orderType], [productType],
                               [validity], [exchange], [price], [triggerPrice], [qty],
                               [uid]]).to_numpy()

            multiOrdersArray = np.vstack([modifyArray, array1])
            print("modifyArray:")
            print("+++++++++++++++++++++++++++++++++:")
            print(modifyArray)
            statingPoint += self.PendingW.visibleColumns


        self.show()

    def multipleOrders(self):
        ########### pending
        for i in self.modifyArray:
            print("Multi order exec : ")
            modifiedPrice = self.leModifiedPrice.text()
            #modifyOrder(self,i[0],i[7],i[1],i[2],i[3],i[10],modifiedPrice,0,i[9],i[11],i[4],i[5],i[6])

    def connectSlot(self):
        pass
        #print("btn::",self.btn_submit )
      #  self.btn_submit.clicked.connect(self.multipleOrders)

    def hideWindow(self):
        self.hide()

    def getClientId(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 1]
        print('getClientId', value)
        return value[0]

    def getFolioNo(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        folioNo = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 15]
        print('getFolioNo', folioNo)
        return folioNo[0]

    def getOrderSide(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 8]
        print('getOrderSide', value)
        return value[0]

    def getExchange(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 19]
        print('getExchange', value)
        return value[0]

    def getPrice(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 13]
        print('getPrice', value)
        return value[0]

    def getToken(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 2]
        print('getToken', value)
        return value[0]

    def getOrderType(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 9]
        print('getOrderType', value)
        return value[0]

    def getValidity(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 24]
        print('getValidity', value)
        return value[0]

    def getProductType(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 23]
        print('getProductType', value)
        return value[0]

    def getTriggerPrice(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 14]
        print('getTriggerPrice', value)
        return '%.2f' % value[0]

    def getQty(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 12]
        print('getQty', value)
        return value[0]

    def getOUID(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 15]
        print('getQty', value)
        return value[0]

    def getLimitPrice(self, AppOrderId):
        fltr = np.asarray([AppOrderId])
        value = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr), 13]
        print('getLimitPrice', value)
        return value[0]
