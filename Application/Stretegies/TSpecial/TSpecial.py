import traceback

from PyQt5.QtCore import QObject
from Application.Stretegies.TSpecial.Views.addW import addW
from Application.Stretegies.TSpecial.Views.modifyW import modifyW
import numpy as np
import datetime
import time

class logic(QObject):
    ################################# Intialization Here ##################################################
    def __init__(self):
        super(logic, self).__init__()
        # self.createConnection()


    def createObject(self,fo_contract):
        self.fo_contract=fo_contract
        self.addW =addW()
        self.getSymbolList()
        self.addW.cbSymbol.setCurrentText('BANKNIFTY')
        self.symbol = self.addW.cbSymbol.currentText()
        self.getOptionExpiryList()
        self.modifyW = modifyW ()
        self.createConnection()
    def setParameters(self):
        try:
            self.folioName = self.addW.leFolioName.text()
            self.symbol = self.addW.cbSymbol.currentText()
            self.expiry = self.addW.cbExp.currentText()
            self.qty = self.addW.leQty.text()
            self.upperRangeIndex = self.addW.cbUpperRange.currentIndex()
            self.lowerRangeIndex = self.addW.cbLowerRange.currentIndex()
            self.coverType = "Half" if self.addW.rbCHalf.isChecked() else "Full"
            self.strikeDecisionPoint = self.addW.leLowerPoint.text()
            now = datetime.datetime.today()
            date = now.strftime('%Y-%m-%d ')
            self.executionTime = datetime.datetime.strptime(date + self.addW.lt1.text() + ":" +self.addW.lt2.text() + ":" + self.addW.lt3.text() ,'%Y-%m-%d %H:%M:%S')
            print(self.executionTime)
            self.getCETable()
            self.getPETable()
        except:
            print(traceback.print_exc())

    def createConnection(self):
        self.addW.pbApply.clicked.connect(self.setParameters)


    def updateTrade(self):
        pass

    def tradeVarification(self):
        pass

    def updateOrder(self):
        pass

    def orderVarification(self):
        pass

    def checkTrade(self):
        pass

    def initVaribles(self):
        self.isStart = False
        self.isClose = False


        # self.baseSymbol = 'NIFTY'
        # self.strikeInterval = 50
        # self.executionTime = '09:16:00'
        # self.cashToken
        # self.foToken
        # self.lowerPoint = 0.4


    def getSymbolList(self):
        fo_contract1 = self.fo_contract[np.where(self.fo_contract[:, 1] != 'x')]
        uniqueSymbols = np.unique(fo_contract1[:,3])
        self.addW.cbSymbol.addItems(uniqueSymbols)


    def getOptionExpiryList(self):
        fltr = np.asarray([self.symbol])
        filteredarray = self.fo_contract[np.in1d(self.fo_contract[:, 3], fltr)]
        uniqueExp = np.unique(filteredarray[:,6])
        self.addW.cbExp.addItems(uniqueExp)




    def getCETable(self):

        fltr = np.asarray([self.symbol])
        filteredarray = self.fo_contract[np.in1d(self.fo_contract[:, 3], fltr)]
        fltr1 = np.asarray([self.expiry])
        filteredarray1 = filteredarray[np.in1d(filteredarray[:, 6], fltr1)]

        fltr2 = np.asarray(['CE'])
        self.ceTable= filteredarray1[np.in1d(filteredarray1[:, 8], fltr2)]

    def getPETable(self):
        fltr = np.asarray([self.symbol])
        filteredarray = self.fo_contract[np.in1d(self.fo_contract[:, 3], fltr)]
        fltr1 = np.asarray([self.expiry])
        filteredarray1 = filteredarray[np.in1d(filteredarray[:, 6], fltr1)]
        fltr2 = np.asarray(['PE'])
        self.peTable= filteredarray1[np.in1d(filteredarray1[:, 8], fltr2)]

    def getCEList(self,ATMStrike):
        lowerRange= ATMStrike - self.lowerRangeIndex+1*self.strikeDiff
        upperRange


    def getPEList(self):
        pass



    def getExecutionTime(self):
        now = datetime.datetime.today()
        date = now.strftime('%Y-%m-%d ')
        a915 = datetime.datetime.strptime(date + '09:15:00', '%Y-%m-%d %H:%M:%S')
        a920 = datetime.datetime.strptime(date + self.etime, '%Y-%m-%d %H:%M:%S')

        self.timeout1 = int(a920.timestamp()-time.time())*1000
        return self.timeout1

    def getFutureToken(self):
        self.futureToken = self.fo_contract[np.where(self.fo_contract[:, 3] == self.symbol)][0, 17]
    def getStrikeDiff(self):
        self.strikeDiff = self.fo_contract[self.futureToken,36]

