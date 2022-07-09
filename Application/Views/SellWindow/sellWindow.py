
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Application.Views.titlebar import tBar

import qdarkstyle

import traceback
import sys
import logging
import requests
from os import path, getcwd
from threading import Thread
from Theme.dt2 import dt1
#
# from Application.configReader import readConfig_All,config_location



class Ui_SellW(QMainWindow):
    sgTmSubd=pyqtSignal(dict)
    sgTmUnSubd=pyqtSignal(dict)
    sgAppOrderID =  pyqtSignal(int)


    ######################### All Initializers Here ##########################
    def __init__(self,parent=None):
        super(Ui_SellW, self).__init__(parent=None)
        self.ticksize = 0.05
        self.lotsize = 0

        self.clist = []

        try:
            loc11 = getcwd().split('Application')
            ui_login =path.join(loc11[0], 'Resourses','UI','sellWindow.ui')
            uic.loadUi(ui_login, self)
            #

            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
            self.setWindowFlags(flags)


            self.title = tBar('')
            self.headerFrame.layout().addWidget(self.title, 0, 0)
            ############## Set StyleSheet ######################
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)
            ################### End Section Here ###############

            # self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source,market_data_appKey,market_data_secretKey,ia_appKey,ia_secretKey,clist,DClient,broadcastMode = readConfig_All()

            self.slist = ['MANUAL']
            self.isFresh =True
            self.modifyOIDList = []

            self.quitSc = QShortcut(QKeySequence('Esc'), self)
            self.quitSc.activated.connect(self.hide)


            self.Buysc = QShortcut(QKeySequence('F1'), self)
            self.Buysc.activated.connect(self.hide)

            self.setAllShortcuts()
            self.connectAllSlots()

            self.uid = 100000
            self.leQty.setFocus(True)
            self.title.sgPoss.connect(self.movWin)


        except:
            print(config_location,'in sell wind')
            print(traceback.print_exc())
            logging.error(sys.exc_info())
    ####################################### Ends Here ##############################

    ######################################## All Functions Here ########################
    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)

    def connectAllSlots(self):
        self.bt_min.clicked.connect(self.hide)
        self.bt_close.clicked.connect(self.hide)



    def showWindow(self, exchange,token, price, qty, symbol, instrument, exp, strk, opt, freezeQty,lotSize,tickSize):
        self.leToken.setText(str(token))
        self.leInsType.setText(instrument)
        self.leSymbol.setText(symbol)
        self.cbExp.clear()
        self.cbExp.addItem(exp)
        self.cbStrike.clear()
        self.cbStrike.addItem(strk)
        self.cbOpt.clear()
        self.cbOpt.addItem(opt)
        self.leMLT.setText('1')

        self.leQty.setText(str(lotSize))
        self.leRate.setText(price)



        self.lotsize=lotSize
        self.ticksize =tickSize
        self.freezeQty = freezeQty

        self.show()




    def placeOrd(self):
        try:
            token  = self.leToken.text()
            orderType = self.cbOrdType.currentText()
            if (self.isFresh):
                th1=Thread(target=self.PlaceOrder,args=(token, orderType , "SELL", self.leQty.text(),
                                self.leRate.text(), self.uid, self.cbValidity.currentText(), self.leDiscQ.text(),
                                self.leTrigger.text(), self.cbEx.currentText(),self.leClient.text()))
                th1.start()
            else:
                if(len(self.modifyOIDList)>1):
                    for i in self.modifyOIDList:
                        th1 = Thread(target=self.modify,
                                     args=(i, self.cbOrdType.currentText(), i[1], self.leDiscQ.text(),
                                           self.leRate.text(), self.leTrigger.text(), self.cbStretegyNo.currentText(),
                                           self.leClient.text()))
                        th1.start()
                    else:
                        th1 = Thread(target=self.modify,
                                     args=(self.modifyOIDListp[0][0], self.cbOrdType.currentText(), self.leQty.text(),
                                           self.leDiscQ.text(),
                                           self.leRate.text(), self.leTrigger.text(), self.cbStretegyNo.currentText(),
                                           self.leClient.text()))
                        th1.start()
            self.hide()
        except:
            print(sys.exc_info())

    def PlaceOrder(self, instrument_id, ordertype, orderSide, orderQuantity, limitPrice, orderUniqueIdentifier,tim,disc, triggerPrice, exch,clientid):
        try:
            uid1 = self.cbStretegyNo.currentText()

            if(limitPrice=='0'):
                ordertype = 'MARKET'

            if(self.source != 'TWSAPI'):

                payload_order_place = {
                    "exchangeSegment": exch,
                    "exchangeInstrumentID": int(instrument_id),
                    "productType": "NRML",
                    "orderType": ordertype,
                    "orderSide": orderSide,
                    "timeInForce": tim,
                    "disclosedQuantity": int(disc),
                    "orderQuantity": int(orderQuantity),
                    "limitPrice": float(limitPrice) ,
                    "stopPrice": float(triggerPrice),
                    "orderUniqueIdentifier": uid1
                }

            else:
                payload_order_place = {
                "clientID": clientid,
                    "exchangeSegment": exch,
                    "exchangeInstrumentID": int(instrument_id),
                    "productType": "NRML",
                    "orderType": ordertype,
                    "orderSide": orderSide,
                    "timeInForce": tim,
                    "disclosedQuantity": int(disc),
                    "orderQuantity": int(orderQuantity),
                    "limitPrice": float(limitPrice) ,
                    "stopPrice": float(triggerPrice),
                    "orderUniqueIdentifier": uid1
                }

            print(payload_order_place)
            place_order_url = requests.post(self.URL+'/interactive/orders', json=payload_order_place,
                                            headers=self.IAheaders)
            data_p_order = place_order_url.json()
            self.sgAppOrderID.emit(data_p_order['result']['AppOrderID'])

            if(data_p_order['type']!='success'):
                print(data_p_order)
        except:
            print(sys.exc_info(),'@PlaceOrder')
    ############################ Ends Here ############################

    def refresh_config(self):
        self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source,market_data_appKey,market_data_secretKey,ia_appKey,ia_secretKey,clist,DClient,broadcastMode = readConfig_All()


    def dec_v(self):
        if(self.leQty.hasFocus()==True):
            if (self.leQty.text()!='0'):
                self.leQty.setText(str(int(self.leQty.text())-self.lotsize))
        if(self.leRate.hasFocus()==True):
            if (self.leRate.text()!='0'):
                aa='%.2f'%(float(self.leRate.text())-float(self.ticksize))
                self.leRate.setText(aa)


    def inc_v(self):
        if(self.leQty.hasFocus()==True):

            self.leQty.setText(str(int(self.leQty.text())+self.lotsize))
        if(self.leRate.hasFocus()==True):
            aa = '%.2f' % (float(self.leRate.text()) + float(self.ticksize))
            self.leRate.setText(aa)



    def dec_v1(self):
        # a=QtWidgets.QLineEdit()
        # a.hasFocus()
        if(self.leQty.hasFocus()==True):
            if (self.leQty.text()!='0'):
                self.leQty.setText(str(int(self.leQty.text())-self.lotsize))
        if(self.leRate.hasFocus()==True):
            if (self.leRate.text()!='0'):
                aa='%.2f'%(float(self.leRate.text())-float(self.ticksize)*20)
                self.leRate.setText(aa)


    def inc_v1(self):
        if(self.leQty.hasFocus()==True):

            self.leQty.setText(str(int(self.leQty.text())+self.lotsize))
        if(self.leRate.hasFocus()==True):
            aa = '%.2f' % (float(self.leRate.text()) + float(self.ticksize)*20)
            self.leRate.setText(aa)



    def set2List(self):
        self.cbCli.setCurrentIndex(1)
    def set2Market(self):
        self.cbOrdType.setCurrentIndex(1)

    def setAllShortcuts(self):
        self.scMarket = QShortcut(QKeySequence('Alt+M'), self)
        self.scMarket.activated.connect(self.set2Market)
        self.leRate.sc_up = QShortcut(QKeySequence('Up'), self.leRate)
        self.leRate.sc_up.setContext(Qt.WidgetWithChildrenShortcut)
        self.leRate.sc_up.activated.connect(self.inc_v)
        self.leRate.sc_up1 = QShortcut(QKeySequence('Ctrl+Up'), self.leRate)
        self.leRate.sc_up1.setContext(Qt.WidgetWithChildrenShortcut)
        self.leRate.sc_up1.activated.connect(self.inc_v1)
        self.leRate.sc_down = QShortcut(QKeySequence('Down'), self.leRate)
        self.leRate.sc_down.activated.connect(self.dec_v)
        self.leRate.sc_down.setContext(Qt.WidgetWithChildrenShortcut)
        self.leRate.sc_down1 = QShortcut(QKeySequence('Ctrl+Down'), self.leRate)
        self.leRate.sc_down1.activated.connect(self.dec_v1)
        self.leRate.sc_down1.setContext(Qt.WidgetWithChildrenShortcut)
        self.leQty.sc_up = QShortcut(QKeySequence('Up'), self.leQty)
        self.leQty.sc_up.setContext(Qt.WidgetWithChildrenShortcut)
        self.leQty.sc_up.activated.connect(self.inc_v)
        self.leQty.sc_up1 = QShortcut(QKeySequence('Ctrl+Up'), self.leQty)
        self.leQty.sc_up1.setContext(Qt.WidgetWithChildrenShortcut)
        self.leQty.sc_up1.activated.connect(self.inc_v)

        self.leQty.sc_down = QShortcut(QKeySequence('Down'), self.leQty)
        self.leQty.sc_down.activated.connect(self.dec_v)
        self.leQty.sc_down.setContext(Qt.WidgetWithChildrenShortcut)

        self.leQty.sc_down1 = QShortcut(QKeySequence('Ctrl+Down'), self.leQty)
        self.leQty.sc_down1.activated.connect(self.dec_v)
        self.leQty.sc_down1.setContext(Qt.WidgetWithChildrenShortcut)
        self.PlaceOrdSc1 = QShortcut(QKeySequence('Return'), self)
        self.PlaceOrdSc1.activated.connect(self.placeOrd)
        self.PlaceOrdSc2 = QShortcut(QKeySequence('Enter'), self)
        self.PlaceOrdSc2.activated.connect(self.placeOrd)
        self.pbSubmit.clicked.connect(self.placeOrd)


    def modify(self,apporderid,orderType,qty,discQty,Mprice,MStopPrice,OrderUniqueID,clientId):
        try:
            if(self.source !='TWSAPI'):

                modify_payload = {
                    "appOrderID": apporderid,
                    "modifiedProductType": "NRML",
                    "modifiedOrderType": orderType,
                    "modifiedOrderQuantity": qty,
                    "modifiedDisclosedQuantity": discQty,
                    "modifiedLimitPrice": Mprice,
                    "modifiedStopPrice": MStopPrice,
                    "modifiedTimeInForce": "DAY",
                    "orderUniqueIdentifier": OrderUniqueID
                }
            else:
                modify_payload = {
                    "clientID": clientId,
                    "appOrderID": apporderid,
                    "modifiedProductType": "NRML",
                    "modifiedOrderType": orderType,
                    "modifiedOrderQuantity": qty,
                    "modifiedDisclosedQuantity": discQty,
                    "modifiedLimitPrice": Mprice,
                    "modifiedStopPrice": MStopPrice,
                    "modifiedTimeInForce": "DAY",
                    "orderUniqueIdentifier": OrderUniqueID
                }

            print(modify_payload)
            # modify_payload1 = json.dumps(modify_payload,cls=NumpyEncoder)
            place_order_url = requests.put(self.apiip + '/interactive/orders', json=modify_payload,
                                            headers=self.iheaders)
            data_p_order = place_order_url.json()
            print('Order Modification request',data_p_order)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_SellW()
    form.show()
    sys.exit(app.exec_())