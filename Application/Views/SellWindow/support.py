from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
import traceback
import logging
import time

from Application.Services.Xts.Api.servicesIA import PlaceOrder

import sys


from threading import Thread



def showWindow(self, exchange ,token, price, qty, symbol, instrument, exp, strk, opt, freezeQty ,lotSize ,tickSize):
    try:

        self.leToken.setText(str(token))
        self.leInsType.setText(instrument)
        self.leSymbol.setText(symbol)
        self.cbExp.clear()
        self.cbExp.addItem(exp)
        self.cbStrike.clear()
        self.cbStrike.addItem(strk)
        self.cbOpt.clear()
        self.cbOpt.addItem(opt)
        self.leMLT.setText('1')

        self.leQty.setText(str(lotSize))
        self.leRate.setText(price)



        self.lotsize =lotSize
        self.ticksize =tickSize
        self.freezeQty = freezeQty

        self.show()
    except:
        print(traceback.print_exc())

def placeOrd(self):
    try:
        sellW = self.sellW
        if(sellW.leToken.text() != ''):
            clientID = sellW.leClient.text()
            exchange = sellW.cbEx.currentText()
            token = int(sellW.leToken.text())
            uid = sellW.cbStretegyNo.currentText()
            limitPrice = float(sellW.leRate.text())
            disQty = int(sellW.leDiscQ.text())
            qty = int(sellW.leQty.text())
            triggerPrice = float(sellW.leTrigger.text())

            ##############################################################################################
            productType = sellW.cbProduct.currentText()
            orderSide = 'SELL'
            if(limitPrice==0):
                orderType = 'MARKET'
            else:
                orderType = getOrderType(sellW)

            validity = sellW.cbValidity.currentText()
            if(sellW.isFresh):
                sellW.mltplr = int(sellW.leMLT.text())
                for i in range(sellW.mltplr):
                    th1 = Thread(target=PlaceOrder,args=(self,
                                     exchange, clientID, token, orderSide,  qty,
                                    limitPrice,  validity, disQty,triggerPrice,uid,
                                     orderType,productType))
                    th1.start()
            # else:
            #     if(len(sellW.modifyOIDList)>1):
            #         print(len(sellW.modifyOIDList),'len(self.modifyOIDList)')
            #         for i in sellW.modifyOIDList:
            #             th1 = Thread(target=sellW.modify,
            #                          args=(i[0], self.cbOrdType.currentText(),  i[1],self.leDiscQ.text(),
            #                                self.leRate.text(), self.leTrigger.text(), self.cbStretegyNo.currentText() ,
            #                                  self.leClient.text()))
            #             th1.start()
            #
            #     else:
            #         th1 = Thread(target=self.modify,
            #                      args=(self.modifyOIDList[0][0], self.cbOrdType.currentText(), self.modifyOIDList[0][1], self.leDiscQ.text(),
            #                            self.leRate.text(), self.leTrigger.text(), self.cbStretegyNo.currentText(),
            #                            self.leClient.text()))
            #         th1.start()

        hideWindow(self.sellW)
    except:
        print(sys.exc_info())

############################ Ends Here ############################

def refresh_config(self):
    self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source, market_data_appKey, market_data_secretKey, ia_appKey, ia_secretKey, clist, DClient, broadcastMode = readConfig_All()

def dec_v(self):
    if (self.leQty.hasFocus() == True):
        if (self.leQty.text() != '0'):
            self.leQty.setText(str(int(self.leQty.text()) - self.lotsize))
    if (self.leRate.hasFocus() == True):
        if (self.leRate.text() != '0'):
            aa = '%.2f' % (float(self.leRate.text()) - float(self.ticksize))
            self.leRate.setText(aa)


def inc_v(self):
    if (self.leQty.hasFocus() == True):
        self.leQty.setText(str(int(self.leQty.text()) + self.lotsize))
    if (self.leRate.hasFocus() == True):
        aa = '%.2f' % (float(self.leRate.text()) + float(self.ticksize))
        self.leRate.setText(aa)


def dec_v1(self):
    # a=QtWidgets.QLineEdit()
    # a.hasFocus()
    if (self.leQty.hasFocus() == True):
        if (self.leQty.text() != '0'):
            self.leQty.setText(str(int(self.leQty.text()) - self.lotsize))
    if (self.leRate.hasFocus() == True):
        if (self.leRate.text() != '0'):
            aa = '%.2f' % (float(self.leRate.text()) - float(self.ticksize) * 20)
            self.leRate.setText(aa)


def inc_v1(self):
    if (self.leQty.hasFocus() == True):
        self.leQty.setText(str(int(self.leQty.text()) + self.lotsize))
    if (self.leRate.hasFocus() == True):
        aa = '%.2f' % (float(self.leRate.text()) + float(self.ticksize) * 20)
        self.leRate.setText(aa)


def set2List(self):
    self.cbCli.setCurrentIndex(1)


def set2Market(self):
    self.cbOrdType.setCurrentIndex(1)


def setAllShortcuts(self):
    self.scMarket = QShortcut(QKeySequence('Alt+M'), self)
    self.scMarket.activated.connect(lambda:set2Market(self))
    self.leRate.sc_up = QShortcut(QKeySequence('Up'), self.leRate)
    self.leRate.sc_up.setContext(Qt.WidgetWithChildrenShortcut)
    self.leRate.sc_up.activated.connect(lambda: inc_v(self))
    self.leRate.sc_up1 = QShortcut(QKeySequence('Ctrl+Up'), self.leRate)
    self.leRate.sc_up1.setContext(Qt.WidgetWithChildrenShortcut)
    self.leRate.sc_up1.activated.connect(lambda: inc_v1(self))
    self.leRate.sc_down = QShortcut(QKeySequence('Down'), self.leRate)
    self.leRate.sc_down.activated.connect(lambda: dec_v(self))
    self.leRate.sc_down.setContext(Qt.WidgetWithChildrenShortcut)
    self.leRate.sc_down1 = QShortcut(QKeySequence('Ctrl+Down'), self.leRate)
    self.leRate.sc_down1.activated.connect(lambda: dec_v1(self))
    self.leRate.sc_down1.setContext(Qt.WidgetWithChildrenShortcut)
    self.leQty.sc_up = QShortcut(QKeySequence('Up'), self.leQty)
    self.leQty.sc_up.setContext(Qt.WidgetWithChildrenShortcut)
    self.leQty.sc_up.activated.connect(lambda: inc_v(self))
    self.leQty.sc_up1 = QShortcut(QKeySequence('Ctrl+Up'), self.leQty)
    self.leQty.sc_up1.setContext(Qt.WidgetWithChildrenShortcut)
    self.leQty.sc_up1.activated.connect(lambda: inc_v(self))

    self.leQty.sc_down = QShortcut(QKeySequence('Down'), self.leQty)
    self.leQty.sc_down.activated.connect(lambda: dec_v(self))
    self.leQty.sc_down.setContext(Qt.WidgetWithChildrenShortcut)

    self.leQty.sc_down1 = QShortcut(QKeySequence('Ctrl+Down'), self.leQty)
    self.leQty.sc_down1.activated.connect(lambda: dec_v(self))
    self.leQty.sc_down1.setContext(Qt.WidgetWithChildrenShortcut)
    # self.PlaceOrdSc1 = QShortcut(QKeySequence('Return'), self)
    # self.PlaceOrdSc1.activated.connect(lambda: placeOrd(self))
    # self.PlaceOrdSc2 = QShortcut(QKeySequence('Enter'), self)
    # self.PlaceOrdSc2.activated.connect(lambda: placeOrd(self))
    # self.pbSubmit.clicked.connect(lambda: placeOrd(self))


def modify(self, apporderid, orderType, qty, discQty, Mprice, MStopPrice, OrderUniqueID, clientId):
    try:
        if (self.source != 'TWSAPI'):

            modify_payload = {
                "appOrderID": apporderid,
                "modifiedProductType": "NRML",
                "modifiedOrderType": orderType,
                "modifiedOrderQuantity": qty,
                "modifiedDisclosedQuantity": discQty,
                "modifiedLimitPrice": Mprice,
                "modifiedStopPrice": MStopPrice,
                "modifiedTimeInForce": "DAY",
                "orderUniqueIdentifier": OrderUniqueID
            }
        else:
            modify_payload = {
                "clientID": clientId,
                "appOrderID": apporderid,
                "modifiedProductType": "NRML",
                "modifiedOrderType": orderType,
                "modifiedOrderQuantity": qty,
                "modifiedDisclosedQuantity": discQty,
                "modifiedLimitPrice": Mprice,
                "modifiedStopPrice": MStopPrice,
                "modifiedTimeInForce": "DAY",
                "orderUniqueIdentifier": OrderUniqueID
            }

        print(modify_payload)
        # modify_payload1 = json.dumps(modify_payload,cls=NumpyEncoder)
        place_order_url = requests.put(self.apiip + '/interactive/orders', json=modify_payload,
                                       headers=self.iheaders)
        data_p_order = place_order_url.json()
        print('Order Modification request', data_p_order)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])

def hideWindow(self):
    self.isFresh = True
    self.hide()
