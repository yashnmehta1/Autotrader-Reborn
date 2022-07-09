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

def hideWindow(self):
    self.isFresh = True
    self.hide()

def getOrderType(self):
    if(self.cbOrdType.currentIndex()==0):
        return 'LIMIT'
    elif(self.cbOrdType.currentIndex()==1):
        return 'MARKET'
    elif(self.cbOrdType.currentIndex()==2):
        return 'StopLimit'
    elif(self.cbOrdType.currentIndex()==3):
        return 'StopMarket'

def dec_v(self):
    if(self.leQty.hasFocus( ) == True):
        if (self.leQty.text( ) != '0'):
            self.leQty.setText(str(int(self.leQty.text() ) -self.lotsize))
    if(self.leRate.hasFocus( ) == True):
        if (self.leRate.text( ) != '0'):
            aa ='%.2f ' %(float(self.leRate.text() ) -float(self.ticksize))
            self.leRate.setText(aa)

def inc_v(self):
    if(self.leQty.hasFocus( )==True):
        self.leQty.setText(str(int(self.leQty.text() ) +self.lotsize))
    if(self.leRate.hasFocus( )==True):
        aa = '%.2f' % (float(self.leRate.text()) + float(self.ticksize))
        self.leRate.setText(aa)

def dec_v1(self):
    if(self.leQty.hasFocus( ) == True):
        if (self.leQty.text( ) != '0'):
            self.leQty.setText(str(int(self.leQty.text() ) -self.lotsize))
    if(self.leRate.hasFocus( ) == True):
        if (self.leRate.text( ) != '0'):
            aa ='%.2f ' %(float(self.leRate.text() ) -float(self.ticksize ) *20)
            self.leRate.setText(aa)

def inc_v1(self):
    if(self.leQty.hasFocus( ) == True):

        self.leQty.setText(str(int(self.leQty.text() ) +self.lotsize))
    if(self.leRate.hasFocus( ) == True):
        aa = '%.2f' % (float(self.leRate.text()) + float(self.ticksize ) *20)
        self.leRate.setText(aa)

def chackMaxMlt(self):
    if(int(self.leMLT.text()) > 10):
        self.leMLT.setText('10')

def set2List(self):
    self.cbCli.setCurrentIndex(1)

def set2Market(self):
    self.cbOrdType.setCurrentIndex(1)

def placeOrd(self):
    try:
        ##############################################################################################
        buyW = self.buyW
        if(buyW.leToken.text() != ''):
            clientID = buyW.leClient.text()
            exchange = buyW.cbEx.currentText()
            token = int(buyW.leToken.text())
            uid = buyW.cbStretegyNo.currentText()
            limitPrice = float(buyW.leRate.text())
            disQty = int(buyW.leDiscQ.text())
            qty = int(buyW.leQty.text())
            triggerPrice = float(buyW.leTrigger.text())

            ##############################################################################################
            productType = buyW.cbProduct.currentText()
            orderSide = 'BUY'
            if(limitPrice==0):
                orderType = 'MARKET'
            else:
                orderType = getOrderType(buyW)

            validity = buyW.cbValidity.currentText()
            if(buyW.isFresh):
                buyW.mltplr = int(buyW.leMLT.text())
                for i in range(buyW.mltplr):
                    th1 = Thread(target=PlaceOrder,args=(self,
                                     exchange, clientID, token, orderSide,  qty,
                                    limitPrice,  validity, disQty,triggerPrice,uid,
                                     orderType,productType))
                    th1.start()
            # else:
            #     if(len(buyW.modifyOIDList)>1):
            #         print(len(buyW.modifyOIDList),'len(self.modifyOIDList)')
            #         for i in buyW.modifyOIDList:
            #             th1 = Thread(target=buyW.modify,
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

        hideWindow(self.buyW)

    except:
        print(traceback.print_exc())

def modify(self,apporderid,orderType,qty,discQty,Mprice,MStopPrice,OrderUniqueID,clientId):
    try:
        if(self.source !='TWSAPI'):
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
        place_order_url = requests.put(self.URL + '/interactive/orders', json=modify_payload,
                                        headers=self.IAheaders)
        data_p_order = place_order_url.json()
        print('Order Modification request',data_p_order)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])

def showWindow(self, exchange,token, price, qty, symbol, instrument, exp, strk, opt, freezeQty,lotSize,tickSize):
    if(self.buyW.isVisible()):
        hideWindow(self.buyW)

    self.buyW.cbEx.clear()
    self.buyW.cbEx.addItem(exchange)

    self.buyW.leToken.setText(str(token))
    self.buyW.leInsType.setText(instrument)
    self.buyW.leSymbol.setText(symbol)
    self.buyW.cbExp.clear()
    self.buyW.cbExp.addItem(exp)
    self.buyW.cbStrike.clear()
    self.buyW.cbStrike.addItem(strk)
    self.buyW.cbOpt.clear()
    self.buyW.cbOpt.addItem(opt)
    self.buyW.leQty.setText(str(lotSize))
    self.buyW.leRate.setText(price)


    self.buyW.leMLT.setText('1')


    self.buyW.show()

    self.buyW.lotsize=lotSize
    self.buyW.ticksize =tickSize
    self.buyW.freezeQty = freezeQty

def setAllShortcuts(self):

    self.bt_min.clicked.connect(lambda: hideWindow(self))
    self.bt_close.clicked.connect(lambda: hideWindow(self))

    self.quitSc = QShortcut(QKeySequence('Esc'), self)
    self.quitSc.activated.connect(lambda: hideWindow(self))

    self.scMarket = QShortcut(QKeySequence('Alt+M'), self)
    self.scMarket.activated.connect(lambda:set2Market(self))
    self.leRate.sc_up = QShortcut(QKeySequence('Up'), self.leRate)
    self.leRate.sc_up.setContext(Qt.WidgetWithChildrenShortcut)
    self.leRate.sc_up.activated.connect(lambda:inc_v(self))
    self.leRate.sc_up1 = QShortcut(QKeySequence('Ctrl+Up'), self.leRate)
    self.leRate.sc_up1.setContext(Qt.WidgetWithChildrenShortcut)
    self.leRate.sc_up1.activated.connect(lambda:inc_v1(self))
    self.leRate.sc_down = QShortcut(QKeySequence('Down'), self.leRate)
    self.leRate.sc_down.activated.connect(lambda:dec_v(self))
    self.leRate.sc_down.setContext(Qt.WidgetWithChildrenShortcut)
    self.leRate.sc_down1 = QShortcut(QKeySequence('Ctrl+Down'), self.leRate)
    self.leRate.sc_down1.activated.connect(lambda:dec_v1(self))
    self.leRate.sc_down1.setContext(Qt.WidgetWithChildrenShortcut)
    self.leQty.sc_up = QShortcut(QKeySequence('Up'), self.leQty)
    self.leQty.sc_up.setContext(Qt.WidgetWithChildrenShortcut)
    self.leQty.sc_up.activated.connect(lambda:inc_v(self))
    self.leQty.sc_up1 = QShortcut(QKeySequence('Ctrl+Up'), self.leQty)
    self.leQty.sc_up1.setContext(Qt.WidgetWithChildrenShortcut)
    self.leQty.sc_up1.activated.connect(lambda:inc_v(self))
    self.leQty.sc_down = QShortcut(QKeySequence('Down'), self.leQty)
    self.leQty.sc_down.activated.connect(lambda:dec_v(self))
    self.leQty.sc_down.setContext(Qt.WidgetWithChildrenShortcut)
    self.leQty.sc_down1 = QShortcut(QKeySequence('Ctrl+Down'), self.leQty)
    self.leQty.sc_down1.activated.connect(lambda:dec_v(self))
    self.leQty.sc_down1.setContext(Qt.WidgetWithChildrenShortcut)
