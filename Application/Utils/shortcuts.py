from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt
from Application.Utils.openRequstedWindow import *
from Application.Utils.scriptSearch import *
from Application.Views import BuyWindow


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






    self.marketW.tableView.callPendind = QShortcut(QKeySequence('F3'), self)
    self.marketW.tableView.callPendind.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.callPendind.activated.connect(lambda:requestBuyWindow(self))

    self.marketW.tableView.shortcut_snapQuote = QShortcut(QKeySequence('F5'), self.marketW.tableView)
    self.marketW.tableView.shortcut_snapQuote.setContext(Qt.WidgetWithChildrenShortcut)
    self.marketW.tableView.shortcut_snapQuote.activated.connect(lambda:snapQuoteRequested(self))

    self.buyW.PlaceOrdSc1 = QShortcut(QKeySequence('Return'), self.buyW)
    self.buyW.PlaceOrdSc1.activated.connect(lambda:BuyWindow.support.placeOrd(self))
    self.buyW.PlaceOrdSc2 = QShortcut(QKeySequence('Enter'), self.buyW)
    self.buyW.PlaceOrdSc2.activated.connect(lambda:BuyWindow.support.placeOrd(self))
    self.buyW.pbSubmit.clicked.connect(lambda:BuyWindow.support.placeOrd(self))