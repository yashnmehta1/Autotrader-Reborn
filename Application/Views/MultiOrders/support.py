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
        # if (orderType == 'StopLimit'):
        #     self.leModifiedTriggerPrice.setEnabled(True)
        # else:
        #     self.leModifiedTriggerPrice.setEnabled(False)
        indexes =[]
        marketwatchSupportRef = [];
        marketwatchRef = [];
        serialNoIndex = 0
        if (superClass == 'MarketWatch'):
            marketwatchSupportRef = marketSupport
            indexes = self.marketW.tableView.selectedIndexes()
            serialNoIndex = 30
            marketwatchRef = self.marketW
        elif (superClass == 'MarketWatch_basic'):
            marketwatchSupportRef =basicMarketSupport
            indexes = self.marketWB.tableView.selectedIndexes()
            serialNoIndex = 22
            marketwatchRef = self.marketWB

        selectedLen = len(indexes)
        print("selectedLen:", selectedLen)
        print("self.marketW.visibleColumns:", marketwatchRef.visibleColumns)
        noOfSelectedRecord = int(selectedLen / marketwatchRef.visibleColumns)
        statingPoint = 0
        multiOrders = self.multiOrders
        table = np.zeros((noOfSelectedRecord,7),dtype=object)
        print("noOfSelectedRecord:::::::::::", noOfSelectedRecord)
        j =0
        if(noOfSelectedRecord < 2 ):
            print("Selected record should be grater than 1")
        elif (noOfSelectedRecord > 4):
            print("Selected record should be  less than 5")
        else :
            for i in range(noOfSelectedRecord):
                print("::::: I :: ", i)
                serialNoIndex = 30 + statingPoint
                serialNo =  (indexes[serialNoIndex].data())
                clientId = marketwatchSupportRef.getClientId(marketwatchRef,serialNo)

                exchange = marketwatchSupportRef.getExchange(marketwatchRef,serialNo)
                symbol = marketwatchSupportRef.getSymbol(marketwatchRef,serialNo)

                token = marketwatchSupportRef.getToken(marketwatchRef, serialNo)
                expiry = marketwatchSupportRef.getExpiry(marketwatchRef, serialNo)

                strikePrice = marketwatchSupportRef.getStrikePrice(marketwatchRef,serialNo)

                optionType = marketwatchSupportRef.getOptionType(marketwatchRef,serialNo)
                ltp = marketwatchSupportRef.getInstrumentType(marketwatchRef,serialNo)

                table[j,:]=dt.Frame([[exchange],[token],[symbol],[strikePrice],[expiry],[optionType],[ltp]]).to_numpy()
                j+=1
                statingPoint += marketwatchRef.visibleColumns
            uniqueSymbol = np.unique(table[:, 2])
            print("uniqueSymbol : ", uniqueSymbol)
            if (uniqueSymbol.size != 1):
                print("Symbol must be same. Please select same symbol records")

            else:
                updateMultiOrderstable(self.multiOrders,table)
                multiOrders.show()

    except:
        print(traceback.print_exc(), sys.exc_info())

def executeMultipleOrders(self):

    try :
        ########### pending
       # print("Table : ",self.multiOrders.table)
        leQty = int(self.multiOrders.leQty.text())
        if( leQty < 1):
            print("Please enter correct qty")
        else:
            sliceLoopIndex = 0
            leSlice = int(self.multiOrders.leSlice.text())

            if (self.multiOrders.table[0][0] == 'NSEFO'):
                ins_details = self.fo_contract[self.multiOrders.table[0][1] - 35000]
            else:
                ins_details = self.fo_contract[self.multiOrders.table[0][1]]

            lotSize = int(ins_details[11])
            print("lotsize:",lotSize)

            sliceLot = 0
            if(leSlice == 0 ):
                sliceLoopIndex = 1
                sliceLot = leQty
            else:
                sliceLot = int(lotSize * leSlice)
            print("slice:", leSlice)
            counter = 1
            while(leQty > 0):
                print("leSlice : ", leSlice)
                if (leSlice <= sliceLoopIndex):
                    sliceLot = leQty

                if(leSlice <= sliceLoopIndex | leQty < sliceLot):
                    sliceLot = leQty

                print("sliceLot:", sliceLot)

                for i in self.multiOrders.table:
                    clientId = self.multiOrders.cbClient.currentText()
                    orderSide = self.multiOrders.cbOrderType.currentText().upper()
                    uid = self.multiOrders.leFolioNo.text()
                    token = i[1]

                    if(len(i[0]) > 0):
                        PlaceOrder(self,i[0],clientId,token,orderSide,sliceLot,0,'DAY',0,0,uid,'MARKET')

                leQty -=sliceLot
                #leQty =0
                print("after slice :", leQty)
                print("sliceLoopIndex :", sliceLoopIndex)
                print("############# :", counter)
                sliceLoopIndex +=1
        self.multiOrders.hideWindow()

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