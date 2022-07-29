import numpy as np
from Application.Views import BuyWindow
from Application.Views import SellWindow
from Application.Views import SellWindow
from Application.Views.multiModification import  Ui_MultiModification
import traceback
from Application.Utils.supMethods import showPendingW, showOrderBookW, showTradeBookW, showFolioPosW

def orderBookRequested(self,superClass):
    print("Ordrbook inside",superClass )

    if (superClass == 'MarketWatch'):
        token = int(self.marketW.tableView.selectedIndexes()[0].data())
        exchange = self.marketW.tableView.selectedIndexes()[1].data()
    elif (superClass == 'MarketWatch_basic'):
        token = int(self.marketWB.tableView.selectedIndexes()[0].data())
        exchange = self.marketWB.tableView.selectedIndexes()[1].data()
    elif (superClass == 'PendingOrder'):
        token = int(self.PendingW.tableView.selectedIndexes()[2].data())
        exchange = self.PendingW.tableView.selectedIndexes()[19].data()

    elif (superClass == 'OrderBook'):
        token = ''
    elif (superClass == 'NetPosition'):
        token = int(self.NetPos.tableView.selectedIndexes()[3].data())
        exchange = self.NetPos.tableView.selectedIndexes()[2].data()
    elif (superClass == 'FolioPosition'):
        token = int(self.FolioPos.tableView.selectedIndexes()[5].data())
        exchange = self.FolioPos.tableView.selectedIndexes()[4].data()
    elif (superClass == 'SnapQuote'):
        token = self.snapW.Token
        exchange = self.snapW.exchange

    showOrderBookW(self, token)

def FolioPosRequested(self,superClass):
    print("FolioPosRequested",superClass )

    if (superClass == 'MarketWatch'):
        token = int(self.marketW.tableView.selectedIndexes()[0].data())
        exchange = self.marketW.tableView.selectedIndexes()[1].data()
    elif (superClass == 'MarketWatch_basic'):
        token = int(self.marketWB.tableView.selectedIndexes()[0].data())
        exchange = self.marketWB.tableView.selectedIndexes()[1].data()
    elif (superClass == 'PendingOrder'):
        token = int(self.PendingW.tableView.selectedIndexes()[2].data())
        exchange = self.PendingW.tableView.selectedIndexes()[19].data()

    elif (superClass == 'OrderBook'):
        token = int(self.OrderBook.tableView.selectedIndexes()[2].data())
        exchange = self.OrderBook.tableView.selectedIndexes()[19].data()
    elif (superClass == 'NetPosition'):
        token = int(self.NetPos.tableView.selectedIndexes()[3].data())
        exchange = self.NetPos.tableView.selectedIndexes()[2].data()
    elif (superClass == 'FolioPosition'):
        token = ''
    elif (superClass == 'SnapQuote'):
        token = self.snapW.Token
        exchange = self.snapW.exchange

    showFolioPosW(self, token)

def tradeBookRequested(self,superClass):
    print("Tradebook inside",superClass )

    if (superClass == 'MarketWatch'):
        token = int(self.marketW.tableView.selectedIndexes()[0].data())
        exchange = self.marketW.tableView.selectedIndexes()[1].data()
    elif (superClass == 'MarketWatch_basic'):
        token = int(self.marketWB.tableView.selectedIndexes()[0].data())
        exchange = self.marketWB.tableView.selectedIndexes()[1].data()
    elif (superClass == 'PendingOrder'):
        token = int(self.PendingW.tableView.selectedIndexes()[2].data())
        exchange = self.PendingW.tableView.selectedIndexes()[19].data()
    elif (superClass == 'OrderBook'):
        token = int(self.OrderBook.tableView.selectedIndexes()[2].data())
        exchange = self.OrderBook.tableView.selectedIndexes()[19].data()
    elif (superClass == 'TradeBook'):
        token = ''
    elif (superClass == 'NetPosition'):
        token = int(self.NetPos.tableView.selectedIndexes()[3].data())
        exchange = self.NetPos.tableView.selectedIndexes()[2].data()
    elif (superClass == 'FolioPosition'):
        token = int(self.FolioPos.tableView.selectedIndexes()[5].data())
        exchange = self.FolioPos.tableView.selectedIndexes()[4].data()
    elif (superClass == 'SnapQuote'):
        token = self.snapW.Token
        exchange = self.snapW.exchange

    showTradeBookW(self, token)

def folioRequested(self,superClass):
    if (superClass == 'MarketWatch'):
        token = int(self.marketW.tableView.selectedIndexes()[0].data())
        exchange = self.marketW.tableView.selectedIndexes()[1].data()
    elif (superClass == 'MarketWatch_basic'):
        token = int(self.marketWB.tableView.selectedIndexes()[0].data())
        exchange = self.marketWB.tableView.selectedIndexes()[1].data()
    elif (superClass == 'PendingOrder'):
        # self.PendingW.smodelO.setFilterFixedString('')
        token = ''
        exchange = self.PendingW.tableView.selectedIndexes()[19].data()
    elif (superClass == 'NetPosition'):
        token = int(self.NetPos.tableView.selectedIndexes()[3].data())
        exchange = self.NetPos.tableView.selectedIndexes()[2].data()
    elif (superClass == 'FolioPosition'):
        token = int(self.FolioPos.tableView.selectedIndexes()[5].data())
        exchange = self.FolioPos.tableView.selectedIndexes()[4].data()
    elif (superClass == 'SnapQuote'):
        token = self.snapW.Token
        exchange = self.snapW.exchange

    showPendingMW(self, token)

def pendingOrderRequested(self,superClass):
    if (superClass == 'MarketWatch'):
        token = int(self.marketW.tableView.selectedIndexes()[0].data())
        exchange = self.marketW.tableView.selectedIndexes()[1].data()
    elif (superClass == 'MarketWatch_basic'):
        token = int(self.marketWB.tableView.selectedIndexes()[0].data())
        exchange = self.marketWB.tableView.selectedIndexes()[1].data()
    elif (superClass == 'PendingOrder'):
        # self.PendingW.smodelO.setFilterFixedString('')
        token = ''
        #exchange = self.PendingW.tableView.selectedIndexes()[19].data()
    elif (superClass == 'NetPosition'):
        token = int(self.NetPos.tableView.selectedIndexes()[3].data())
        exchange = self.NetPos.tableView.selectedIndexes()[2].data()
    elif (superClass == 'FolioPosition'):
        token = int(self.FolioPos.tableView.selectedIndexes()[5].data())
        exchange = self.FolioPos.tableView.selectedIndexes()[4].data()
    elif (superClass == 'SnapQuote'):
        token = self.snapW.Token
        exchange = self.snapW.exchange

    showPendingW(self, token)

def snapQuoteRequested(self,superClass):


    if(self.snapW.isVisible()):
        self.snapW.hideWindow()

    if(superClass == 'MarketWatch'):
        token = int(self.marketW.tableView.selectedIndexes()[0].data())
        exchange = self.marketW.tableView.selectedIndexes()[1].data()
    elif(superClass=='MarketWatch_basic'):
        token = int(self.marketWB.tableView.selectedIndexes()[0].data())
        exchange = self.marketWB.tableView.selectedIndexes()[1].data()
    elif (superClass == 'PendingOrder'):
        token = int(self.PendingW.tableView.selectedIndexes()[2].data())
        exchange = self.PendingW.tableView.selectedIndexes()[19].data()
    elif (superClass == 'NetPosition'):
        token = int(self.NetPos.tableView.selectedIndexes()[3].data())
        exchange = self.NetPos.tableView.selectedIndexes()[2].data()
    elif (superClass == 'FolioPosition'):
        token = int(self.FolioPos.tableView.selectedIndexes()[5].data())
        exchange = self.FolioPos.tableView.selectedIndexes()[4].data()



    print("Token = :",token!=self.snapW.token, token, self.snapW.token)
    if(token!=self.snapW.token):
        self.snapW.Token = token
        self.ins_details = self.fo_contract[token-35000]
        lua = self.ins_details
        print("LUaa:::::", lua)
        self.snapW.cbEx.setCurrentText(lua[0])
        self.snapW.cbSg.setCurrentText(lua[1])
        self.snapW.cbIns.setCurrentText(lua[5])
        self.snapW.cbSym.setCurrentText(lua[3])
        self.snapW.cbExp.setCurrentText(lua[6])
        self.snapW.cbStrk.setCurrentText(lua[7])
        self.snapW.cbOtype.setCurrentText(lua[8])
        self.snapW.LeToken.setText(str(token))
    else:
        print("----0.0")
        self.snapW.subscription_feed(self.snapW.Token,seg=exchange,streamType=1502)

    if(self.snapW.isVisible()):
        print("----0")
        self.snapW.hideWindow()
    print("----1")
    self.snapW.show()


def requestBuyModification(self,appOrderID, exchange, token, price, orderType, validity, productType,triggerPrice,qty,uid):

    try:
        if(exchange == 'NSEFO'):
            ins_details = self.fo_contract[token-35000]
        else:
            ins_details = self.fo_contract[token]

        instrumentType = ins_details[5]
        symbol = ins_details[3]
        exp = ins_details[6]
        strk = ins_details[7]
        opt = ins_details[8]
        tick = ins_details[10]
        lotSize = ins_details[11]
        max = ins_details[14]
        self.buyW.appOrderIdFprModification = appOrderID
        price = '%.2f' %price
        BuyWindow.support.showWindow(self,exchange,token,price,qty,symbol,instrumentType,exp,strk,opt,max,lotSize,tick, triggerPrice,uid,validity, productType, orderType,False)
        #self.buyW.show()
    except:
        print(traceback.print_exc())

def requestSellModification(self,appOrderID, exchange, token, price, orderType, validity, productType, triggerPrice, qty,uid):
    try:
        if (exchange == 'NSEFO'):
            ins_details = self.fo_contract[token - 35000]
        else:
            ins_details = self.fo_contract[token]

        instrumentType = ins_details[5]
        symbol = ins_details[3]
        exp = ins_details[6]
        strk = ins_details[7]
        opt = ins_details[8]
        tick = ins_details[10]
        lot = ins_details[11]
        max = ins_details[14]
        self.sellW.appOrderIdFprModification = appOrderID
        price = '%.2f' % price
        SellWindow.support.showWindow(self, exchange, token, price, qty, symbol, instrumentType, exp, strk, opt, max,
                                     lot, tick, triggerPrice, uid, validity, productType, orderType, False)
        # self.buyW.show()
    except:
        print(traceback.print_exc())

def requestMultiModification(self, modifyArray):
    try:

        if (modifyArray[0][7] == 'NSEFO'):
            ins_details = self.fo_contract[modifyArray[0][2] - 35000]
        else:
            ins_details = self.fo_contract[modifyArray[0][2]]
        instrumentType = ins_details[5]
        self.multiModifyW.showWindow( modifyArray, instrumentType)
    except:
        print(traceback.print_exc())

def requestBuyWindow(self,sourceClass):

    if(sourceClass == 'MarketWatch'):
        selectedIndexes = self.marketW.tableView.selectedIndexes()

        token = int(selectedIndexes[0].data())
        exchange = selectedIndexes[1].data()
        price = '%.2f' % selectedIndexes[8].data()
    elif(sourceClass == 'MarketWatch_basic'):
        selectedIndexes = self.marketWB.tableView.selectedIndexes()
        print("selectedIndexes:",selectedIndexes[0].data())
        token = int(selectedIndexes[0].data())
        exchange = selectedIndexes[1].data()
        price = '%.2f' % selectedIndexes[8].data()

    elif(sourceClass == 'NetPosition'):
        pass
    elif(sourceClass == 'SnapQuote'):

        token = self.snapW.token
        exchange = self.snapW.exchange
        price = self.snapW.sp1.text()

    elif(sourceClass == 'FolioPosition'):
        pass


    if(exchange == 'NSEFO'):
        ins_details = self.fo_contract[token-35000]
    elif(exchange == 'NSECM'):
        ins_details = self.eq_contract[token]
    elif(exchange == 'NSECD'):
        ins_details = self.cd_contract[token]
    instrumentType = ins_details[5]
    symbol = ins_details[3]
    exp = ins_details[6]
    strk = ins_details[7]
    opt = ins_details[8]
    tick = ins_details[10]
    lot = ins_details[11]
    max = ins_details[14]
    triggerPrice = '0.0'

    BuyWindow.support.showWindow(self,exchange,token,price,lot,symbol,instrumentType,exp,strk,opt,max,lot,tick, triggerPrice)

def requestSellWindow(self,sourceClass):


    if(sourceClass == 'MarketWatch'):
        selectedIndexes = self.marketW.tableView.selectedIndexes()
        token = int(selectedIndexes[0].data())
        exchange = selectedIndexes[1].data()
        price = '%.2f' % selectedIndexes[7].data()

    elif(sourceClass == 'MarketWatch_basic'):
        selectedIndexes = self.marketWB.tableView.selectedIndexes()
        token = int(selectedIndexes[0].data())
        exchange = selectedIndexes[1].data()
        price = '%.2f' % selectedIndexes[7].data()

    elif(sourceClass == 'NetPosition'):
        pass
    elif(sourceClass == 'SnapQuote'):
        token = self.snapW.token
        exchange = self.snapW.exchange
        price = self.snapW.bp1.text()

    elif(sourceClass == 'FolioPosition'):
        pass


    if(exchange == 'NSEFO'):
        ins_details = self.fo_contract[token-35000]
    else:
        ins_details = self.fo_contract[token]

    instrumentType = ins_details[5]
    symbol = ins_details[3]
    exp = ins_details[6]
    strk = ins_details[7]
    opt = ins_details[8]
    tick = ins_details[10]
    lot = ins_details[11]
    max = ins_details[14]

    triggerPrice = '0.0'

    SellWindow.support.showWindow(self,exchange,token,price,lot,symbol,instrumentType,exp,strk,opt,max,lot,tick,triggerPrice)
