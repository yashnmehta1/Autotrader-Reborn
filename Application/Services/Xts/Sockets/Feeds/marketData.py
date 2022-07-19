
# import datetime
import traceback
import sys
import requests
import json
import logging
from threading import Thread
from py_vollib.black_scholes.implied_volatility import implied_volatility as iv
from py_vollib.black_scholes.implied_volatility import implied_volatility as iv
from py_vollib.black_scholes.greeks.analytical import delta
from py_vollib.black_scholes.greeks.analytical import gamma
from py_vollib.black_scholes.greeks.analytical import rho
from py_vollib.black_scholes.greeks.analytical import theta
from py_vollib.black_scholes.greeks.analytical import vega




from PyQt5.QtCore import QObject,pyqtSlot,pyqtSignal

from Application.Services.Xts.Sockets.Feeds.marketDataSocketClient import  MDSocket_io
from Application.Utils.configReader import *
# from Application.GetLogs import getLogFile

class MarketFeeds(QObject):
    sgLoginS = pyqtSignal(str)
    sgSocketConn = pyqtSignal()
    sgNPFrec = pyqtSignal(dict)
    sgNSQrec = pyqtSignal(str)
    sgindexfd = pyqtSignal(int,float)
    sgSocConn = pyqtSignal(int)

    def __init__(self):
        super(MarketFeeds, self).__init__()
        refresh(self)

    def start_socket(self):
        try:
            refresh(self)
            self.soc = MDSocket_io(self.MDToken, self.userID)
            Thread(target=self.connectsocket).start()
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())
    def connectsocket(self):
        try:

            el = self.soc.get_emitter()

            el.on('1502-json-partial', self.on_message1502_json_partial)
            el.on('1501-json-partial', self.on_message1501_json_partial)
            el.on('1505-json-partial', self.on_message1505_json_partial)


            el.on('disconnect', self.on_disconnect)
            el.on('connect', self.on_connect)
            el.on('joined',self.on_join)

            self.soc.connect()
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())


    def on_message1501_json_partial(self, data):
        # print(sys.getsizeof(data))
        # print(type(data))
        #print(data)
        # print(data)

        try:
            b = (data.split(','))
            exch = b[0].split('_')[0][2]
            token = b[0].split('_')[1]
            bid = float(b[1].split('|')[2])
            bidQ = float(b[1].split('|')[1])
            ask = float(b[2].split('|')[2])
            askQ = float(b[2].split('|')[1])
            ltp = float(b[3].split(':')[1])
            pc = '%.2f'%(float(b[11].split(':')[1]))
            open = float(b[12].split(':')[1])
            high = float(b[13].split(':')[1])
            low = float(b[14].split(':')[1])
            close = float(b[15].split(':')[1])
    #a
            d1 = {"Exch":exch,"Token": int(token),"Bid": bid,"BQ": bidQ,"Ask": ask,"AQ": askQ,"LTP": ltp,
                  "%CH" : pc,"OPEN":open,"HIGH":high,"LOW":low,"CLOSE":close,}
            self.sgNPFrec.emit(d1)

            if(token in ['26000','26001','26002']):
                self.sgindexfd.emit(int(token), float(ltp))

            # Thread(target=self.updatept,args=(ltp,bid,ask,token)).start()
        except IndexError:
            pass
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())
    def on_connect(self):
        try:
            print('Market Data Socket connected successfully!')
            logging.info('Market Data Socket connected successfully!')
            self.sgSocketConn.emit()
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())
    def on_join(self,data):
        try:
            print(data)
            logging.info('Market Data Socket join!' +  data)
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())
    def on_disconnect(self):
        try:
            print('Market Data Socket disconnected!')
            logging.info('Market Data Socket disconnected!')
            # msg = QMessageBox()
            # msg.setIcon(QMessageBox.Warning)
            # msg.setText("Market-Data Socket has benn Disconnected...!")
            # msg.show()
            self.sgSocConn.emit(1)
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())
    def on_message1505_json_partial(self,data):
        try:

            logging.info(data)
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())
    def on_message1502_json_partial(self, data):
        # print(data)
        self.sgNSQrec.emit(data)
        pass

