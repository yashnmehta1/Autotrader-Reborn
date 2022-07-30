import numpy as np
import traceback
import sys

from Application.Views.basicMWatch import support as basicMarketSupport
from Application.Views.MarketWatch import support as marketSupport
import datatable as dt
from Application.Services.Xts.Api.servicesIA import PlaceOrder

def updateMultiOrderstable(self, data):
    try:
        j = 0
        self.table[:, :] = ''
        for i in data:
            self.table[j, :] = i
            print(self.model._data)
            ind = self.model.index(0, 0)
            ind1 = self.model.index(0, 31)

            self.model.dataChanged.emit(ind, ind1)
            j += 1

    except:
        print(traceback.print_exc(), sys.exc_info())


def showWindow(self, superClass):
    try:
        if (self.multiOrders.isVisible()):
            self.multiOrders.hideWindow()

        indexes =[]
        marketwatchSupportRef = [];
        marketwatchRef = [];
        serialNo = 0
        if (superClass == 'MarketWatch'):
            marketwatchSupportRef = marketSupport
            indexes = self.marketW.tableView.selectedIndexes()
            print("Indexes : ",indexes )
            serialNo = int(indexes[30].data())
            marketwatchRef = self.marketW
        elif (superClass == 'MarketWatch_basic'):
            marketwatchSupportRef =basicMarketSupport
            indexes = self.marketWB.tableView.selectedIndexes()
            print("Indexes : ", indexes)
            serialNo = int(indexes[22].data())
            marketwatchRef = self.marketWB

        selectedLen = len(indexes)
        noOfSelectedRecord = int(selectedLen / self.marketW.visibleColumns)
        statingPoint = 0
        multiOrders = self.multiOrders
        table = np.zeros((noOfSelectedRecord,7),dtype=object)
        j =0
        if(noOfSelectedRecord < 2 | noOfSelectedRecord > 4):
            print("Selected record should be grater than 1 & less than 5")
        else :
            for i in range(noOfSelectedRecord):
                print("11111111111111111111")
                clientId = marketwatchSupportRef.getClientId(marketwatchRef,serialNo)
                print("clienid:", clientId)
                exchange = marketwatchSupportRef.getExchange(marketwatchRef,serialNo)
                symbol = marketwatchSupportRef.getSymbol(marketwatchRef,serialNo)
                token = marketwatchSupportRef.getToken(marketwatchRef, serialNo)
                expiry = marketwatchSupportRef.getExpiry(marketwatchRef, serialNo)
                print("EXPO ------------------>", expiry)
                strikePrice = marketwatchSupportRef.getStrikePrice(marketwatchRef,serialNo)
                print("strikePrice ------------------>", strikePrice)
                optionType = marketwatchSupportRef.getOptionType(marketwatchRef,serialNo)
                ltp = marketwatchSupportRef.getInstrumentType(marketwatchRef,serialNo)

                table[j,:]=dt.Frame([[exchange],[token],[symbol],[strikePrice],[expiry],[optionType],[ltp]]).to_numpy()
                j+=1

            updateMultiOrderstable(self.multiOrders,table)
            multiOrders.show()

    except:
        print(traceback.print_exc(), sys.exc_info())

def executeMultipleOrders(self):

    try :
        ########### pending
        print("Table : ",self.multiOrders.table)
        for i in self.multiOrders.table:
            print("Multi order exec : ", i)
            clientId = self.multiOrders.cbClient.currentText()
            orderSide = self.multiOrders.cbOrderType.currentText().upper()
            leQty = int(self.multiOrders.leQty.text())
            uid = self.multiOrders.leFolioNo.text()
            print("&&&&&&&&&& -> ", i[0])
            print("----------------Len",len(i[0]))
            if(len(i[0]) > 0):
                PlaceOrder(self,i[0],clientId,i[1],orderSide,leQty,0,'DAY',0,0,uid,'MARKET')
                print("execured:")

    except:
      print(traceback.print_exc(), sys.exc_info())

def updateLTP(self, token,ltp):
    try:
        self.table[np.where(self.table[:,1]==token),6] =ltp
        ind = self.model.index(0, 0)
        ind1 = self.model.index(0, 31)
        self.model.dataChanged.emit(ind, ind1)

    except:
        print(traceback.print_exc(), sys.exc_info())