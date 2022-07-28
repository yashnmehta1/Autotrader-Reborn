from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from os import path, getcwd

import qdarkstyle
import logging
from Theme.dt2 import  dt1

import sys
import requests
import traceback
import json
import threading
import time
from threading import Thread

from Application.Views.BuyWindow.buyWindow import Ui_BuyW
from Application.Views.SellWindow.sellWindow import Ui_SellW
from Application.Views.titlebar import tBar
from Application.Utils.configReader import *

from Application.Utils.dbConnection import  *
from Application.Views.SnapQuote.scriptbar import *

# from download_master import *

import numpy as np
import platform

class Ui_snapQ(QMainWindow):
    sgTmSubd = pyqtSignal(dict)
    sgTmUnSubd = pyqtSignal(dict)
    sgUnsubs = pyqtSignal(int,int,int)
    #################################### All Initialization Functions Are Here ################################
    def __init__(self,parent=None):
        super(Ui_snapQ, self).__init__(parent=None)
        try:
            #########################################################################
            loc1 = getcwd().split('Application')
            ui_login = os.path.join(loc1[0] , 'Resourses','UI','snapQuote.ui')
            uic.loadUi(ui_login, self)

            osType = platform.system()
            if (osType == 'Darwin'):
                flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            else:
                flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)
            self.setWindowFlags(flags)
            self.title = tBar('snapQuote')
            self.headerFrame.layout().addWidget(self.title, 0, 0)
            self.title.sgPoss.connect(self.movWin)
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)

            #########################################################################
            refresh(self)
            self.initVaribles()

            ############## Set StyleSheet ######################
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            ################### End Section Here ###############
            self.createSlots()


        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def initVaribles(self):
        try:
            self.token = 0
            self.exchange = 'NSEFO'
            # self.ins_details = self.fo_contract[self.token - 35000]
        except:
            print(traceback.print_exc())

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)

    def  createSlots(self):
        try:
            self.quitSc = QShortcut(QKeySequence('Esc'), self)
            self.quitSc.activated.connect(self.hideWindow)

            self.bt_min.clicked.connect(self.hideWindow)
            self.bt_close.clicked.connect(self.hideWindow)

            self.cbEx.currentIndexChanged.connect(lambda :ExchChange(self,  self.cbEx.currentIndex()))
            self.cbSg.currentIndexChanged.connect(lambda :SegmentChange(self, self.cbSg.currentIndex()))
            self.cbIns.currentIndexChanged.connect(lambda :inschange(self, self.cbIns.currentIndex()))
            self.cbSym.currentIndexChanged.connect(lambda :symchange(self, self.cbSym.currentIndex()))
            self.cbExp.currentIndexChanged.connect(lambda :expchange(self, self.cbExp.currentIndex()))
            self.cbStrk.currentIndexChanged.connect(lambda :changestrike(self, self.cbStrk.currentIndex()))
            self.cbOtype.currentIndexChanged.connect(lambda :changeOtype(self, ))
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])



    def showBuy(self):
        try:
            cnt_d = self.t5[0]
            if(self.buyw.isVisible()==True):
                self.buyw.hide()
                self.buyw.show()
            else:
                self.buyw.show()
            self.buyw.leToken.setText(str(self.LeToken.text()))
            self.buyw.leInsType.setText(self.cbIns.currentText())
            self.buyw.leSymbol.setText(self.cbSym.currentText())

            self.buyw.cbExp.clear()
            self.buyw.cbStrike.clear()
            self.buyw.cbOpt.clear()
            #
            self.buyw.cbExp.addItem(str(self.cbExp.currentText()))
            self.buyw.cbStrike.addItem(str(self.cbStrk.currentText()))
            self.buyw.cbOpt.addItem(self.cbOtype.currentText())
            #
            self.buyw.ticksize =  cnt_d[10]
            self.buyw.lotsize= cnt_d[11]
            self.buyw.leQty.setText(str( cnt_d[11]))
            rate = self.sp1.text()

            self.buyw.leRate.setText(rate)
            self.buyw.leQty.setFocus(True)
            self.buyw.leQty.selectAll()
            self.buyw.cbOrdType.setCurrentIndex(0)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def showSell(self):
        try:
            cnt_d = self.t5[0]

            if(self.sellw.isVisible()==True):
                self.sellw.hide()
                self.sellw.show()
            else:
                self.sellw.show()

            self.sellw.leToken.setText(str(self.LeToken.text()))
            self.sellw.leInsType.setText(self.cbIns.currentText())
            self.sellw.leSymbol.setText(self.cbSym.currentText())

            self.sellw.cbExp.clear()
            self.sellw.cbStrike.clear()
            self.sellw.cbOpt.clear()

            self.sellw.cbExp.addItem(str(self.cbExp.currentText()))
            self.sellw.cbStrike.addItem(str(self.cbStrk.currentText()))
            self.sellw.cbOpt.addItem(self.cbOtype.currentText())

            self.sellw.ticksize = cnt_d[10]
            self.sellw.lotsize=cnt_d[11]
            self.sellw.leQty.setText(str(cnt_d[11]))
            rate = self.bp1.text()
            self.sellw.leRate.setText(rate)
            self.sellw.leQty.setFocus(True)
            self.sellw.leQty.selectAll()

            self.sellw.cbOrdType.setCurrentIndex(0)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])


    def updateQuote(self,a):
        try:
            # print('in snqp Quote update quote',a)
            ab=a.split(',')
            # print(ab)
            token1=(ab[0].split('_')[1])
            # print(token1)
            if(int(token1)==self.token):


                b=(ab[1].split('|'))
                s=(ab[2].split('|'))

                try:
                    self.bq1.setText(b[1])
                    self.bp1.setText(b[2])
                    self.nb1.setText(b[3])

                    self.bq2.setText(b[5])
                    self.bp2.setText(b[6])
                    self.nb2.setText(b[7])

                    self.bq3.setText(b[9])
                    self.bp3.setText(b[10])
                    self.nb3.setText(b[11])

                    self.bq4.setText(b[13])
                    self.bp4.setText(b[14])
                    self.nb4.setText(b[15])

                    self.bq5.setText(b[17])
                    self.bp5.setText(b[18])
                    self.nb5.setText(b[19])

                    self.sq1.setText(s[1])
                    self.sp1.setText(s[2])
                    self.ns1.setText(s[3])

                    self.sq2.setText(s[5])
                    self.sp2.setText(s[6])
                    self.ns2.setText(s[7])

                    self.sq3.setText(s[9])
                    self.sp3.setText(s[10])
                    self.ns3.setText(s[11])

                    self.sq4.setText(s[13])
                    self.sp4.setText(s[14])
                    self.ns4.setText(s[15])

                    self.sq5.setText(s[17])
                    self.sp5.setText(s[18])
                    self.ns5.setText(s[19])

                except:
                    print(traceback.print_exc())
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def sock1502(self,a):
        b = a.split(',')

        token = int(b[0].split('_')[1])
        if(token==self.token):
            for i in b:
                # print(i[:2])
                if(i[:2]=='ai'):
                    ask = i.split(':')[1].split('|')
                elif(i[:2]=='bi'):
                    bids = i.split(':')[1].split('|')
                elif(i[:3]=='ltp'):
                    ltp = i.split(':')[1]
                elif (i[:2] == 'ap'):
                    atp = i.split(':')[1]
                elif (i[0] == 'v'):
                    vol = i.split(':')[1]
                elif (i[0] == 'o'):
                    open = i.split(':')[1]
                elif (i[0] == 'h'):
                    high = i.split(':')[1]
                elif (i[0] == 'l'):
                    low = i.split(':')[1]
                elif (i[0] == 'c'):
                    close = i.split(':')[1]

            self.bq1.setText(bids[1])
            self.bq2.setText(bids[5])
            self.bq3.setText(bids[9])
            self.bq4.setText(bids[13])
            self.bq5.setText(bids[17])

            self.bp1.setText(bids[2])
            self.bp2.setText(bids[6])
            self.bp3.setText(bids[10])
            self.bp4.setText(bids[14])
            self.bp5.setText(bids[18])


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
            self.sp2.setText(ask[6])
            self.sp3.setText(ask[10])
            self.sp4.setText(ask[14])
            self.sp5.setText(ask[18])

            self.ns1.setText(ask[3])
            self.ns2.setText(ask[7])
            self.ns3.setText(ask[11])
            self.ns4.setText(ask[15])
            self.ns5.setText(ask[19])

            self.lbLTP.setText(ltp)
            self.lbATP.setText(atp)
            self.lbVol.setText(vol)
            self.lbOpen.setText(open)
            self.lbHigh.setText(high)
            self.lbLow.setText(low)
            self.lbClose.setText(close)

    def subscription_feed(self,token, seg=2,  streamType = 1502):
        try:
            sub_url = self.URL + '/marketdata/instruments/subscription'
            payloadsub = {"instruments": [{"exchangeSegment": seg,"exchangeInstrumentID": token}],"xtsMessageCode": streamType}
            # payloadsub = {"instruments": [{"exchangeSegment": 1,"exchangeInstrumentID": 26000}],"xtsMessageCode": 1501}
            payloadsubjson = json.dumps(payloadsub)
            # print(payloadsubjson)
            req = requests.request("POST", sub_url, data=payloadsubjson, headers=self.MDheaders)

            logging.info(req.text)
            print(req.text)
            resp = req.json()
            print(resp,self)
            'Instrument subscribed successfully!',
            #"Instrument Already Subscribed !"
            if(resp['description']=='Instrument subscribed successfully!'):
                print("subscription feed : ", resp['result']['listQuotes'])
                packet =json.loads(resp['result']['listQuotes'][0])
                bids= packet['Bids']
                asks= packet['Asks']
                # print(bids)
                # print(asks)
            elif(resp['description']=='Instrument Already Subscribed !'):
                print("Instrument Already Subscribed:", token)
                packet = self.getQuote(token)
                bids = packet['Bids']
                asks = packet['Asks']


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
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())

    def unSubscription_feed(self,token, seg=2,  streamType = 1502):
        try:
            sub_url = self.URL + '/marketdata/instruments/subscription'
            payloadsub = {"instruments": [{"exchangeSegment": seg,"exchangeInstrumentID": token}],"xtsMessageCode": streamType}
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("PUT", sub_url, data=payloadsubjson, headers=self.MDheaders)
            logging.info(req.text)

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
            print("getQuote exception : ")
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def hideWindow(self):
        try:
            self.unSubscription_feed(self.token)
            self.bq1.setText('0')
            self.bp1.setText('0')
            self.nb1.setText('0')

            self.bq2.setText('0')
            self.bp2.setText('0')
            self.nb2.setText('0')

            self.bq3.setText('0')
            self.bp3.setText('0')
            self.nb3.setText('0')

            self.bq4.setText('0')
            self.bp4.setText('0')
            self.nb4.setText('0')

            self.bq5.setText('0')
            self.bp5.setText('0')
            self.nb5.setText('0')

            self.sq1.setText('0')
            self.sp1.setText('0')
            self.ns1.setText('0')

            self.sq2.setText('0')
            self.sp2.setText('0')
            self.ns2.setText('0')

            self.sq3.setText('0')
            self.sp3.setText('0')
            self.ns3.setText('0')

            self.sq4.setText('0')
            self.sp4.setText('0')
            self.ns4.setText('0')

            self.sq5.setText('0')
            self.sp5.setText('0')
            self.ns5.setText('0')

            self.hide()
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = Ui_snapQ()
    form.show()
    sys.exit(app.exec_())