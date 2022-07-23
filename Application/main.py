from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import qdarkstyle
from Theme.dt2 import dt1
from qtwidgets import AnimatedToggle

import numpy as np
import time
import datetime
import threading
import sys
import traceback
import logging
import platform
from os import path, getcwd,makedirs,listdir
import playsound

from Application.Utils.scriptSearch import scriptBarSlots

from Application.Utils.animations import *
from Application.Utils.feedHandler import FeedHandler
from Application.Utils.getMasters import  *
from Application.Utils.banned import *
from Application.Utils.supMethods import *
from Application.Utils.configReader import all_refresh_config,refresh
from Application.Utils.updation import *

from Application.Services.Xts.Sockets.Trade.interactiveApi import Interactive
from Application.Services.Xts.Sockets.Feeds.marketData import MarketFeeds

from Application.Views.Models.ProxyModel import ProxyModel
from Application.Views.Models.tableTB import ModelTB
from Application.Views.Models.tableMW import  ModelPosition
from Application.Views.Models.tableOrder import ModelOB

from Application.Views.SManager.sManager import Manager
from Application.Views.PendingOrder.pendingOrder import PendingOrder
from Application.Views.Banned.bannedScript import Ui_Banned
from Application.Views.OrderBook.orderBook import OrderBook
from Application.Views.TradeBook.tradeBook import TradeBook
from Application.Views.Prerferences.prefereances import Ui_Preferences
from Application.Views.MarketWatch.mWatch import MarketW
from Application.Views.basicMWatch.mWatch import MarketW_basic
from Application.Views.Login.login import Ui_Login
from Application.Views.cframe import  Ui_CFrame
from Application.Views.splashScreen import Ui_Splash
from Application.Views.titlebar import tBar
from Application.Views.BuyWindow.buyWindow import Ui_BuyW
from Application.Views.SellWindow.sellWindow import Ui_SellW
from Application.Views.SnapQuote.snapQuote import Ui_snapQ
from Application.Views.FolioPosition.folioPosition  import FolioPosition
from Application.Views.NetPosition.netPosition  import NetPosition
from Application.Utils.basicWinOps import res_max

from Application.Utils.createTables import tables_details_mw, tables_details_mw_basic
from Application.Services.UDP.UDPSock import Receiver
from Application.Views.FolioPosition.support import filterData

from Application.Services.Xts.Api import servicesMD
from Application.Services.Xts.Api import servicesIA
from Application.Utils.configReader import get_udp_port
from Application.Utils.shortcuts import setShortcuts
from PyQt5 import uic

from Application.Stretegies import TSpecial

class Ui_Main(QMainWindow):
    ################################# Intialization Here ##################################################
    def __init__(self):
        super(Ui_Main, self).__init__()
        self.osType = platform.system()
        #########################################################
        getLogPath(self)
        ########################################################
        #########################################################
        loc1 = getcwd().split('Application')
        ui_login = path.join(loc1[0],'Resourses','UI','Main.ui')
        uic.loadUi(ui_login, self)
        flags = Qt.WindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.title = tBar('ANV TRADER')
        self.headerFrame.layout().addWidget(self.title,0,1)

        self.title.setStyleSheet('  border-radius: 4px;')
        QSizeGrip(self.frame_5)
        self.setStyleSheet(dt1)
        #########################################################
        #########################################################
        self.objectCreation()
        self.initVariables()
        self.createSlots()

        effectWorking(self)
        self.createAnimations()
        self.scriptBar.layout().addWidget(self.lbUDP,19)
        self.scriptBar.layout().addWidget(self.toggleUDP,20)
        setShortcuts(self)
        refresh(self)

        self.addFolio('abc')
        self.addFolio('parth')

    def objectCreation(self):
        try:
            self.lbUDP = QLabel('UDP FEEDS')
            self.toggleUDP = AnimatedToggle()
            self.toggleUDP.setMaximumHeight(25)
            self.toggleUDP.setMaximumWidth(50)
            self.lbUDP.setMaximumWidth(55)
            self.Splash = Ui_Splash()

            self.buyW = Ui_BuyW()
            self.sellW = Ui_SellW()
            self.snapW = Ui_snapQ()

            get_udp_port(self)

            self.recv_fo = Receiver(self.port_fo)
            self.recv_cash = Receiver(self.port_cash)

            self.CFrame = Ui_CFrame()

            self.LiveFeed = MarketFeeds()
            self.IAS = Interactive()

            self.marketW = MarketW()
            self.marketWB = MarketW_basic()
            self.marketW.buyw = Ui_BuyW()
            self.marketW.sellw = Ui_SellW()

            tables_details_mw(self)
            tables_details_mw_basic(self)
            self.FolioPos = FolioPosition()
            self.NetPos = NetPosition()
            self.Manager = Manager()

            self.PendingW = PendingOrder()
            self.OrderBook =OrderBook(self)
            self.TradeW = TradeBook(self)

            self.PreferanceW = Ui_Preferences(self)

            self.Banned = Ui_Banned()


            self.mainFrame.layout().addWidget(self.CFrame,0,1)
            self.CFrame.dockOP.setWidget(self.PendingW)

            # self.CFrame.dockPB.setWidget(self.FolioPos)
            self.CFrame.dockMGR.setWidget(self.Manager)
            self.CFrame.dockMW.setWidget(self.marketW)
            self.CFrame.dockMW_basic.setWidget(self.marketWB)

            self.CFrame.resizeDocks([self.CFrame.dockOP,self.CFrame.dockMW],[500,500],Qt.Vertical)
            self.CFrame.resizeDocks([self.CFrame.dockOP],[500],Qt.Horizontal)

            self.login = Ui_Login()
            self.FeedHandler = FeedHandler()

            # self.marketW.snapW.FeedHandler = self.FeedHandler
            self.PendingW.FeedHandler = self.FeedHandler
            self.createTimers()

            self.msg = QMessageBox()
        except:
            print(traceback.print_exc())


    def createSlots(self):
        try:
            scriptBarSlots(self)

            self.pbFolioPos.clicked.connect(self.FolioPos.hide)
            self.pbFolioPos.clicked.connect(self.FolioPos.show)
            self.pbNetPos.clicked.connect(self.NetPos.hide)
            self.pbNetPos.clicked.connect(self.NetPos.show)
            self.pbTradeB.clicked.connect(self.TradeW.hide)
            self.pbTradeB.clicked.connect(self.TradeW.show)
            self.pbOrderB.clicked.connect(self.OrderBook.hide)
            self.pbOrderB.clicked.connect(self.OrderBook.show)

            self.pbPreferences.clicked.connect(self.PreferanceW.show)
            self.PreferanceW.pbApply.clicked.connect(lambda:self.setDefaultClient(self.PreferanceW.cbCList.currentText))

            ################################## Trade Setting Slot  ##########################################


            ################################# Login Class Slota ####################################

            self.login.pbLogin.clicked.connect(self.proceed2login)
            self.login.pbNext.clicked.connect(self.proceed2Main)
            self.login.pbCancel.clicked.connect(sys.exit)


            self.IAS.sgSocketConn.connect(self.LiveFeed.start_socket)
            self.IAS.sgSocketConn.connect(lambda:changeIAS_connIcon(self,0))
            self.IAS.sgSocketConn.connect(lambda:self.login.label.append('Interactive socket is connected'))
            self.LiveFeed.sgSocketConn.connect(lambda:changeMD_connIcon(self,0))
            self.LiveFeed.sgSocketConn.connect(lambda: self.login.label.append('Marketdata socket is connected'))
            self.LiveFeed.sgSocketConn.connect(self.login.pbNext.show)

            ################################################################################3
            # self.marketW.buyw.sgAppOrderID.connect(self.inPoreccessOrderIds.append)
            # self.marketW.sellw.sgAppOrderID.connect(self.inPoreccessOrderIds.append)
            #########################################################################################3
            # self.IAS.sgGetAPIpos.connect(lambda: updateGetPosition(self))
            self.IAS.sgOpenPos.connect(lambda: updateOpenPosition(self))
            self.IAS.sgAPIpos.connect(self.updateOnPosition)

            self.IAS.sgGetTrd.connect(self.on_get_tradeBook)
            self.IAS.sgTrdSoc.connect(self.updateOnTrade)

            ######################################################################
            # both getOrderbook process is done directly from Api call methos only
            # self.IAS.sgGetOrder.connect(self.updateGetorderBook)
            # self.IAS.sgGetPOrder.connect(self.updateGetPendinOrderBook)
            ######################################################################


            self.IAS.sgPendSoc.connect(self.updateOderSocket)
            ############################################################################################
            self.LiveFeed.sgindexfd.connect(lambda:self.on_new_feed_Index)
            self.LiveFeed.sgNPFrec.connect(self.on_new_feed_1501)
            self.LiveFeed.sgNSQrec.connect(self.on_new_feed_1502)
            #########################################################################################3
            self.IAS.sgStatusUp.connect(lambda:updateStatusLable(self,'x'))
            #########################################################################################3
            # self.PositionW.sgTMTM.connect(self.setMTM)
            self.bt_close.clicked .connect(self.close)
            self.bt_min.clicked.connect(self.showMinimized)
            self.bt_max.clicked.connect(lambda:res_max(self))
            self.title.sgPoss.connect(self.movWin)
            # self.pbMenu.clicked.connect(self.openSideBar)
            # self.pbDPosition.clicked.connect(lambda:showDetailPos(self.marketW.DetailPos))

            self.pbDelta.clicked.connect(lambda:showDeltaSummary)
            self.pbBanned.clicked.connect(self.Banned.show)

            self.Splash.sgFin.connect(lambda:splashWork(self))
            self.btnIB.clicked.connect(lambda:showIndexBar(self))
            self.btnSB.clicked.connect(lambda:showScriptBar(self))
            self.btnSttn.clicked.connect(lambda:showSettingMenu(self))
            self.btnMMW.clicked.connect(lambda:showM2mW(self))
            self.title.sgDClick.connect(lambda:res_max(self))
            self.marketW.sgShowPending.connect(lambda:showPendingMW(self))

            self.Banned.pbAddBSym.clicked.connect(lambda:addBannedSymbol(self))
            self.Banned.pbAddBIns.clicked.connect(lambda:addBannedInstrument(self))
            self.Banned.pbRemBSym.clicked.connect(lambda:remBannedSymbol(self))
            self.Banned.pbRemBIns.clicked.connect(lambda:remBannedInstrument(self))


            self.Manager.pbAdd.clicked.connect(self.addNewStretegy)
        except:
            print(traceback.print_exc())

    def createTimers(self):
        self.timeSplash =QTimer()
        self.timeSplash.setInterval(1000)
        self.timeSplash.timeout.connect(self.SplashTimerWorking)


        self.timerChStatus = QTimer()
        self.timerChStatus.setInterval(5000)
        self.timerChStatus.timeout.connect(lambda:clearStatus(self))
        self.timerChStatus.start()


    def createAnimations(self):
        self.anim41 = QPropertyAnimation(self.scriptBar, b"maximumHeight")
        self.anim31 = QPropertyAnimation(self.indexBar, b"maximumHeight")
        self.anim32 = QPropertyAnimation(self.indexBar, b"maximumHeight")
        self.anim71 = QPropertyAnimation(self.settingsMenu, b"minimumWidth")
        self.anim72 = QPropertyAnimation(self.settingsMenu, b"minimumWidth")
        self.anim42 = QPropertyAnimation(self.scriptBar, b"maximumHeight")
        self.anim93 = QPropertyAnimation(self.lbMTM, b"maximumWidth")
        self.anim94 = QPropertyAnimation(self.lbMTM, b"maximumWidth")

    def SplashTimerWorking(self):
        self.Splash.close()
        self.login.show()
        # self.show()
        self.timeSplash.stop()

###########################################################
    def setMTM(self,a):
        self.lbMTM.setText(a)
        if(float(a)>0):
            self.lbMTM.setStyleSheet('QLabel {background-color: #1464A0;border: 1px solid #2d2d2d;color: #F0F0F0;border-radius: 4px;padding: 3px;outline: none;min-width: 10px;}')
        else:
            self.lbMTM.setStyleSheet('QLabel {background-color: #c32051;border: 1px solid #2d2d2d;color: #F0F0F0;border-radius: 4px;padding: 3px;outline: none;min-width: 10px;}')


    def setclist(self,a):
        self.PreferanceW.cbCList.addItems(a)
        self.marketW.buyw.clist=a
        self.marketW.sellw.clist=a

    def setDefaultClient(self,a):
        try:
            self.DefaultClient = a
            self.marketW.buyw.DefaultClient=self.DefaultClient
            self.marketW.sellw.DefaultClient=self.DefaultClient

            self.marketW.buyw.leClient.setText(self.DefaultClient)
            self.marketW.sellw.leClient.setText(self.DefaultClient)

            # self.marketW.snapW.sellw.leClient.setText(self.DefaultClient)

        except:
            logging.error(traceback.print_exc())
    def shareContract(self):
        try:
            self.fo_contract1 = self.fo_contract[np.where(self.fo_contract[:,1] != 'x')]
            self.eq_contract1 = self.eq_contract[np.where(self.eq_contract[:,1] !='x')]
            self.cd_contract1 = self.cd_contract[np.where(self.cd_contract[:,1] !='x')]

            self.IAS.fo_contract = self.fo_contract
            self.IAS.eq_contract = self.eq_contract
            self.IAS.cd_contract = self.cd_contract

            self.snapW.fo_contract1 = self.fo_contract1
            self.snapW.eq_contract1 = self.eq_contract1
            self.snapW.cd_contract1 = self.cd_contract1

            # self.snapW.fo_contract = self.fo_contract
            # self.snapW.eq_contract = self.eq_contract
            # self.snapW.cd_contract = self.cd_contract

            self.marketW.fo_contract = self.fo_contract
            self.marketW.eq_contract = self.eq_contract
            self.marketW.cd_contract = self.cd_contract

        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])


    def cancelAllMDAPIConnction(self):
        self.LiveFeed.sgNSQrec.disconnect(self.PendingW.sock1502)
        self.LiveFeed.sgNSQrec.disconnect(self.snapW.sock1502)
        # self.LiveFeed.sgNSQrec.disconnect(self.snapW.sock1502)
        # self.LiveFeed.sgNPFrec.disconnect(self.UpdateLTP)
        # self.LiveFeed.sgNPFrec.disconnect(self.updatefuturePdict)
        self.LiveFeed.sgNPFrec.disconnect(self.PositionW.MTM_update)

    def initVariables(self):
        self.inPoreccessOrderIds = []

        ################### as part of window animation ############
        self.isIndexBarOpen =True
        self.isSTBarOpen =True
        self.AllowOnlyIndex = False
        self.isScriptBarOpen =True
        self.isSidebarOpen =False
        self.isMenuOpen = False
        self.isMrgWOpen = False
        self.isMMWOpen = False
        ############################################################
        self.jobbinMode = False
        self.Mrglvl = 0
        self.listBannedSymbol = []
        self.listBannedIns = []
        self.isOverOTRFIndex = True  #check its use
        self.openPosDict ={}

    def proceed2login(self):
        servicesMD.login(self)
        servicesIA.login(self)

    def proceed2Main(self):
        self.login.hide()
        self.show()
        self.showMaximized()
        filterData(self.FolioPos)
        servicesMD.subscribeToken(self, 26000, 'NSECM')
        servicesMD.subscribeToken(self, 26001, 'NSECM')
        servicesMD.subscribeToken(self, 26002, 'NSECM')

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)


    #################################################################
    def updateOnPosition(self,position):
        print("update on position")
        update_Position_Socket_NP(self, position)

        update_Position_socket_MW(self,position)
    ##################################################################
    # currently not in use

    def updateGetorderBook(self,order,rowNo):
        updateGetOrder_OB(self,order,rowNo)

    def updateGetPendinOrderBook(self,order,rowNo):
        updateGetOrder_POB(order,rowNo)
    ##################################################################

    def updateOderSocket(self,order):
        self.OrderBook.updateSocketOB(order)
        updateSocketPOB(self.PendingW,order)

    ##################################################################
    def on_get_tradeBook(self,tradeBook):
        updateGetTradeApi(self.TradeW,tradeBook)
        updateGetTrade_FP(self.FolioPos,tradeBook)

    def updateOnTrade(self,trade):
        updateTradeSocket_TB(self,trade)
        updateGetTrade_FP(self,trade)
    ##################################################################



    def on_new_feed_1501(self,data):
        UpdateLTP_MW(self,data)
        UpdateLTP_MW_basic(self, data)
        UpdateLTP_NP(self,data)
        UpdateLTP_FP(self,data)


    def on_new_feed_1502(self,data):
        sock1502(self.snapW,data)
    def on_new_feed_Index(self,data):
        updateCashIndex(self,data)

    def addNewStretegy(self):
        if(self.Manager.lastSelectedStretegy == self.Manager.pbTSpecial):
            newStretegy = TSpecial.TSpecial.logic()
            newStretegy.createObject(self.fo_contract)
            # newStretegy.createConnection()
            self.Manager.stretegyList.append(newStretegy)
            x=len(self.Manager.stretegyList)
            folioName = str(x) +'_TSpecial'
            newStretegy.addW.leFolioName.setText(folioName)
            newStretegy.addW.show()


    def addFolio(self,folio):
        self.buyW.cbStretegyNo.addItem(folio)
        self.sellW.cbStretegyNo.addItem(folio)
        self.FolioPos.folioList.append(folio)
        self.FolioPos.cbUID.addItem(folio)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_Main()
    showSplashScreen(form)
    sys.exit(app.exec_())
