import traceback
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Resourses.icons import icons_rc
from os import path, getcwd
import qdarkstyle
from Theme.dt2 import dt1
from Application.Views.titlebar import tBar
import time
from Application.Views.Models.tableOrder import ModelOB
from Application.Utils.configReader import *
from Application.Views.BuyWindow.buyWindow import Ui_BuyW
from Application.Views.SellWindow.sellWindow import Ui_SellW
import json
import requests
import logging
import sys
import numpy as np

import threading

class PendingOrder(QMainWindow):
    ################################# Intialization Here ##################################################
    def __init__(self,parent=None):
        super(PendingOrder, self).__init__()

        loc1 = getcwd().split('Application')
        ui_login = os.path.join (loc1[0] , 'Resourses','UI','pendingOrderBook.ui')
        uic.loadUi(ui_login, self)
        self.setStyleSheet(dt1)
        self.createObjects()
        self.subToken = 0
        self.isSnapQuotOpen = False
        self.lastSerialNo = 0

        self.leSearch = QLineEdit()
        self.leSearch.setPlaceholderText('Search')
        self.leSearch.setFixedWidth(150)
        self.leSearch.textChanged.connect(self.filterData)

        self.pbClear = QPushButton()
        self.pbClear.setText('Clear')
        self.pbClear.clicked.connect(self.clearFilter)

        self.toolBar.addWidget(self.leSearch)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.pbClear)

        self.pbShowSQ.clicked.connect(self.showSnapWin)
        self.filterStr = ''
        self.modifyOIDList =[]
        self.sortOrder = 0
        self.sortColumn = 0
        self.tableView.horizontalHeader().sectionClicked.connect(self.llp)

        self.createShortcuts()
        self.createSlots()


    def createObjects(self):
        self.tables_details()
        self.buyw = Ui_BuyW(self)
        self.sellw = Ui_SellW(self)
        self.buyw.cbStretegyNo.clear()
        self.sellw.cbStretegyNo.clear()

    def llp(self,a):
        # print(a,self.smodel.sortOrder(),self.smodel.sortColumn())
        self.sortOrder = self.smodelO.sortOrder()
        self.sortColumn =self.smodelO.sortColumn()
        self.smodelO.setFilterKeyColumn(self.sortColumn)


    def createShortcuts(self):
        self.tableView.shortcut_modify = QShortcut(QKeySequence('Shift+F2'), self.tableView)
        self.tableView.shortcut_modify.setContext(Qt.WidgetWithChildrenShortcut)
        self.tableView.shortcut_modify.activated.connect(self.ModifyOrder)

        self.tableView.slideRifgtSM = QShortcut(QKeySequence('Esc'), self.tableView)
        self.tableView.slideRifgtSM.setContext(Qt.WidgetWithChildrenShortcut)
        self.tableView.slideRifgtSM.activated.connect(self.hideSnapWin)
        #
        # self.tableView.shortcut_modify = QShortcut(QKeySequence('Shift+F2'), self.tableView)
        # self.tableView.shortcut_modify.setContext(Qt.WidgetWithChildrenShortcut)
        # self.tableView.shortcut_modify.activated.connect(self.ModifyOrder)

        self.tableView.delt = QShortcut(QKeySequence('Del'), self.tableView)
        self.tableView.delt.setContext(Qt.WidgetWithChildrenShortcut)
        self.tableView.delt.activated.connect(self.CancelOrder)



    def createSlots(self):
        # self.bt_min.clicked.connect(self.hide)
        # self.bt_close.clicked.connect(self.hide)
        self.tableView.doubleClicked.connect(self.snp)

    def cancel_order(self,apporderid, uniqueidentifier,clientid):
        try:
            param1={'appOrderId':apporderid,'orderUniqueIdentifier':uniqueidentifier}
            cancle_url = self.URL + "/interactive/orders?appOrderID=" + str(apporderid)+"&orderUniqueIdentifier="+str(uniqueidentifier) + "&clientID=" + clientid

            cancle_order_r = requests.delete(cancle_url,headers = self.IAheaders)
            print(cancle_order_r.text)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])
    def CancelOrder(self):

        try:
            a = self.tableView.selectedIndexes()
            b = int(a[8].data())

            print('datatype b',type(b))

            d = a[0].data()
            print('b %s , d %s'%(b,d))
            try:
                c = a[15].data()
            except:

                print(traceback.print_exc())
                c = ' '
            if (c == ''):
                c = ' '
            # print(b,c)
            th1=threading.Thread(target=self.cancel_order,args=(b,c,d))
            th1.start()
            # self.cancel_order(b, c)
            # th1=threading.Thread(self.cancel_order,args=(b,c))
            # th1.start()
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())


    def snp(self):
        # print(self.tableView.selectedIndexes()[1].data())
        self.subToken = int(self.tableView.selectedIndexes()[1].data())
        self.showSnapWin()


    def sock1502(self,a):
        # print(b)
        b = a.split(',')
        # print('b',b)
        token = int(b[0].split('_')[1])
        if(token==self.subToken):
            for i in b:
                # print(i[:2])
                if(i[:2]=='ai'):
                    ask = i.split(':')[1].split('|')
                elif(i[:2]=='bi'):
                    bids = i.split(':')[1].split('|')

            # bids = b[17].split(':')[1].split('|')
            # ask = b[16].split(':')[1].split('|')
            # print('bids',bids)
            # print('ask',ask)

            self.bq1.setText(bids[1])
            self.bq2.setText(bids[5])
            self.bq3.setText(bids[9])
            self.bq4.setText(bids[13])
            self.bq5.setText(bids[17])

            self.bp1.setText(bids[2])
            self.bp1.setText(bids[6])
            self.bp1.setText(bids[10])
            self.bp1.setText(bids[14])
            self.bp1.setText(bids[18])


            self.nb1.setText(bids[3])
            self.nb2.setText(bids[7])
            self.nb3.setText(bids[11])
            self.nb4.setText(bids[15])
            self.nb5.setText(bids[19])

            self.sq1.setText(ask[1])
            self.sq2.setText(ask[5])
            self.sq3.setText(ask[9])
            self.sq4.setText(ask[13])
            self.sq5.setText(ask[17])

            self.sp1.setText(ask[2])
            self.sp1.setText(ask[6])
            self.sp1.setText(ask[10])
            self.sp1.setText(ask[14])
            self.sp1.setText(ask[18])

            self.ns1.setText(ask[3])
            self.ns2.setText(ask[7])
            self.ns3.setText(ask[11])
            self.ns4.setText(ask[15])
            self.ns5.setText(ask[19])


    def ModifyOrder(self):
        RO = self.ApiOrder.shape[1]
        # print('RO',RO)
        a=self.tableView.selectedIndexes()
        # print(len(a))
        noOfRecords = int(len(a) / RO)
        # print('noOfRecords',noOfRecords)
        token = a[1].data()
        # print('token',token)
        bs=a[7].data()
        # qty = 0
        ordType = a[9].data()
        cli = a[0].data()
        folioNo = a[15].data()
        orderId =a[8].data()

        print('modify order folio',folioNo)
        # print('ordType',ordType)
        self.modifyOIDList = []
        qty = 0
        for i in range(noOfRecords):
            baseCount = i*RO
            itoken=a[(baseCount+1)].data()
            ibs=a[(baseCount+7)].data()
            icli=a[(baseCount)].data()
            iordType=a[(baseCount+9)].data()
            ifolioNo = a[baseCount+15].data()
            iorderId = a[baseCount+8].data()
            if(itoken!=token):

                print('all token not same')
                return False
            elif(ibs != bs):
                print('all orderSide not same')
                return False
            elif(icli != cli):
                print('all client not same')
                return False
            elif (iordType != ordType):
                print('all orderType not same')
                return False
            elif (ifolioNo != folioNo):
                print('all folioNo not same')
                return False
            else:
                qty = qty +  int(a[baseCount+12].data())
                self.modifyOIDList.append([iorderId,int(a[baseCount+12].data())])

        if(bs=='Buy'):
            self.buyw.isFresh = False
            if(self.buyw.isVisible()):
                self.buyw.hide()
            if(self.sellw.isVisible()):
                self.sellw.hide()

            self.buyw.leToken.setText(token)
            # self.InsType.setText()
            self.buyw.leSymbol.setText(a[3].data())
            self.buyw.cbExp.clear()
            self.buyw.cbExp.addItem(a[4].data())
            self.buyw.cbStrike.clear()
            self.buyw.cbStrike.addItem(a[5].data())
            self.buyw.cbOpt.clear()
            self.buyw.cbOpt.addItem(a[6].data())
            self.buyw.leQty.setText(str(qty))
            self.buyw.leRate.setText(a[13].data())
            self.buyw.leTrigger.setText(a[14].data())
            self.buyw.leClient.setText(a[0].data())
            self.buyw.modifyOIDList =self.modifyOIDList
            self.buyw.cbStretegyNo.addItem(folioNo)
            # self.buyw.cbStretegyNo.setCurrentText(folioNo)
            self.buyw.show()

        else:
            if (self.sellw.isVisible()):
                self.sellw.hide()

            if(self.buyw.isVisible()):
                self.buyw.hide()

            self.sellw.leToken.setText(token)
            # self.InsType.setText()
            self.sellw.leSymbol.setText(a[3].data())
            self.sellw.cbExp.clear()
            self.sellw.cbExp.addItem(a[4].data())
            self.sellw.cbStrike.clear()
            self.sellw.cbStrike.addItem(a[5].data())
            self.sellw.cbOpt.clear()
            self.sellw.cbOpt.addItem(a[6].data())
            self.sellw.leQty.setText(str(qty))
            self.sellw.leRate.setText(a[13].data())
            self.sellw.leTrigger.setText(a[14].data())
            self.sellw.cbStretegyNo.addItem(folioNo)

            # self.sellw.cbStretegyNo.setCurrentText(folioNo)

            self.sellw.leClient.setText(a[0].data())
            self.sellw.modifyOIDList =self.modifyOIDList

            self.sellw.show()




    def refresh_config(self):
        try:
            self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source ,self.MDKey,self.MDSecret,self.IAKey,self.IASecret,self.client_list,DClient,broadcastMode= readConfig_All()
            self.buyw.refresh_config()
            self.sellw.refresh_config()
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])




    def shwSnapWin(self):
        if(self.isSnapQuotOpen==False):
            self.animssq4 = QPropertyAnimation(self.snapQ, b"minimumWidth")
            self.animssq4.setDuration(50)
            self.animssq4.setStartValue(0)
            self.animssq4.setEndValue(400)
            self.animssq4.start()
            self.isSnapQuotOpen = True

            self.unSubscription_feed(self.subToken)

    def hideSnapWin(self):

        print('hideSnapwin', self.isSnapQuotOpen)
        if(self.isSnapQuotOpen==True):
            self.animssq3 = QPropertyAnimation(self.snapQ, b"minimumWidth")
            self.animssq3.setDuration(50)
            self.animssq3.setStartValue(400)
            self.animssq3.setEndValue(0)
            self.animssq3.start()
            self.isSnapQuotOpen = False
            self.unSubscription_feed(self.subToken)

    def showSnapWin(self):
        if(self.isSnapQuotOpen==False):
            self.animssq1 = QPropertyAnimation(self.snapQ, b"minimumWidth")
            self.animssq1.setDuration(50)
            self.animssq1.setStartValue(0)
            self.animssq1.setEndValue(400)
            self.animssq1.start()
            self.isSnapQuotOpen = True
            self.subscription_feed(self.subToken)

        else:
            self.animssq2 = QPropertyAnimation(self.snapQ, b"minimumWidth")
            self.animssq2.setDuration(50)
            self.animssq2.setStartValue(400)
            self.animssq2.setEndValue(0)
            self.animssq2.start()
            self.isSnapQuotOpen = False
            self.unSubscription_feed(self.subToken)

    def tables_details(self):
        try:
            self.ApiOrder = np.empty((5000,23),dtype=object)
            self.heads = ['ClientID',
                  'ExchangeInstrumentID', 'Instrument','Symbol','Expiry','Strike_price',
                  'C/P','OrderSide', 'AppOrderID', 'OrderType','OrderStatus',
                'OrderQuantity', 'LeavesQuantity', 'OrderPrice','OrderStopPrice','OrderUniqueIdentifier',
                  'OrderGeneratedDateTime','ExchangeTransactTime','CancelRejectReason','Exchange','Instrument',
                          'AvgPrice', 'Qty1']

            #############################################################################################################

            #############################################
            self.modelO = ModelOB(self.ApiOrder,self.heads)
            self.smodelO = QSortFilterProxyModel()
            self.smodelO.setSourceModel(self.modelO)
            self.tableView.setModel(self.smodelO)
            self.smodelO.setDynamicSortFilter(False)
            self.smodelO.setFilterCaseSensitivity(False)
            self.smodelO.setFilterKeyColumn(1)

            self.tableView.horizontalHeader().setSectionsMovable(True)
            self.tableView.verticalHeader().setSectionsMovable(True)
            # self.tableView.setStyleSheet(
            #     'background-color: rgb(50, 50, 50);selection-background-color: transparent;color: rgb(245, 245, 245);')
            self.tableView.setDragDropMode(self.tableView.InternalMove)
            # self.tableView.horizontalHeader().setStyleSheet('color : black')
            self.tableView.setDragDropOverwriteMode(False)
            # self.tableView.clicked.connect(self.tvs6)
            self.tableView.verticalHeader().setMaximumSectionSize(8)
            self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)

        except:
            logging.error(sys.exc_info()[1])


    def updateGetApi(self,data):
        pass
        # try:
        #     # print('updateGetApi',data)
        #     self.ApiOrder = data
        #     self.modelO = ModelOB(self.ApiOrder,self.heads)
        #     self.smodelO.setSourceModel(self.modelO)
        #     self.tableView.setModel(self.smodelO)
        #     self.rcount = self.ApiOrder.shape[0]
        # except:
        #     print(traceback.print_exc())
        #     logging.error(sys.exc_info())

    def updateSocketOB(self,ord):
        try:


            print('ord',type(ord),ord)
            print(self.ApiOrder)


            appOrderId = ord[0][8]
            # print('appOrderId',appOrderId)
            fltr = np.asarray([int(ord[0][8]),str(ord[0][8])])
            if (ord[0][10] == 'New'):
                self.ApiOrder[self.lastSerialNo,:]=ord

                self.lastSerialNo += 1
                self.modelO.lastSerialNo += 1
                self.modelO.insertRows()
                self.modelO.rowCount()
                self.smodelO.setFilterFixedString(self.filterStr)

                ind = self.modelO.index(0, 0)
                ind1 = self.modelO.index(0,1)
                self.modelO.dataChanged.emit(ind, ind1)

                print(self.ApiOrder)

            elif (ord[0][10] == 'Rejected'):
                newary = np.empty((1,22),dtype=object)
                x= np.where(self.ApiOrder[:, 8] == appOrderId)
                self.ApiOrder[x, :] = newary
                self.lastSerialNo -= 1
                self.modelO.lastSerialNo -= 1
                self.modelO._data = self.ApiOrder
                self.modelO.DelRows()
                self.modelO.rowCount()
                self.modelO.modelReset()
                self.smodelO.setFilterFixedString(self.filterStr)
                ind = self.modelO.index(0, 0)
                ind1 = self.modelO.index(0, 1)
                self.modelO.dataChanged.emit(ind, ind1)


            elif(ord[0][10] in ['Cancelled','PendingCancel','Filled']):
                newary = np.empty((1,22),dtype=object)
                x= np.where(self.ApiOrder[:, 8] == appOrderId)
                self.ApiOrder[x, :] = newary
                self.lastSerialNo -= 1
                self.modelO.lastSerialNo -= 1
                self.modelO._data = self.ApiOrder
                self.modelO.DelRows()
                self.modelO.rowCount()
                self.modelO.modelReset.emit()
                self.smodelO.setFilterFixedString(self.filterStr)

                ind = self.modelO.index(0, 0)
                ind1 = self.modelO.index(0, 1)
                self.modelO.dataChanged.emit(ind, ind1)

                ######################################################################################################
            elif (ord[0][10] == 'PartiallyFilled'):
                try:
                    self.ApiOrder[np.in1d(self.ApiOrder[:, 8], fltr), [10,12]] = [ord[10],ord[12]]
                except:
                    print(sys.exc_info())
                ind = self.modelO.index(0, 0)
                ind1 = self.modelO.index(0, 1)
                self.modelO.dataChanged.emit(ind, ind1)
            elif (ord[0][10] == 'Replaced'):
                self.ApiOrder[np.in1d(self.ApiOrder[:, 8], fltr), [10,11,12,13]] = [ord[10],ord[11],ord[12],ord[13]]
                ind = self.modelO.index(0, 0)
                ind1 = self.modelO.index(0, 1)
                self.modelO.dataChanged.emit(ind, ind1)

            self.modelO.setDta(self.ApiOrder)
            ind = self.modelO.index(0, 0)
            ind1 = self.modelO.index(0, 1)
            self.modelO.dataChanged.emit(ind, ind1)

        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())

    def subscription_feed(self,token, seg=2,  streamType = 1502):
        try:
            sub_url = self.URL + '/marketdata/instruments/subscription'
            payloadsub = {"instruments": [{"exchangeSegment": seg,"exchangeInstrumentID": token}],"xtsMessageCode": streamType}
            # payloadsub = {"instruments": [{"exchangeSegment": 1,"exchangeInstrumentID": 26000}],"xtsMessageCode": 1501}
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("POST", sub_url, data=payloadsubjson, headers=self.MDheaders)

            logging.info(req.text)
            resp = req.json()
            # print(resp)
            #'Instrument subscribed successfully!',
            #"Instrument Already Subscribed !"
            if(resp['description']=='Instrument subscribed successfully!'):
                # print(json.loads(resp['result']['listQuotes'][0]))
                # print(json.loads(resp['result']['listQuotes'][0])['Bids'][0]['Size'])
                packet =json.loads(resp['result']['listQuotes'][0])
                bids= packet['Bids']
                asks= packet['Asks']
                # print(bids)
                # print(asks)
            elif(resp['description']=='Instrument Already Subscribed !'):
                packet = self.getQuote(token)
                bids = packet['Bids']
                asks = packet['Asks']
                # print(bids)
                # print(asks)


            #######################################################################

            self.bq1.setText(str(bids[0]['Size']))
            self.bq2.setText(str(bids[1]['Size']))
            self.bq3.setText(str(bids[2]['Size']))
            self.bq4.setText(str(bids[3]['Size']))
            self.bq5.setText(str(bids[4]['Size']))

            self.bp1.setText(str(bids[0]['Price']))
            self.bp2.setText(str(bids[1]['Price']))
            self.bp3.setText(str(bids[2]['Price']))
            self.bp4.setText(str(bids[3]['Price']))
            self.bp5.setText(str(bids[4]['Price']))

            self.nb1.setText(str(bids[0]['TotalOrders']))
            self.nb2.setText(str(bids[1]['TotalOrders']))
            self.nb3.setText(str(bids[2]['TotalOrders']))
            self.nb4.setText(str(bids[3]['TotalOrders']))
            self.nb5.setText(str(bids[4]['TotalOrders']))

            self.sq1.setText(str(asks[0]['Size']))
            self.sq2.setText(str(asks[1]['Size']))
            self.sq3.setText(str(asks[2]['Size']))
            self.sq4.setText(str(asks[3]['Size']))
            self.sq5.setText(str(asks[4]['Size']))

            self.sp1.setText(str(asks[0]['Price']))
            self.sp2.setText(str(asks[1]['Price']))
            self.sp3.setText(str(asks[2]['Price']))
            self.sp4.setText(str(asks[3]['Price']))
            self.sp5.setText(str(asks[4]['Price']))

            self.ns1.setText(str(asks[0]['TotalOrders']))
            self.ns2.setText(str(asks[1]['TotalOrders']))
            self.ns3.setText(str(asks[2]['TotalOrders']))
            self.ns4.setText(str(asks[3]['TotalOrders']))
            self.ns5.setText(str(asks[4]['TotalOrders']))
        #######################################################################

            if('subscribed successfully' in req.text or 'Already Subscribed' in req.text ):
                pass
            else:
                logging.error(req.text)

            ####################### database working passage deleted if required retrive from backup ##################
        except:
            print(req.text)
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())



    def unSubscription_feed(self,token, seg=2,  streamType = 1502):
        try:
            sub_url = self.URL + '/marketdata/instruments/subscription'
            payloadsub = {"instruments": [{"exchangeSegment": seg,"exchangeInstrumentID": token}],"xtsMessageCode": streamType}
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("PUT", sub_url, data=payloadsubjson, headers=self.MDheaders)

            logging.info(req.text)
            print(req.text)

            if('subscribed successfully' in req.text or 'Already Subscribed' in req.text ):
                pass
            else:
                logging.error(req.text)
            ####################### database working passage deleted if required retrive from backup ##################
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())

    def getQuote(self, token,seg=2,streamType=1502):
        try:
            quote_url = self.URL + '/marketdata/instruments/quotes'
            payload_quote = {"instruments": [{"exchangeSegment": seg,"exchangeInstrumentID": token}],"xtsMessageCode": streamType,"publishFormat": "JSON"}
            quote_json = json.dumps(payload_quote)
            data = requests.request("POST", quote_url, data=quote_json, headers=self.MDheaders)
            # print(data.text)
            data1 = data.json()
            d = data1['result']['listQuotes'][0]
            d = json.loads(d)
            # ltp = [d['Touchline']['BidInfo']['Price'],d['Touchline']['AskInfo']['Price']]
            return d

        except:
            print(sys.exc_info(),'get Quote')

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




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = PendingOrder()
    form.show()

    sys.exit(app.exec_())