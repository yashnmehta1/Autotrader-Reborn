import numpy as np
from Application.Views import BuyWindow
from Application.Views import SellWindow
from Application.Views import SellWindow
from Application.Views.multiModification import  Ui_MultiModification
import traceback



def snapQuoteRequested(self,superClass):


    if(self.snapW.isVisible()):
        self.snapW.hideWindow()

    if(superClass == 'MarketWatch'):
        token = int(self.marketW.tableView.selectedIndexes()[0].data())
    elif(superClass=='MarketWatch_basic'):
        token = int(self.marketWB.tableView.selectedIndexes()[0].data())



    if(token!=self.snapW.token):
        self.snapW.Token = token
        self.ins_details = self.fo_contract[token-35000]
        lua = self.ins_details

        self.snapW.cbEx.setCurrentText(lua[0])
        self.snapW.cbSg.setCurrentText(lua[1])
        self.snapW.cbIns.setCurrentText(lua[5])
        self.snapW.cbSym.setCurrentText(lua[3])
        self.snapW.cbExp.setCurrentText(lua[6])
        self.snapW.cbStrk.setCurrentText(lua[7])
        self.snapW.cbOtype.setCurrentText(lua[8])
        self.snapW.LeToken.setText(str(token))
    else:
        self.snapW.subscription_feed(self.snapW.token)

        if(self.snapW.isVisible()):
            self.snapW.hideWindow()
    self.snapW.show()


def requestBuyModification(self,appOrderID, exchange, token, price, orderType, validity, productType,triggerPrice,qty):

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
        BuyWindow.support.showWindow(self,exchange,token,price,qty,symbol,instrumentType,exp,strk,opt,max,lotSize,tick, triggerPrice,validity, productType, orderType,False)
        #self.buyW.show()
    except:
        print(traceback.print_exc())

def requestSellModification(self,appOrderID, exchange, token, price, orderType, validity, productType, triggerPrice, qty):
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
                                     lot, tick, triggerPrice, validity, productType, orderType, False)
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
        self.multiModifyW.showWindow(self, modifyArray, instrumentType)
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
