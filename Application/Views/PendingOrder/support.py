import numpy as np
import logging
import sys
import traceback
import threading
from Application.Services.Xts.Api.servicesIA import cancle_order
from PyQt5.QtWidgets import QMessageBox
from Application.Utils.animations import showSnapFrame1
from Application.Utils.openRequstedWindow import requestBuyModification, requestSellModification

def getClientId(self,AppOrderId):
    fltr = np.asarray([AppOrderId])
    clientId = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr),1]
    print('clientId',clientId)
    return clientId[0]

def getFolioNo(self,AppOrderId):
    fltr = np.asarray([AppOrderId])
    folioNo = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr),15]
    print('folioNo',folioNo)
    return folioNo[0]

def getOrderSide(self,AppOrderId):
    fltr = np.asarray([AppOrderId])
    clientId = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr),8]
    print('clientId',clientId)
    return clientId[0]

def getExchange(self,AppOrderId):
    fltr = np.asarray([AppOrderId])
    clientId = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr),19]
    print('clientId',clientId)
    return clientId[0]

def getPrice(self,AppOrderId):
    fltr = np.asarray([AppOrderId])
    clientId = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr),13]
    print('clientId',clientId)
    return clientId[0]

def getToken(self,AppOrderId):
    fltr = np.asarray([AppOrderId])
    clientId = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr),2]
    print('clientId',clientId)
    return clientId[0]

def getOrderType(self,AppOrderId):
    fltr = np.asarray([AppOrderId])
    clientId = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr),9]
    print('clientId',clientId)
    return clientId[0]

def getValidity(self,AppOrderId):
    fltr = np.asarray([AppOrderId])
    clientId = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr),0]
    print('clientId',clientId)
    return 'DAY'

def getProductType(self,AppOrderId):
    fltr = np.asarray([AppOrderId])
    clientId = self.ApiOrder[np.in1d(self.ApiOrder[:, 0], fltr),7]
    print('clientId',clientId)
    return 'NRML'

def CancleOrder(self):
    try:
        indexes = self.tableView.selectedIndexes()
        selectedLen = len(indexes)
        # rows
        noOfSelectedRecord = int (selectedLen / self.visibleColumns )
        print("noOfSelectedRecord:", noOfSelectedRecord)
        startingPoint = 0
        cancledOrderist = []
        for i in range(noOfSelectedRecord):
            AppOrderId = int(indexes[startingPoint + 0].data())
            clientId = getClientId(self,AppOrderId)
            FolioNO = getFolioNo(self,AppOrderId)

            startingPoint += self.visibleColumns
            if (FolioNO == ''):
                FolioNO = ' '
            cancledOrderist.append({'AppOrderId': AppOrderId, 'clientId': clientId, 'FolioNO': FolioNO})
        th1 = threading.Thread(target=cancle_order, args=(self, cancledOrderist,))
        th1.start()
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())


def showSnapQ(self):
    self.subToken = int(self.tableView.selectedIndexes()[1].data())
    showSnapFrame1(self)

# self =  Main.py -  parent class
def ModifyOrder(self):

    try:
        indexes = self.PendingW.tableView.selectedIndexes()
        selectedLen = len(indexes)
        noOfSelectedRecord = int(selectedLen / self.PendingW.visibleColumns)
        if (noOfSelectedRecord == 1):
            AppOrderId = int(indexes[0].data())
            orderSide = getOrderSide(self.PendingW,AppOrderId)
            productType= getProductType(self.PendingW,AppOrderId)
            validity = getValidity(self.PendingW,AppOrderId)
            orderType =  getOrderType(self.PendingW,AppOrderId)
            exchange = getExchange(self.PendingW,AppOrderId)
            price = getPrice(self.PendingW,AppOrderId)
            token = getToken(self.PendingW,AppOrderId)

            if orderSide == 'Buy':
                requestBuyModification(self,AppOrderId, exchange, token, price, orderType, validity, productType)
            else:
                requestSellModification(self, AppOrderId, exchange, token, price, orderType, validity, productType)
        else:
            pass
    except:
        print(traceback.print_exc())
    # RO = self.ApiOrder.shape[1]
    # # print('RO',RO)
    # a = self.tableView.selectedIndexes()
    # # print(len(a))
    # noOfRecords = int(len(a) / RO)
    # # print('noOfRecords',noOfRecords)
    # token = a[1].data()
    # # print('token',token)
    # bs = a[7].data()
    # # qty = 0
    # ordType = a[9].data()
    # cli = a[0].data()
    # folioNo = a[15].data()
    # orderId = a[8].data()
    #
    # print('modify order folio', folioNo)
    # # print('ordType',ordType)
    # self.modifyOIDList = []
    # qty = 0
    # for i in range(noOfRecords):
    #     baseCount = i * RO
    #     itoken = a[(baseCount + 1)].data()
    #     ibs = a[(baseCount + 7)].data()
    #     icli = a[(baseCount)].data()
    #     iordType = a[(baseCount + 9)].data()
    #     ifolioNo = a[baseCount + 15].data()
    #     iorderId = a[baseCount + 8].data()
    #     if (itoken != token):
    #
    #         print('all token not same')
    #         return False
    #     elif (ibs != bs):
    #         print('all orderSide not same')
    #         return False
    #     elif (icli != cli):
    #         print('all client not same')
    #         return False
    #     elif (iordType != ordType):
    #         print('all orderType not same')
    #         return False
    #     elif (ifolioNo != folioNo):
    #         print('all folioNo not same')
    #         return False
    #     else:
    #         qty = qty + int(a[baseCount + 12].data())
    #         self.modifyOIDList.append([iorderId, int(a[baseCount + 12].data())])
    #
    # if (bs == 'Buy'):
    #     self.buyw.isFresh = False
    #     if (self.buyw.isVisible()):
    #         self.buyw.hide()
    #     if (self.sellw.isVisible()):
    #         self.sellw.hide()
    #
    #     self.buyw.leToken.setText(token)
    #     # self.InsType.setText()
    #     self.buyw.leSymbol.setText(a[3].data())
    #     self.buyw.cbExp.clear()
    #     self.buyw.cbExp.addItem(a[4].data())
    #     self.buyw.cbStrike.clear()
    #     self.buyw.cbStrike.addItem(a[5].data())
    #     self.buyw.cbOpt.clear()
    #     self.buyw.cbOpt.addItem(a[6].data())
    #     self.buyw.leQty.setText(str(qty))
    #     self.buyw.leRate.setText(a[13].data())
    #     self.buyw.leTrigger.setText(a[14].data())
    #     self.buyw.leClient.setText(a[0].data())
    #     self.buyw.modifyOIDList = self.modifyOIDList
    #     self.buyw.cbStretegyNo.addItem(folioNo)
    #     # self.buyw.cbStretegyNo.setCurrentText(folioNo)
    #     self.buyw.show()
    #
    # else:
    #     if (self.sellw.isVisible()):
    #         self.sellw.hide()
    #
    #     if (self.buyw.isVisible()):
    #         self.buyw.hide()
    #
    #     self.sellw.leToken.setText(token)
    #     # self.InsType.setText()
    #     self.sellw.leSymbol.setText(a[3].data())
    #     self.sellw.cbExp.clear()
    #     self.sellw.cbExp.addItem(a[4].data())
    #     self.sellw.cbStrike.clear()
    #     self.sellw.cbStrike.addItem(a[5].data())
    #     self.sellw.cbOpt.clear()
    #     self.sellw.cbOpt.addItem(a[6].data())
    #     self.sellw.leQty.setText(str(qty))
    #     self.sellw.leRate.setText(a[13].data())
    #     self.sellw.leTrigger.setText(a[14].data())
    #     self.sellw.cbStretegyNo.addItem(folioNo)
    #
    #     # self.sellw.cbStretegyNo.setCurrentText(folioNo)
    #
    #     self.sellw.leClient.setText(a[0].data())
    #     self.sellw.modifyOIDList = self.modifyOIDList
    #
    #     self.sellw.show()


def ModifyOrderX(self):
    abc = self.tableView.selectedIndexes()
    noOfcolumnsinNetPoss = self.ApiOrder.shape[1]
    lent = int((len(abc)) / noOfcolumnsinNetPoss)

    if (lent == 1):
        orderSide = abc[7].data()

        self.ModifyOrder.radioButton.setChecked(True)
        self.MOappOrderid = abc[8].data()
        symbol = abc[2].data()
        self.MOorderUid = abc[14].data()
        pprice = abc[13].data()

        orderSide = abc[7].data()
        orderType = abc[9].data()
        Pqty = (abc[12].data())
        trigger = abc[16].data()

        self.ModifyOrder.textEdit.clear()
        self.ModifyOrder.textEdit.append(str(self.MOappOrderid))
        if (orderType == 'LIMIT'):
            self.ModifyOrder.comboBox_2.setCurrentIndex(0)
        elif (orderType == 'MARKET'):
            self.ModifyOrder.comboBox_2.setCurrentIndex(1)
        elif (orderType == 'STOPMARKET'):
            self.ModifyOrder.comboBox_2.setCurrentIndex(2)
        self.ModifyOrder.label_5.setText(str(Pqty))
        self.ModifyOrder.label_7.setText(symbol)
        print(pprice)
        print(type(pprice))
        if (float(pprice) == 0.00):
            self.ModifyOrder.lineEdit_2.setText(str(trigger))
        else:
            self.ModifyOrder.lineEdit_2.setText(str(pprice))
        self.ModifyOrder.lineEdit.setText(str(Pqty))
        self.ModifyOrder.lineEdit_11.setText(str(trigger))

        self.ModifyOrder.show()

    elif (lent > 1):
        self.ModifyOrder.radioButton_2.setChecked(True)
        self.ModifyOrder.textEdit.clear()
        psymbol = abc[2].data()
        pside = abc[7].data()
        porderUid = (abc[14].data())
        for i in range(lent):
            symbol = abc[2 + (noOfcolumnsinNetPoss * i)].data()
            side = abc[7 + (noOfcolumnsinNetPoss * i)].data()
            orderUid = int(abc[14 + (noOfcolumnsinNetPoss * i)].data())

            if (psymbol == symbol and pside == side and porderUid == orderUid):
                dd = True
                continue
            else:
                dd = False

        if (dd == True):
            for i in range(lent):
                appOrderid = abc[4 + (noOfcolumnsinNetPoss * i)].data()
                symbol = abc[2 + (noOfcolumnsinNetPoss * i)].data()
                orderUid = int(abc[10 + (noOfcolumnsinNetPoss * i)].data())
        else:
            QMessageBox.about(self, "Error", "Orders of Multiple Instrumentn  can not be modify in bulk")

        self.ModifyOrder.show()

def filterData(self,a):
    self.filterStr = a
    self.smodelO.setFilterFixedString(self.filterStr)

def clearFilter(self):
    self.leSearch.setText('')
    self.smodelO.setFilterFixedString('')
    self.smodelO.setFilterKeyColumn(2)


