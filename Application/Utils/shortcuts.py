from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt
from Application.Utils.openRequstedWindow import *
from Application.Utils.scriptSearch import *
from Application.Views import BuyWindow
from Application.Views import SellWindow
from Application.Views import PendingOrder
def setWindowShortcuts(self):
    self.quitSc = QShortcut(QKeySequence('Esc'), self)
    self.quitSc.activated.connect(self.hide)




#this methon belongs to main class only
def setShortcuts(self):
    ###############################################################
    # setWindowShortcuts(self)
    ###############################################################

    self.selExch = QShortcut(QKeySequence('Ctrl+S'), self)
    self.selExch.activated.connect(lambda:selExchange(self))




    self.scriptBar.addScript = QShortcut(QKeySequence('Enter'), self.scriptBar)
    self.scriptBar.addScript.setContext(Qt.WidgetWithChildrenShortcut)
    self.scriptBar.addScript.activated.connect(lambda:addscript(self))

    self.scriptBar.addScript = QShortcut(QKeySequence('Return'), self.scriptBar)
    self.scriptBar.addScript.setContext(Qt.WidgetWithChildrenShortcut)
    self.scriptBar.addScript.activated.connect(lambda:addscript(self))


    self.focusMW = QShortcut(QKeySequence('F4'),self)
    self.focusMW.activated.connect(self.marketW.tableView.setFocus)
    self.focusMW.activated.connect(self.CFrame.dockMW.raise_)

    self.focusMW = QShortcut(QKeySequence('Ctrl+F4'),self)
    self.focusMW.activated.connect(self.marketWB.tableView.setFocus)
    self.focusMW.activated.connect(self.CFrame.dockMW_basic.raise_)

    self.marketW.tableView.shortcut_buy = QShortcut(QKeySequence('F1'), self.marketW.tableView)
    self.marketW.tableView.shortcut_buy.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.shortcut_buy.activated.connect(lambda:requestBuyWindow(self,'MarketWatch'))

    self.marketW.tableView.shortcut_buy1 = QShortcut(QKeySequence('+'), self)
    self.marketW.tableView.shortcut_buy1.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.shortcut_buy1.activated.connect(lambda:requestBuyWindow(self,'MarketWatch'))

    self.marketW.tableView.shortcut_sell = QShortcut(QKeySequence('-'), self.marketW.tableView)
    self.marketW.tableView.shortcut_sell.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.shortcut_sell.activated.connect(lambda:requestSellWindow(self,'MarketWatch'))

    self.marketW.tableView.shortcut_sell1 = QShortcut(QKeySequence('F2'), self.marketW.tableView)
    self.marketW.tableView.shortcut_sell1.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.shortcut_sell1.activated.connect(lambda:requestSellWindow(self,'MarketWatch'))


    self.PendingW.tableView.shortcut_modify = QShortcut(QKeySequence('M'), self.PendingW)
    self.PendingW.tableView.shortcut_modify.setContext(Qt.WidgetWithChildrenShortcut)
    self.PendingW.tableView.shortcut_modify.activated.connect(lambda: PendingOrder.support.ModifyOrder(self))


    self.marketWB.tableView.shortcut_buy = QShortcut(QKeySequence('F1'), self.marketWB.tableView)
    self.marketWB.tableView.shortcut_buy.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketWB.tableView.shortcut_buy.activated.connect(lambda:requestBuyWindow(self,'MarketWatch_basic'))

    self.marketWB.tableView.shortcut_buy1 = QShortcut(QKeySequence('+'), self)
    self.marketWB.tableView.shortcut_buy1.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketWB.tableView.shortcut_buy1.activated.connect(lambda:requestBuyWindow(self,'MarketWatch_basic'))

    self.marketWB.tableView.shortcut_sell = QShortcut(QKeySequence('-'), self.marketWB.tableView)
    self.marketWB.tableView.shortcut_sell.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketWB.tableView.shortcut_sell.activated.connect(lambda:requestSellWindow(self,'MarketWatch_basic'))

    self.marketWB.tableView.shortcut_sell1 = QShortcut(QKeySequence('F2'), self.marketWB.tableView)
    self.marketWB.tableView.shortcut_sell1.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketWB.tableView.shortcut_sell1.activated.connect(lambda:requestSellWindow(self,'MarketWatch_basic'))


    self.snapW.shortcut_buy = QShortcut(QKeySequence('F1'), self.snapW)
    self.snapW.shortcut_buy.setContext(Qt.WidgetWithChildrenShortcut)
    self.snapW.shortcut_buy.activated.connect(lambda:requestBuyWindow(self,'SnapQuote'))

    self.snapW.shortcut_buy1 = QShortcut(QKeySequence('+'), self.snapW)
    self.snapW.shortcut_buy1.setContext(Qt.WidgetWithChildrenShortcut)
    self.snapW.shortcut_buy1.activated.connect(lambda:requestBuyWindow(self,'SnapQuote'))

    self.snapW.shortcut_sell = QShortcut(QKeySequence('-'), self.snapW)
    self.snapW.shortcut_sell.setContext(Qt.WidgetWithChildrenShortcut)
    self.snapW.shortcut_sell.activated.connect(lambda:requestSellWindow(self,'SnapQuote'))

    self.snapW.shortcut_sell1 = QShortcut(QKeySequence('F2'), self.snapW)
    self.snapW.shortcut_sell1.setContext(Qt.WidgetWithChildrenShortcut)
    self.snapW.shortcut_sell1.activated.connect(lambda:requestSellWindow(self,'SnapQuote'))

    ############################## F3
    self.marketW.tableView.callPendind = QShortcut(QKeySequence('F3'), self.marketW)
    self.marketW.tableView.callPendind.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.callPendind.activated.connect(lambda:pendingOrderRequested(self,'MarketWatch'))

    self.marketWB.tableView.callPendind = QShortcut(QKeySequence('F3'), self.marketWB)
    self.marketWB.tableView.callPendind.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketWB.tableView.callPendind.activated.connect(lambda:pendingOrderRequested(self,'MarketWatch_basic'))

    self.FolioPos.tableView.callPendind = QShortcut(QKeySequence('F3'), self.FolioPos)
    self.FolioPos.tableView.callPendind.setContext(Qt.WidgetWithChildrenShortcut)
    self.FolioPos.tableView.callPendind.activated.connect(lambda: pendingOrderRequested(self,'FolioPosition'))

    self.NetPos.tableView.callPendind = QShortcut(QKeySequence('F3'), self.NetPos)
    self.NetPos.tableView.callPendind.setContext(Qt.WidgetWithChildrenShortcut)
    self.NetPos.tableView.callPendind.activated.connect(lambda:pendingOrderRequested(self,'NetPosition'))

    self.PendingW.tableView.callPendind = QShortcut(QKeySequence('F3'), self.PendingW)
    self.PendingW.tableView.callPendind.setContext(Qt.WidgetWithChildrenShortcut)
    self.PendingW.tableView.callPendind.activated.connect(lambda: pendingOrderRequested(self,'PendingOrder'))

    self.snapW.callPendind = QShortcut(QKeySequence('F3'), self.snapW)
    self.snapW.callPendind.setContext(Qt.WidgetWithChildrenShortcut)
    self.snapW.callPendind.activated.connect(lambda: pendingOrderRequested(self, 'SnapQuote'))
##############################
    ############################## Ctrl+F3
    self.marketW.tableView.callOrderBook = QShortcut(QKeySequence('Ctrl+F3'), self.marketW)
    self.marketW.tableView.callOrderBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.callOrderBook.activated.connect(lambda: orderBookRequested(self, 'MarketWatch'))

    self.marketWB.tableView.callOrderBook = QShortcut(QKeySequence('Ctrl+F3'), self.marketWB)
    self.marketWB.tableView.callOrderBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketWB.tableView.callOrderBook.activated.connect(lambda: orderBookRequested(self, 'MarketWatch_basic'))

    self.FolioPos.tableView.callOrderBook = QShortcut(QKeySequence('Ctrl+F3'), self.FolioPos)
    self.FolioPos.tableView.callOrderBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.FolioPos.tableView.callOrderBook.activated.connect(lambda: orderBookRequested(self, 'FolioPosition'))

    self.NetPos.tableView.callOrderBook = QShortcut(QKeySequence('Ctrl+F3'), self.NetPos)
    self.NetPos.tableView.callOrderBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.NetPos.tableView.callOrderBook.activated.connect(lambda: orderBookRequested(self, 'NetPosition'))

    self.OrderBook.tableView.callOrderBook = QShortcut(QKeySequence('Ctrl+F3'), self.OrderBook)
    self.OrderBook.tableView.callOrderBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.OrderBook.tableView.callOrderBook.activated.connect(lambda: orderBookRequested(self, 'OrderBook'))

    self.PendingW.tableView.callOrderBook = QShortcut(QKeySequence('Ctrl+F3'), self.PendingW)
    self.PendingW.tableView.callOrderBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.PendingW.tableView.callOrderBook.activated.connect(lambda: orderBookRequested(self, 'PendingOrder'))

    self.snapW.callOrderBook = QShortcut(QKeySequence('Ctrl+F3'), self.snapW)
    self.snapW.callOrderBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.snapW.callOrderBook.activated.connect(lambda: orderBookRequested(self, 'SnapQuote'))
    ##############################
    ############################## F8

    self.marketW.tableView.callTradeBook = QShortcut(QKeySequence('F8'), self.marketW)
    self.marketW.tableView.callTradeBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.callTradeBook.activated.connect(lambda: tradeBookRequested(self, 'MarketWatch'))

    self.marketWB.tableView.callTradeBook = QShortcut(QKeySequence('F7'), self.marketWB)
    self.marketWB.tableView.callTradeBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketWB.tableView.callTradeBook.activated.connect(lambda: tradeBookRequested(self, 'MarketWatch_basic'))

    self.FolioPos.tableView.callTradeBook = QShortcut(QKeySequence('F8'), self.FolioPos)
    self.FolioPos.tableView.callTradeBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.FolioPos.tableView.callTradeBook.activated.connect(lambda: tradeBookRequested(self, 'FolioPosition'))

    self.NetPos.tableView.callTradeBook = QShortcut(QKeySequence('F8'), self.NetPos)
    self.NetPos.tableView.callTradeBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.NetPos.tableView.callTradeBook.activated.connect(lambda: tradeBookRequested(self, 'NetPosition'))

    self.OrderBook.tableView.callTradeBook = QShortcut(QKeySequence('F8'), self.OrderBook)
    self.OrderBook.tableView.callTradeBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.OrderBook.tableView.callTradeBook.activated.connect(lambda: tradeBookRequested(self, 'OrderBook'))

    self.PendingW.tableView.callTradeBook = QShortcut(QKeySequence('F8'), self.PendingW)
    self.PendingW.tableView.callTradeBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.PendingW.tableView.callTradeBook.activated.connect(lambda: tradeBookRequested(self, 'PendingOrder'))

    self.TradeW.tableView.callTradeBook = QShortcut(QKeySequence('F8'), self.PendingW)
    self.PendingW.tableView.callTradeBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.PendingW.tableView.callTradeBook.activated.connect(lambda: tradeBookRequested(self, 'TradeBook'))

    self.snapW.callTradeBook = QShortcut(QKeySequence('F8'), self.snapW)
    self.snapW.callTradeBook.setContext(Qt.WidgetWithChildrenShortcut)
    self.snapW.callTradeBook.activated.connect(lambda: orderBookRequested(self, 'SnapQuote'))

    ##############################

    ############################## 'A'

    self.marketW.tableView.callFolioPos = QShortcut(QKeySequence('Ctrl+F1'), self.marketW)
    self.marketW.tableView.callFolioPos.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.callFolioPos.activated.connect(lambda: FolioPosRequested(self, 'MarketWatch'))

    self.marketWB.tableView.callFolioPos = QShortcut(QKeySequence('Ctrl+F1'), self.marketWB)
    self.marketWB.tableView.callFolioPos.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketWB.tableView.callFolioPos.activated.connect(lambda: FolioPosRequested(self, 'MarketWatch_basic'))

    self.FolioPos.tableView.callFolioPos = QShortcut(QKeySequence('A'), self.FolioPos)
    self.FolioPos.tableView.callFolioPos.setContext(Qt.WidgetWithChildrenShortcut)
    self.FolioPos.tableView.callFolioPos.activated.connect(lambda: FolioPosRequested(self, 'FolioPosition'))

    self.NetPos.tableView.callFolioPos = QShortcut(QKeySequence('A'), self.NetPos)
    self.NetPos.tableView.callFolioPos.setContext(Qt.WidgetWithChildrenShortcut)
    self.NetPos.tableView.callFolioPos.activated.connect(lambda: FolioPosRequested(self, 'NetPosition'))

    self.OrderBook.tableView.callFolioPos = QShortcut(QKeySequence('A'), self.OrderBook)
    self.OrderBook.tableView.callFolioPos.setContext(Qt.WidgetWithChildrenShortcut)
    self.OrderBook.tableView.callFolioPos.activated.connect(lambda: FolioPosRequested(self, 'OrderBook'))

    self.PendingW.tableView.callFolioPos = QShortcut(QKeySequence('A'), self.PendingW)
    self.PendingW.tableView.callFolioPos.setContext(Qt.WidgetWithChildrenShortcut)
    self.PendingW.tableView.callFolioPos.activated.connect(lambda: FolioPosRequested(self, 'PendingOrder'))

    self.TradeW.tableView.callFolioPos = QShortcut(QKeySequence('A'), self.PendingW)
    self.PendingW.tableView.callFolioPos.setContext(Qt.WidgetWithChildrenShortcut)
    self.PendingW.tableView.callFolioPos.activated.connect(lambda: FolioPosRequested(self, 'TradeBook'))

    self.snapW.callFolioPos = QShortcut(QKeySequence('A'), self.snapW)
    self.snapW.callFolioPos.setContext(Qt.WidgetWithChildrenShortcut)
    self.snapW.callFolioPos.activated.connect(lambda: FolioPosRequested(self, 'SnapQuote'))

    ##############################
    ############################## 'Ctrl+Z'

    self.marketW.tableView.callFolioPos = QShortcut(QKeySequence('Ctrl+Z'), self.marketW)
    self.marketW.tableView.callFolioPos.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.callFolioPos.activated.connect(lambda: multiOrdersRequested(self, 'MarketWatch'))

    self.marketWB.tableView.callFolioPos = QShortcut(QKeySequence('Ctrl+Z'), self.marketWB)
    self.marketWB.tableView.callFolioPos.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketWB.tableView.callFolioPos.activated.connect(lambda: multiOrdersRequested(self, 'MarketWatch_basic'))
####################
    # self.marketW.tableView.callOrderbook = QShortcut(QKeySequence('Ctrl+F3'), self)
    # self.marketW.tableView.callOrderbook.setContext(Qt.WidgetWithChildrenShortcut)
    # self.marketW.tableView.callOrderbook.activated.connect(lambda:requestOrderbook(self))
    #
    # self.marketW.tableView.callTradebook = QShortcut(QKeySequence('F8'), self)
    # self.marketW.tableView.callTradebook.setContext(Qt.WidgetWithChildrenShortcut)
    # self.marketW.tableView.callTradebook.activated.connect(lambda:requestTradebook(self))


    #
    # self.marketWB.tableView.callPendind = QShortcut(QKeySequence('F3'), self)
    # self.marketWB.tableView.callPendind.setContext(Qt.WidgetWithChildrenShortcut)
    # self.marketWB.tableView.callPendind.activated.connect(lambda:requestPendingWindow(self))
    #
    # self.marketWB.tableView.callOrderbook = QShortcut(QKeySequence('Ctrl+F3'), self)
    # self.marketWB.tableView.callOrderbook.setContext(Qt.WidgetWithChildrenShortcut)
    # self.marketWB.tableView.callOrderbook.activated.connect(lambda:requestOrderbook(self))
    #
    # self.marketWB.tableView.callTradebook = QShortcut(QKeySequence('F8'), self)
    # self.marketWB.tableView.callTradebook.setContext(Qt.WidgetWithChildrenShortcut)
    # self.marketWB.tableView.callTradebook.activated.connect(lambda:requestTradebook(self))
    #


    # self.FolioPos.tableView.callPendind = QShortcut(QKeySequence('F3'), self)
    # self.FolioPos.tableView.callPendind.setContext(Qt.WidgetWithChildrenShortcut)
    # self.FolioPos.tableView.callPendind.activated.connect(lambda:requestPendingWindow(self))
    #
    # self.FolioPos.tableView.callOrderbook = QShortcut(QKeySequence('Ctrl+F3'), self)
    # self.FolioPos.tableView.callOrderbook.setContext(Qt.WidgetWithChildrenShortcut)
    # self.FolioPos.tableView.callOrderbook.activated.connect(lambda:requestOrderbook(self))
    #
    # self.FolioPos.tableView.callTradebook = QShortcut(QKeySequence('F8'), self)
    # self.FolioPos.tableView.callTradebook.setContext(Qt.WidgetWithChildrenShortcut)
    # self.FolioPos.tableView.callTradebook.activated.connect(lambda:requestTradebook(self))



    # self.NetPos.tableView.callPendind = QShortcut(QKeySequence('F3'), self)
    # self.NetPos.tableView.callPendind.setContext(Qt.WidgetWithChildrenShortcut)
    # self.NetPos.tableView.callPendind.activated.connect(lambda:requestPendingWindow(self))

    # self.NetPos.tableView.callOrderbook = QShortcut(QKeySequence('Ctrl+F3'), self)
    # self.NetPos.tableView.callOrderbook.setContext(Qt.WidgetWithChildrenShortcut)
    # self.NetPos.tableView.callOrderbook.activated.connect(lambda:requestOrderbook(self))
    #
    # self.NetPos.tableView.callTradebook = QShortcut(QKeySequence('F8'), self)
    # self.NetPos.tableView.callTradebook.setContext(Qt.WidgetWithChildrenShortcut)
    # self.NetPos.tableView.callTradebook.activated.connect(lambda:requestTradebook(self))
    #

######################

    # self.callNetPos = QShortcut(QKeySequence('Alt+F6'), self)
    # self.callNetPos.activated.connect(lambda: requestNetPos(self))
    #
    #
    #




    self.marketW.tableView.shortcut_snapQuote = QShortcut(QKeySequence('F5'), self.marketW.tableView)
    self.marketW.tableView.shortcut_snapQuote.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.shortcut_snapQuote.activated.connect(lambda:snapQuoteRequested(self,'MarketWatch'))

    self.marketWB.tableView.shortcut_snapQuote = QShortcut(QKeySequence('F5'), self.marketWB.tableView)
    self.marketWB.tableView.shortcut_snapQuote.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketWB.tableView.shortcut_snapQuote.activated.connect(lambda:snapQuoteRequested(self,'MarketWatch_basic'))

    self.buyW.PlaceOrdSc1 = QShortcut(QKeySequence('Return'), self.buyW)
    self.buyW.PlaceOrdSc1.activated.connect(lambda:BuyWindow.support.placeOrd(self))
    self.buyW.PlaceOrdSc2 = QShortcut(QKeySequence('Enter'), self.buyW)
    self.buyW.PlaceOrdSc2.activated.connect(lambda:BuyWindow.support.placeOrd(self))
    self.buyW.pbSubmit.clicked.connect(lambda:BuyWindow.support.placeOrd(self))
    # multi modification
    self.multiModifyW.PlaceOrdSc1 = QShortcut(QKeySequence('Return'), self.multiModifyW)
    self.multiModifyW.PlaceOrdSc1.activated.connect(self.multiModifyW.modifyMultipleOrders)
    self.multiModifyW.PlaceOrdSc2 = QShortcut(QKeySequence('Enter'), self.multiModifyW)
    self.multiModifyW.PlaceOrdSc2.activated.connect(self.multiModifyW.modifyMultipleOrders)

    self.sellW.PlaceOrdSc1 = QShortcut(QKeySequence('Return'), self.sellW)
    self.sellW.PlaceOrdSc1.activated.connect(lambda:SellWindow.support.placeOrd(self))
    self.sellW.PlaceOrdSc2 = QShortcut(QKeySequence('Enter'), self.sellW)
    self.sellW.PlaceOrdSc2.activated.connect(lambda:SellWindow.support.placeOrd(self))
    self.sellW.pbSubmit.clicked.connect(lambda:SellWindow.support.placeOrd(self))