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




def showPendingW(main, a):
    main.CFrame.dockOP.raise_()
    main.PendingW.filterStr = a
    main.PendingW.smodelO.setFilterKeyColumn(2)
    main.PendingW.smodelO.setFilterFixedString(str(a))
    main.PendingW.tableView.setFocus()
    main.PendingW.tableView.selectRow(0)

def showFolioPosW(main, a):
    if(a != ''):
        if(main.FolioPos.isVisible()):
            main.FolioPos.hide()

    main.FolioPos.filterStr = a
    main.FolioPos.smodelFP.setFilterKeyColumn(2)
    main.FolioPos.smodelFP.setFilterFixedString(str(a))
    main.FolioPos.tableView.setFocus()
    main.FolioPos.show()

def showTradeBookW(main, a):
    if(a != ''):
        if(main.TradeW.isVisible()):
            main.TradeW.hide()

    main.TradeW.filterStr = a
    main.TradeW.smodelT.setFilterKeyColumn(2)
    main.TradeW.smodelT.setFilterFixedString(str(a))
    main.TradeW.tableView.setFocus()
    main.TradeW.show()
def showOrderBookW(main, a):
    if(a != ''):
        if(main.OrderBook.isVisible()):
            main.OrderBook.hide()

    main.OrderBook.filterStr = a
    main.OrderBook.smodelO.setFilterKeyColumn(2)
    main.OrderBook.smodelO.setFilterFixedString(str(a))
    main.OrderBook.tableView.setFocus()
    main.OrderBook.show()



def getLogPath(xclass):
    today =  datetime.datetime.today().strftime('%Y%m%d')
    loc1 = getcwd().split('Application')
    xclass.loc1 = loc1
    logDir = path.join(loc1[0] , 'Logs','%s'%today)
    # print('logDir',logDir)
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

    # print('attempt',attempt)
    xclass.logPath= path.join(logDir, '%s_%s.log'%(today,attempt))


    # print('main.logPath',xclass.logPath)
    logging.basicConfig(filename=xclass.logPath, filemode='a+', level=logging.INFO,
                        format='%(asctime)s    %(levelname)s    %(module)s  %(funcName)s   %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')


def effectWorking(main):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(0.01)
    color = QColor(235, 235, 235,30)
    shadow.setColor(color)
    shadow.setXOffset(0)
    shadow.setYOffset(5)
    main.indexBar.setGraphicsEffect(shadow)




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


def changeIAS_connIcon(main,a):
    try:
        if(a==0):
            loc = path.join(main.loc1[0] , 'Resourses','icons','icons','red_icon.png')
            pixmap = QPixmap()
        else:
            loc = path.join(main.loc1[0], 'Resourses', 'icons', 'icons', 'green_icon.png')
            pixmap = QPixmap(loc)
        pixmap = pixmap.scaledToWidth(20)
        pixmap = pixmap.scaledToHeight(20)
        icon = QIcon()
        icon.addPixmap(pixmap)
        main.Interactive_icon.setIcon(icon)
    except:
        print(traceback.print_exc())

def changeMD_connIcon(main,a):
    try:
        if (a == 0):
            pixmap = QPixmap(':/icon1/icons/green_icon.png')
        else:
            pixmap = QPixmap(':/icon1/icons/red_icon.png')
        icon = QIcon()
        icon.addPixmap(pixmap)
        main.MData_icon.setIcon(icon)
        print('f')

    except:
        print(traceback.print_exc())


def clearStatus(main):
    main.lbStatus.setText('')
    main.timerChStatus.stop()


def updateStatusLable(main, a):
    main.lbStatus.setText(a)
    main.timerChStatus.stop()
    main.timerChStatus.setInterval(5000)
    main.timerChStatus.start()




def showBuyWindow(self):
    pass
def showSellWindow(self):
    pass
# def ShowPending(self):
#     token = self.tableView.selectedIndexes()[0].data()
#     self.sgShowPending.emit(str(token))





def addFolio(main,folio):
    main.buyW.cbStretegyNo.addItem(folio)
    main.sellW.cbStretegyNo.addItem(folio)
    main.FolioPos.folioList.append(folio)
    main.FolioPos.cbUID.addItem(folio)
    main.multiOrders.cbFolio.addItem(folio)

def setclist(main,a):
    main.PreferanceW.cbCList.addItems(a)
    main.marketW.buyw.clist=a
    main.marketW.sellw.clist=a

def setDefaultClient(main,a):
    try:
        main.DefaultClient = a
        main.marketW.buyw.DefaultClient=main.DefaultClient
        main.marketW.sellw.DefaultClient=main.DefaultClient
        main.marketW.buyw.leClient.setText(main.DefaultClient)
        main.marketW.sellw.leClient.setText(main.DefaultClient)
    except:
        logging.error(traceback.print_exc())



def SplashTimerWorking(main):
    main.Splash.close()
    main.login.show()
    main.timeSplash.stop()

###########################################################
def setMTM(main, a):
    main.lbMTM.setText(a)
    if (float(a) > 0):
        main.lbMTM.setStyleSheet(
            'QLabel {background-color: #1464A0;border: 1px solid #2d2d2d;color: #F0F0F0;border-radius: 4px;padding: 3px;outline: none;min-width: 10px;}')
    else:
        main.lbMTM.setStyleSheet(
            'QLabel {background-color: #c32051;border: 1px solid #2d2d2d;color: #F0F0F0;border-radius: 4px;padding: 3px;outline: none;min-width: 10px;}')



def proceed2login(self):
    servicesMD.login(self)
    servicesIA.login(self)

def proceed2Main(main):
    main.login.hide()
    main.show()
    main.showMaximized()
    filterData(main.FolioPos)
    servicesMD.subscribeToken(main, 26000, 'NSECM')
    servicesMD.subscribeToken(main, 26001, 'NSECM')
    servicesMD.subscribeToken(main, 26002, 'NSECM')





def createTimers(main):
    main.timeSplash =QTimer()
    main.timeSplash.setInterval(1000)
    main.timeSplash.timeout.connect(SplashTimerWorking(main))


    main.timerChStatus = QTimer()
    main.timerChStatus.setInterval(5000)
    main.timerChStatus.timeout.connect(lambda:clearStatus(main))
    main.timerChStatus.start()


def shareContract(main):
    try:
        main.fo_contract1 = main.fo_contract[np.where(main.fo_contract[:,1] != 'x')]
        main.eq_contract1 = main.eq_contract[np.where(main.eq_contract[:,1] !='x')]
        main.cd_contract1 = main.cd_contract[np.where(main.cd_contract[:,1] !='x')]

        main.IAS.fo_contract = main.fo_contract
        main.IAS.eq_contract = main.eq_contract
        main.IAS.cd_contract = main.cd_contract

        main.snapW.fo_contract1 = main.fo_contract1
        main.snapW.eq_contract1 = main.eq_contract1
        main.snapW.cd_contract1 = main.cd_contract1

        main.marketW.fo_contract = main.fo_contract
        main.marketW.eq_contract = main.eq_contract
        main.marketW.cd_contract = main.cd_contract

    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])






def get_ins_details(self,exchange,token):
    # print(self.fo_contract)
    if (exchange == 'NSEFO'):
        ins_details = self.fo_contract[int(token) - 35000,:]
    elif (exchange == 'NSECM'):
        ins_details = self.eq_contract[int(token),:]
    elif (exchange == 'NSECD'):
        ins_details = self.cd_contract[int(token),:]
    return ins_details

