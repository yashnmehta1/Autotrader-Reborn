from PyQt5.QtCore import QObject,QFile,pyqtSignal,pyqtSlot,Qt,QSortFilterProxyModel,QTimer
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import *
from PyQt5 import uic
from os import path, getcwd
import qtpy
import qdarkstyle
import sys
import pandas as pd
import datatable as dt
import numpy  as np
import requests
import json

from Application.Views.BuyWindow.buyWindow import Ui_BuyW
from Application.Views.SellWindow.sellWindow import Ui_SellW
from Application.Views.SnapQuote.snapQuote import Ui_snapQ
from Application.Utils.dbConnection import  *
from Application.Utils.configReader import readConfig_All
from Application.Views.Models.tableFP import ModelPosition
from Application.Utils.createTables import tables_details_fp
from Theme.dt2 import dt1
import logging



class ProxyModel (QSortFilterProxyModel): #Custom Proxy Model
    def __init__(self):
        super(ProxyModel,self).__init__()
        self.onlyPoss = False

    def filterAcceptsRow(self, row, parent):
        if(self.onlyPoss == True):
            if(self.sourceModel().index(row, 7, parent).data() != 0 ):
                return True
            else:
                return False
        else:
            return True

class FolioPosition(QMainWindow):
    # sgTmSubd=pyqtSignal(dict)
    sgTMTM=pyqtSignal(str)
    sgCallPOrderBook = pyqtSignal(str)
    sgCallTB = pyqtSignal(int)

    def __init__(self):
        super(FolioPosition, self).__init__()
        try:

            self.onlyPoss = False
            self.list1 = []
            self.filterStr = ''
            self.DayNet = 'NET'
            self.sortColumnD=0
            self.sortOrderD=0
            self.sortColumn=0
            self.sortOrder=0

            self.folioList = ['MANUAL']

            # self.contract_df = load_contract1()

            self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source,self.MDKey,self.MDSecret,self.IAKey,self.IASecret,self.client_list,DClient,broadcastMode = readConfig_All()
            #####################################################################

            loc1 = getcwd().split('Application')
            ui_login = os.path.join(loc1[0] , 'Resourses','UI','folioPosition.ui')
            uic.loadUi(ui_login, self)


            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)
            tables_details_fp(self)
            # self.CreateToolBar()
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def changeDayNet(self):
        if(self.rb1.isChecked()):
            self.DayNet = 'DAY'
            self.tableView.setModel(self.smodelFPD)

        elif(self.rb2.isChecked()):
            self.DayNet = 'NET'

            self.tableView.setModel(self.smodelFP)
            self.rcount = self.Apipos.shape[0]

    def orderRaise(self):
        token = int(self.tableView.selectedIndexes()[3].data())
        self.sgCallPOrderBook.emit(str(token))

    def showTB(self):
        token = int(self.tableView.selectedIndexes()[3].data())
        self.sgCallTB.emit(token)


    def filtr(self):
        try:
            self.smodelFP.setFilterFixedString(self.listView.selectedIndexes()[0].data())
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def CreateToolBar(self):
        try:
            self.cbFolio = QComboBox()
            self.cbFolio.setMinimumWidth(150)

            self.toolBar.addWidget(self.cbFolio)


        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def setOnlyPosFlag(self):
        try:
            print('in setOnlyPosFlag ')
            self.onlyPoss = self.opencheckbox.isChecked()
            self.smodelFP.onlyPoss = self.onlyPoss
            self.smodelFP.setFilterFixedString('')

        except:
            print(traceback.print_exc())
        # ind = self.modelFP.index(0, 0)
        # ind1 = self.modelFP.index(0, 1)
        # self.smodelFP.layoutChanged.emit()
        # self.smodelFP.filterAcceptsRow()

    def rightClickMenu(self,position):
        try:
            a=(self.tableView.selectedIndexes()[0].data())
            menu = QMenu()
            squareAction = menu.addAction("Square")
            # cancelAction = menu.addAction("Cancel")
            action = menu.exec_(self.tableView.mapToGlobal(position))
            if action == squareAction:
                abc=self.tableView.selectedIndexes()
                noOfcolumnsinNetPoss = self.Apipos.shape[1]

                lent=int((len(abc))/noOfcolumnsinNetPoss)
                print('lent',lent)
                for i in range(lent):

                    token = abc[1 + (noOfcolumnsinNetPoss*i)].data()
                    qty = int(abc[7 + (noOfcolumnsinNetPoss*i)].data())
                    Maxqty = int(abc[13 + (noOfcolumnsinNetPoss*i)].data())

                    print(token,qty)

                    if(qty>0):
                        absQty = abs(qty)

                        orderSide = 'SELL'
                        while absQty > Maxqty :

                            self.PlaceOrder(token,orderSide,Maxqty,0)
                            absQty = absQty - Maxqty
                        self.PlaceOrder(token, orderSide, absQty, 0)

                    elif(qty<0):
                        absQty = abs(qty)
                        orderSide = 'BUY'
                        while absQty > Maxqty :
                            self.PlaceOrder(token,orderSide,Maxqty,0)
                            absQty = absQty - Maxqty
                        self.PlaceOrder(token, orderSide, absQty, 0)

        except:
            print(sys.exc_info()[1])

    def PlaceOrder(self, instrument_id,  orderSide, orderQuantity,triggerPrice):
        try:
            # print(datetime.datetime.now())
            payload_order_place = {
                "exchangeSegment": "NSEFO",
                "exchangeInstrumentID": int(instrument_id),
                "productType": "NRML",
                "orderType": 'MARKET',
                "orderSide": orderSide,
                "timeInForce": "DAY",
                "disclosedQuantity": 0,
                "orderQuantity": int(orderQuantity),
                "limitPrice": float(0.1),
                "stopPrice": float(triggerPrice),
                "orderUniqueIdentifier": 'MANUAL'
            }
            print(payload_order_place)
            place_order_url = requests.post(self.URL+'/interactive/orders', json=payload_order_place,
                                            headers=self.IAheaders)
            data_p_order = place_order_url.json()
            print(data_p_order)
        except:
            logging.error(sys.exc_info()[1])

    #################################### Ends Here #############################################
    def showBuy(self):

        try:
            token = int(self.tableView.selectedIndexes()[3].data())
            exchange = self.tableView.selectedIndexes()[2].data()
            q = "select * from contract_NFO where Token =%s and Exchange = '%s'" % (token, exchange)
            a = cursor.execute(q)
            for i in a:
                print(i)
                exchange,segment,token1,symbol,instrument,instrument_type,exp,strike,option,cmtoken,tick_size,lot_size,o,multiplier,maxQty = i

            if(self.buyw.isVisible()==True):
                self.buyw.hide()
                self.buyw.show()
            else:
                self.buyw.show()

            self.buyw.leToken.setText(str(token1))
            self.buyw.leInsType.setText(instrument_type)
            self.buyw.leSymbol.setText(symbol)

            self.buyw.cbExp.clear()
            self.buyw.cbOpt.clear()
            self.buyw.cbStrike.clear()


            self.buyw.cbExp.addItem(str(exp))
            self.buyw.cbStrike.addItem(str(strike))
            self.buyw.cbOpt.addItem(option)

            self.buyw.ticksize = tick_size
            self.buyw.lotsize=lot_size
            self.buyw.leQty.setText(str(lot_size))
            self.buyw.leRate.setText(str(self.tableView.selectedIndexes()[11].data()))

            self.buyw.leQty.setFocus(True)
            self.buyw.leQty.selectAll()
            self.buyw.cbOrdType.setCurrentIndex(0)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def showSell(self):
        try:
            token = int(self.tableView.selectedIndexes()[3].data())
            exchange = self.tableView.selectedIndexes()[2].data()
            q = "select * from contract_NFO where Token =%s and Exchange = '%s'" % (token, exchange)
            a = cursor.execute(q)
            for i in a:
                print(i)
                exchange, segment, token1, symbol, instrument, instrument_type, exp, strike, option, cmtoken, tick_size, lot_size, o, multiplier, maxQty = i


            if(self.sellw.isVisible()==True):
                self.sellw.hide()
                self.sellw.show()
            else:
                self.sellw.show()

            self.sellw.leToken.setText(str(token1))
            self.sellw.leInsType.setText(instrument_type)
            self.sellw.leSymbol.setText(symbol)

            self.sellw.cbExp.clear()
            self.sellw.cbStrike.clear()
            self.sellw.cbOpt.clear()


            self.sellw.cbExp.addItem(str(exp))
            self.sellw.cbStrike.addItem(str(strike))
            self.sellw.cbOpt.addItem(option)

            self.sellw.ticksize = tick_size
            self.sellw.lotsize=lot_size
            self.sellw.leQty.setText(str(lot_size))
            self.sellw.leRate.setText(str(self.tableView.selectedIndexes()[11].data()))
            self.sellw.leQty.setFocus(True)
            self.sellw.leQty.selectAll()
            self.sellw.cbOrdType.setCurrentIndex(0)

        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def snapQuoteRequested(self):
        if(self.snapW.isVisible()):
            self.snapW.hide1()

        token = int(self.tableView.selectedIndexes()[3].data())

        if(token!=self.snapW.subToken):

            self.snapW.subToken = token

            fltr = np.asarray([token])
            # fltr = np.asarray([71322])
            lua = self.snapW.Contract_df[np.in1d(self.snapW.Contract_df[:, 2], fltr)]
            # print(lua)

            self.snapW.cbEx.setCurrentText(lua[0][0])
            self.snapW.cbSg.setCurrentText(lua[0][1])
            self.snapW.cbIns.setCurrentText(lua[0][5])
            self.snapW.cbSym.setCurrentText(lua[0][3])
            self.snapW.cbExp.setCurrentText(lua[0][6])
            self.snapW.cbStrk.setCurrentText(lua[0][7])
            self.snapW.cbOtype.setCurrentText(lua[0][8])
            self.snapW.LeToken.setText(str(token))
        else:
            self.snapW.subscription_feed(self.snapW.subToken)


        if(self.snapW.isVisible()):
            self.snapW.hide()
        self.snapW.show()

    def updateGetApi(self,data):
        try:
            # print('update get api netPos',data)
            if(data.size == 0):
                pass
            else:
                self.Apipos = data
                self.modelFP = ModelPosition(self.Apipos,self.heads)
                self.smodelFP.setSourceModel(self.modelFP)
                self.tableView.setModel(self.smodelFP)
            self.rcount = self.Apipos.shape[0]
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())

    def MTM_update(self, newPrice):
        try:
            if(self.Apipos.size != 0):
                ################################ API POS NETWISE ##################################################
                fltr = np.asarray([(newPrice['Token'])])
                lua = self.Apipos[np.in1d(self.Apipos[:, 3], fltr)]
                if (lua.size == 0):
                    pass
                else:
                    mtm = (int(lua[0][9]) * float(newPrice['LTP'])) + float(lua[0][13])
                    self.Apipos[np.in1d(self.Apipos[:, 3], fltr), [10, 11]] = [mtm, newPrice['LTP']]
                ##################################################################################

                ############################### API POS DAYWISE ##########################################
                fltr = np.asarray([(newPrice['Token'])])
                lua = self.ApiposDay[np.in1d(self.ApiposDay[:, 3], fltr)]
                if (lua.size == 0):
                    pass
                else:

                    mtm = (int(lua[0][9]) * float(newPrice['LTP'])) + float(lua[0][13])
                    self.ApiposDay[np.in1d(self.ApiposDay[:, 3], fltr), [10, 11]] = [mtm, newPrice['LTP']]

                ##################################################################################
                if(self.DayNet=='NET'):
                        ind = self.modelFP.index(0, 0)
                        ind1 = self.modelFP.index(0, 1)
                        self.modelFP.dataChanged.emit(ind, ind1)
                else:
                        ind = self.modelFPD.index(0, 0)
                        ind1 = self.modelFPD.index(0, 1)
                        self.modelFPD.dataChanged.emit(ind, ind1)
                try:
                    tmtm = np.sum(self.Apipos[:, 10])
                    self.sgTMTM.emit('%.2f' % (tmtm))
                except:
                    logging.error(sys.exc_info()[1])
                    print(traceback.print_exc())

        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())

    def squareAll(self):
        try:
            xyz = self.Apipos
            for i in self.Apipos:
                print(i)
                if(i[7] !=0):
                    if (i[7] > 0):
                        qty=abs(i[7])
                        maxqty = int(i[13])
                        while(qty>maxqty):
                            self.PlaceOrder(i[1],'SELL',maxqty,1.1)
                            qty = qty - maxqty
                        self.PlaceOrder(i[1],'SELL',qty,1.1)
                    elif (i[7] < 0):
                        maxqty = int(i[13])
                        qty=abs(i[7])
                        while(qty>maxqty):
                            self.PlaceOrder(i[1],'BUY',maxqty,1.1)
                            qty = qty - maxqty
                        self.PlaceOrder(i[1],'BUY',qty,1.1)

        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def refresh_config(self):
        try:
            self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source,self.MDKey,self.MDSecret,self.IAKey,self.IASecret,self.client_list,DClient,broadcastMode = readConfig_All()
        except:
            logging.error(sys.exc_info()[1])

    def subscription_feed(self,token, seg = 'NSEFO', streamType=1501):
        try:
            # print('token %s,seg %s,st %s'%(token,seg,streamType),type(token))
            if(seg == 'NSEFO'):
                segment =2
            elif(seg == 'NSE_CASH'):
                segment =1

            sub_url = self.URL + '/marketdata/instruments/subscription'
            payloadsub = {"instruments": [{"exchangeSegment": segment,"exchangeInstrumentID": token}],"xtsMessageCode": streamType}
            print(payloadsub)
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("POST", sub_url, data=payloadsubjson, headers=self.MDheaders)

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

    def filterData(self,a):
        self.filterStr = a
        self.smodelFP.setFilterFixedString(self.filterStr)
        self.smodelFPD.setFilterFixedString(self.filterStr)

    def clearFilter(self):
        self.filterStr = ''
        self.smodelFPD.setFilterFixedString('')

    def updateGetApitrd(self,trades):
        print("--------------------------------------------------------")
        try:
            for i in trades:
                print('updateGetApitrd',trades)
                token =i[2]
                clientid= i[1]
                exchange= i[20]
                #check token
                ouid = i[15]
                fltr0 = np.asarray([token])
                filteredArray0 = self.table[np.in1d(self.table[:, 5], fltr0)]
                isRecordExist = False
                if (filteredArray0.size != 0):
                    fltr = np.asarray([exchange])
                    filteredArray1 = filteredArray0[np.in1d(filteredArray0[:, 4], fltr)]
                    if (filteredArray1.size != 0):
                        fltr = np.asarray([clientid])
                        filteredArray2 = filteredArray1[np.in1d(filteredArray1[:, 1], fltr)]
                        if (filteredArray2.size != 0):
                            fltr = np.asarray([ouid])
                            filteredArray21 = filteredArray2[np.in1d(filteredArray2[:, 3], fltr)]

                        if (filteredArray21.size != 0):
                            isRecordExist = True

                if(isRecordExist ==False):
                    buyQ = i[18] if(i[18] > 0) else 0
                    buyA = i[17] if(i[18] > 0) else 0.0
                    sellQ = - i[18] if(i[18] < 0) else 0
                    sellA = - i[17] if(i[18] < 0) else 0.0
                    anm = dt.Frame([
                        [i[0]],
                        [i[1]],['Stretegy_type'],[i[15]],[i[20]],[i[2]],
                        [i[3]],[i[4]],[i[5]],[i[6]],[i[7]],
                        [0],[i[18]],[i[18]],[i[19]],[i[17]],
                        [buyQ],[buyA],[sellQ],[sellA],[i[17]],
                        [0.0],[i[20]],[i[21]],[0.0],[self.lastSerialNo],
                        [i[19]]
                                    ]).to_numpy()

                    self.table[self.modelFP.lastSerialNo]=anm
                    self.modelFP.lastSerialNo +=1
                    self.lastSerialNo +=1
                    self.modelFP.rowCount()
                    self.modelFP.insertRows()

                else:
                    serialNo = filteredArray2[0][25]
                    openValue = self.table[serialNo, 24]
                    openQty = self.table[serialNo, 11]
                    dayQ = self.table[serialNo, 12] + i[18]
                    dayAmt = self.table[serialNo, 26] + i[19]
                    netQ = dayQ + openQty
                    netAmt = dayAmt + openValue

                    self.table[serialNo, [12, 13, 14]] = [dayQ, netQ, netAmt]

                ind = self.modelFP.index(0, 0)
                ind1 = self.modelFP.index(0, 26)
                self.modelFP.dataChanged.emit(ind, ind1)

        except:
            print(traceback.print_exc())

    def updateSocketTB(self, trades):
        try:
            for i in trades:
                isRecordExist = False
                token = i[2]
                clientid = i[1]
                exchange = i[20]
                # check token
                fltr0 = np.asarray([token])
                filteredArray0 = self.table[np.in1d(self.table[:, 5], fltr0)]
                isRecordExist = False
                if (filteredArray0.size != 0):
                    fltr = np.asarray([exchange])
                    filteredArray1 = filteredArray0[np.in1d(filteredArray0[:, 4], fltr)]
                    if (filteredArray1.size != 0):
                        fltr = np.asarray([clientid])
                        filteredArray2 = filteredArray1[np.in1d(filteredArray1[:, 1], fltr)]
                        if (filteredArray2.size != 0):
                            isRecordExist = True

                if (isRecordExist == False):
                    buyQ = i[18] if (i[18] > 0) else 0
                    buyA = i[17] if (i[18] > 0) else 0.0
                    sellQ = - i[18] if (i[18] < 0) else 0
                    sellA = - i[17] if (i[18] < 0) else 0.0
                    # openValue =
                    anm = dt.Frame([
                        [i[0]],
                        [i[1]], ['Stretegy_type'], [i[15]], [i[20]], [i[2]],
                        [i[3]], [i[4]], [i[5]], [i[6]], [i[7]],
                        [0], [i[18]], [i[18]], [i[19]], [i[17]],
                        [buyQ], [buyA], [sellQ], [sellA], [i[17]],
                        [0.0], [i[20]], [i[21]], [0.0], [self.lastSerialNo],
                        [i[19]]
                    ]).to_numpy()

                    self.table[self.modelFP.lastSerialNo] = anm
                    self.modelFP.lastSerialNo += 1
                    self.lastSerialNo += 1

                    self.modelFP.rowCount()
                    self.modelFP.insertRows()

                else:
                    serialNo = filteredArray2[0][25]
                    openValue = self.table[serialNo, 24]
                    openQty = self.table[serialNo, 11]
                    dayQ = self.table[serialNo, 12]+i[18]
                    dayAmt = self.table[serialNo, 26]+i[19]
                    netQ = dayQ + openQty
                    netAmt = dayAmt +openValue



                    self.table[serialNo, [12, 13, 14]] = [dayQ, netQ, netAmt]

                ind = self.modelFP.index(0, 0)
                ind1 = self.modelFP.index(0, 26)
                self.modelFP.dataChanged.emit(ind, ind1)

        except:
            print(traceback.print_exc())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = FolioPosition()
    form.show()
    sys.exit(app.exec_())
