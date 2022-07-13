import threading
import traceback
import sys
import requests
import logging

import datetime
from os import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
import  numpy as np
import datatable as dt
from Application.Services.Xts.Api.servicesMD import  subscribeToken,unSubscription_feed
from Application.Utils.scriptSearch import selExchange,addscript




def showPendingMW(self, a):
    self.CFrame.dockOP.raise_()
    self.PendingW.filterStr = a
    self.PendingW.smodelO.setFilterKeyColumn(1)
    self.PendingW.smodelO.setFilterFixedString(a)
    self.PendingW.tableView.setFocus()


def getLogPath(xclass):
    today =  datetime.datetime.today().strftime('%Y%m%d')
    loc1 = getcwd().split('Application')
    xclass.loc1 = loc1
    logDir = path.join(loc1[0] , 'Logs','%s'%today)
    print('logDir',logDir)
    try:
        makedirs(logDir)
    except OSError as e:
        pass
    ls=listdir(logDir)
    attempt =1

    for i in ls:
        x=i.replace('.log','')
        y=x.split('_')
        if( int(y[1]) >= attempt):
            attempt=int(y[1])+1

    print('attempt',attempt)
    xclass.logPath= path.join(logDir, '%s_%s.log'%(today,attempt))


    print('self.logPath',xclass.logPath)
    logging.basicConfig(filename=xclass.logPath, filemode='a+', level=logging.INFO,
                        format='%(asctime)s    %(levelname)s    %(module)s  %(funcName)s   %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')


def effectWorking(self):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(0.01)
    color = QColor(235, 235, 235,30)
    shadow.setColor(color)
    shadow.setXOffset(0)
    shadow.setYOffset(5)
    self.indexBar.setGraphicsEffect(shadow)




def PO4CT(self,Token,FDiffQty,AbsFDiffQty,freezQty,OrderType,Bid,Ask,Segment):

    if (FDiffQty > 0):  # buy

        LimitPrice = Ask + self.logicReplicate.differPoint
        while AbsFDiffQty > freezQty:
            self.PlaceOrder(Token, OrderType, "BUY", freezQty, LimitPrice, self.logicReplicate.FolioNo, 0.00,Segment)
            AbsFDiffQty = AbsFDiffQty - freezQty
        self.PlaceOrder(Token, "MARKET", "BUY", AbsFDiffQty, 1.0, self.logicReplicate.FolioNo, 0.00,Segment)
    else:  # sell
        while AbsFDiffQty > freezQty:
            LimitPrice = Bid - self.logicReplicate.differPoint

            self.PlaceOrder(Token, OrderType, "SELL", freezQty, LimitPrice, self.logicReplicate.FolioNo, 0.00,Segment)
            AbsFDiffQty = AbsFDiffQty - freezQty
        self.PlaceOrder(Token, OrderType, "SELL", AbsFDiffQty, LimitPrice, self.logicReplicate.FolioNo, 0.00,Segment)

def PO4CT1(self, Token, FDiffQty, AbsFDiffQty, freezQty, OrderType, LimitPrice,Segment):

    if (FDiffQty > 0):  # buy


        while AbsFDiffQty > freezQty:
            self.PlaceOrder(Token, OrderType, "BUY", freezQty, LimitPrice, self.logicReplicate.FolioNo, 0.00,Segment)
            AbsFDiffQty = AbsFDiffQty - freezQty
        self.PlaceOrder(Token, "MARKET", "BUY", AbsFDiffQty, 1.0, self.logicReplicate.FolioNo, 0.00,Segment)
    else:  # sell
        while AbsFDiffQty > freezQty:

            self.PlaceOrder(Token, OrderType, "SELL", freezQty, LimitPrice, self.logicReplicate.FolioNo, 0.00,Segment)
            AbsFDiffQty = AbsFDiffQty - freezQty
        self.PlaceOrder(Token, OrderType, "SELL", AbsFDiffQty, LimitPrice, self.logicReplicate.FolioNo, 0.00,Segment)


def changeIAS_connIcon(self,a):
    try:
        if(a==0):
            loc = path.join(self.loc1[0] , 'Resourses','icons','icons','red_icon.png')
            pixmap = QPixmap()
        else:
            loc = path.join(self.loc1[0], 'Resourses', 'icons', 'icons', 'green_icon.png')
            pixmap = QPixmap(loc)
        pixmap = pixmap.scaledToWidth(20)
        pixmap = pixmap.scaledToHeight(20)
        icon = QIcon()
        icon.addPixmap(pixmap)
        self.Interactive_icon.setIcon(icon)
    except:
        print(traceback.print_exc())

def changeMD_connIcon(self,a):
    try:
        if (a == 0):
            pixmap = QPixmap(':/icon1/icons/green_icon.png')
        else:
            pixmap = QPixmap(':/icon1/icons/red_icon.png')
        icon = QIcon()
        icon.addPixmap(pixmap)
        self.MData_icon.setIcon(icon)
        print('f')

    except:
        print(traceback.print_exc())


def clearStatus(self):
    self.lbStatus.setText('')
    self.timerChStatus.stop()


def updateStatusLable(self, a):
    self.lbStatus.setText(a)
    self.timerChStatus.stop()
    self.timerChStatus.setInterval(5000)
    self.timerChStatus.start()




def showBuyWindow(self):
    pass
def showSellWindow(self):
    pass
def ShowPending(self):
    token = self.tableView.selectedIndexes()[0].data()
    self.sgShowPending.emit(str(token))

