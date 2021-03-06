from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
import traceback
import logging
import time

from Application.Services.Xts.Api.servicesIA import PlaceOrder,modifyOrder

import sys


from threading import Thread


def getOrderType(self):
    if(self.cbOrdType.currentIndex()==0):
        return 'LIMIT'
    elif(self.cbOrdType.currentIndex()==1):
        return 'MARKET'
    elif(self.cbOrdType.currentIndex()==2):
        return 'StopLimit'
    elif(self.cbOrdType.currentIndex()==3):
        return 'StopMarket'

def setOrderType(self, orderType):
    if(orderType == 'Limit'):
        self.cbOrdType.setCurrentIndex(0)
    elif (orderType == 'Market'):
        self.cbOrdType.setCurrentIndex(1)

    elif (orderType == 'StopLimit'):
        self.cbOrdType.setCurrentIndex(2)

    elif (orderType == 'StopMarket'):
        self.cbOrdType.setCurrentIndex(3)

def showWindow(self, exchange ,token, price, qty, symbol, instrument, exp, strk, opt, freezeQty ,lotSize ,tickSize,triggerPrice, uid='', validity='DAY',productType='NRML',orderType='LIMIT', isFreshOrd = True):
    try:

        self.sellW.leToken.setText(str(token))
        self.sellW.leInsType.setText(instrument)
        self.sellW.leSymbol.setText(symbol)
        self.sellW.cbExp.clear()
        self.sellW.cbExp.addItem(exp)
        self.sellW.cbStrike.clear()
        self.sellW.cbStrike.addItem(strk)
        self.sellW.cbOpt.clear()
        self.sellW.cbOpt.addItem(opt)
        self.sellW.leMLT.setText('1')
        self.sellW.leQty.setText(str(qty))
        self.sellW.leRate.setText(price)
        self.sellW.lotsize =lotSize
        self.sellW.ticksize =tickSize
        self.sellW.freezeQty = freezeQty
        setOrderType(self.sellW,orderType)
        self.sellW.cbProduct.setCurrentText(productType)
        self.sellW.cbValidity.setCurrentText(validity)
        self.sellW.leTrigger.setText(triggerPrice)
        if (isFreshOrd == False):
            self.sellW.cbStretegyNo.setCurrentText(uid)
        self.sellW.isFresh = isFreshOrd
        self.sellW.show()

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
            else:

                th1 = Thread(target=modifyOrder,
                             args=(self,sellW.appOrderIdFprModification,exchange,clientID,token,orderSide,qty,limitPrice,disQty,triggerPrice,uid,orderType,productType,validity))
                th1.start()
        hideWindow(self.sellW)
        sellW.appOrderIdFprModification=0
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

def hideWindow(self):
    self.isFresh = True
    self.hide()
