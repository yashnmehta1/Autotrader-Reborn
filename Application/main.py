from PyQt5.QtGui import *

from Theme.dt2 import dt1
from qtwidgets import AnimatedToggle

import platform

from Application.Utils.scriptSearch import scriptBarSlots

from Application.Utils.animations import *
from Application.Utils.feedHandler import FeedHandler
from Application.Utils.supMethods import *
from Application.Utils.configReader import refresh
from Application.Utils.updation import *

from Application.Services.Xts.Sockets.Trade.interactiveApi import Interactive
from Application.Services.Xts.Sockets.Feeds.marketData import MarketFeeds

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
from Application.Views.MultiOrders.multiOrders import Ui_MultiOrders

from Application.Utils.basicWinOps import res_max

from Application.Utils.createTables import tables_details_mw, tables_details_mw_basic, tables_details_mo
from Application.Services.UDP.UDPSock import Receiver
from Application.Views.FolioPosition.support import filterData

from Application.Services.Xts.Api import servicesMD
from Application.Services.Xts.Api import servicesIA
from Application.Utils.configReader import get_udp_port
from Application.Utils.shortcuts import setShortcuts
from Application.Views.multiModification import Ui_MultiModification
from PyQt5 import uic

from Application.Utils.animations import createAnimations
from Application.Utils.all_slots import createSlots_main



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
        createSlots_main(self)

        effectWorking(self)
        createAnimations(self)


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
            self.multiModifyW = Ui_MultiModification()

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
            self.multiOrders = Ui_MultiOrders()
            tables_details_mo(self)
            self.PendingW = PendingOrder()
            self.OrderBook =OrderBook(self)
            self.TradeW = TradeBook(self)
            self.PreferanceW = Ui_Preferences(self)
            self.Banned = Ui_Banned()
            self.mainFrame.layout().addWidget(self.CFrame,0,1)
            self.CFrame.dockOP.setWidget(self.PendingW)
            self.CFrame.dockMGR.setWidget(self.Manager)
            self.CFrame.dockMW.setWidget(self.marketW)
            self.CFrame.dockMW_basic.setWidget(self.marketWB)
            self.CFrame.resizeDocks([self.CFrame.dockOP,self.CFrame.dockMW],[500,500],Qt.Vertical)
            self.CFrame.resizeDocks([self.CFrame.dockOP],[500],Qt.Horizontal)
            self.login = Ui_Login()
            self.FeedHandler = FeedHandler()
            self.PendingW.FeedHandler = self.FeedHandler
            self.createTimers()
            self.msg = QMessageBox()
        except:
            print(traceback.print_exc())




    def cancelAllMDAPIConnction(self):
        self.LiveFeed.sgNSQrec.disconnect(self.PendingW.sock1502)
        self.LiveFeed.sgNSQrec.disconnect(self.snapW.sock1502)
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


    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)


    #################################################################
    def updateOnPosition(self,position):
        print("update on position")
        update_Position_Socket_NP(self, position)
        update_Position_socket_MW(self,position)

    def updateOderSocket(self,order):
        updateSocketOB(self.OrderBook,order)
        updateSocketPOB(self.PendingW,order)

    def updateOnTrade(self,trade):
        updateTradeSocket_TB(self,trade)
        updateGetTrade_FP(self,trade)

    ##################################################################
    # currently not in us
    def updateGetorderBook(self,order,rowNo):
        updateGetOrder_OB(self,order,rowNo)
    def updateGetPendinOrderBook(self,order,rowNo):
        updateGetOrder_POB(order,rowNo)

    def on_get_tradeBook(self,tradeBook):
        updateGetTradeApi(self.TradeW,tradeBook)
        updateGetTrade_FP(self.FolioPos,tradeBook)


    ##################################################################

    ##################################################################

    def on_new_feed_1501(self,data):
        UpdateLTP_MW(self,data)
        UpdateLTP_MW_basic(self, data)
        UpdateLTP_NP(self,data)
        UpdateLTP_FP(self,data)
        if(data['Exch'] == 'NSEFO'):
            self.fo_contract[data['Token'] - 35000,18 ] = data['LTP']


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




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_Main()
    showSplashScreen(form)
    sys.exit(app.exec_())
