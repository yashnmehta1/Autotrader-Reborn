import time


import traceback
from PyQt5.QtCore import QObject,pyqtSlot,pyqtSignal,QTimer
import sys
import datatable as dt
import socketio
import os
import requests
import json
import logging
from threading import Thread
# import time
import pandas as pd
import datatable as dt

from Application.Utils.dbConnection import *
from Application.Utils.configReader import readConfig_All,readDefaultClient,writeITR,refresh
import numpy as np
from Application.Services.Xts.Sockets.Trade.IA_socket_services import  *


class Interactive(QObject):
    sgLoginS = pyqtSignal(str)
    sgSocketConn = pyqtSignal()
    sgSocConn = pyqtSignal(int)

    # sgOpenPos = pyqtSignal(dict)
    sgGetAPIpos = pyqtSignal(object)
    sgGetAPIposD = pyqtSignal(object)
    sgAPIpos = pyqtSignal(object)

    sgOpenPos = pyqtSignal(object)
    sgGetOrder = pyqtSignal(object)
    sgGetPOrder = pyqtSignal(object)
    sgPendSoc = pyqtSignal(object)
    sgRejection = pyqtSignal()
    sgAPQ =pyqtSignal(list)

    sgGetTrd =pyqtSignal(object)
    sgGTrdSoc =pyqtSignal(object)
    sgTrdSoc =pyqtSignal(object)

    sgAddScrp = pyqtSignal(int, int)
    sgComplOrd = pyqtSignal(list)
    sgClist = pyqtSignal(list)
    sgDClient = pyqtSignal(str)
    sgTrdC =pyqtSignal(list)
    sgBalance = pyqtSignal(list)
    sgRemainingDetail = pyqtSignal(list)
    sgStatusUp = pyqtSignal(str)
    sgLoggedinUser = pyqtSignal(str)
    def __init__(self):
        super(Interactive, self).__init__()

        # self.exchangeList = {"NSECM": 1, "NSEFO": 2, "NSECD": 3, "BSECM": 11, "BSEFO": 12, "MCXFO": 51}
        # self.client_list = []
        # self.FolioNo = 'HMT'

        self.ApiOrderSummary = np.empty(shape=[0,2],dtype='int')
        self.ApiOrderList = np.empty(shape=[0,3],dtype='int')
        self.openPosDict = {}
        self.TWPQ = np.asarray([])




################################################################################


################################################################################

################################################################################

#####################################################################################
    def start_socket_io(self):
        try:
            refresh(self)

            self.interactiveEmitters(self.IAToken,self.userID)
            Thread(target=self.connectIA).start()
            # print('inr api soc connct')
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def connectIA(self, headers={}, transports='websocket', namespaces=None, socketio_path='/interactive/socket.io',
                  verify=False):
        try:
            url = self.connection_url
            self.sid.connect(url, headers, transports, namespaces, socketio_path)
            self.sid.wait()
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def interactiveEmitters(self, token, userID, reconnection=True, reconnection_attempts=0, reconnection_delay=1,
                            reconnection_delay_max=5, randomization_factor=0.5, logger=False, binary=False, json=None, **kwargs):
        try:
            refresh(self)
            self.sid = socketio.Client()
            self.eventlistener = self.sid
            self.sid.on('connect',self.on_connect)

            self.sid.on('message',self.on_message)
            self.sid.on('joined',self.on_joined)
            self.sid.on('position',self.on_position)
            self.sid.on('error',self.on_error)
            self.sid.on('trade',self.on_trade)
            self.sid.on('order',self.on_order)
            self.sid.on('logout',self.on_messagelogout)

            self.sid.on('disconnect',self.on_disconnect)
            self.userID = userID
            self.token = token
            port = f'{self.URL}/?token='
            self.connection_url = port + self.token + '&userID=' + self.userID + "&apiType=INTERACTIVE"
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())

    def on_trade(self,data):
        # print('on_trade',data)
        update_on_trade(self,data)
    def on_order(self,data):
        # print('on_order',data)
        update_on_order(self,data)
    def on_position(self,data):
        # print('on_position',data)
        update_on_position(self,data)

    def get_emitter(self):
        try:
            return self.eventlistener
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def on_connect(self):
        logging.info('Interactive socket connected successfully!1111111')
        # print('Interactive socket connected successfully!1111111')
        self.sgSocketConn.emit()

    def on_disconnect(self):
        self.sgSocConn.emit(1)
        logging.info('Interactive Socket disconnected!')
        # print('Interactive Socket disconnected!')

    def on_message(self, data):
        try:
            logging.info('received a message! : ' + data)
            # print('I received a message! %s'%data)
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())

    def on_joined(self, data):
        try:
            # print('Interactive socket joined successfully! %s' % data)
            logging.info('%s' % data)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])

    def on_error(self, data):
        try:
            logging.error('Interactive socket error!' + data)
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())

    def on_messagelogout(self, data):
        try:
            logging.info("User logged out!" + data)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info()[1])
#####################################################################################

###################################################  Concerns  ####################################################################
"""
auto Reconnect
client list
contract dict
connection status
path for config parser 
path for get log
use of pop ups
Q&A dailogs
if possible dont maintain table at both place


openPos and IntradayPos
all possible error scenarios for openPos calculation

minimize use of python list


where to use slot decorator
user id from config reader and login response telly




stress test json working with [ np array / ujson / orjson]
https://stackoverflow.com/questions/41068942/fastest-way-to-parse-json-strings-into-numpy-arrays


reworking folio pos from scratch no s off from folio pos cb cur index == 0
s off button inactive mean time 2 sec from s off executiom

review replace commas remove if not required


**********not all data comes in trades and order window


changed are made in except condition ins apply in get tarde and get order please check there 


regorous name changes
 
"""


##################################################################################################################################
