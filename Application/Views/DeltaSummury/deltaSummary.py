import time
import traceback
import sys
from os import path, getcwd
from PyQt5.QtCore import QObject,QFile,pyqtSignal,pyqtSlot,Qt,QSortFilterProxyModel,QTimer,QPropertyAnimation
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import *


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import qdarkstyle

from Resourses.icons import icons_rc


import qtpy
import logging
import pandas as pd
import datatable as dt
import requests
import numpy as np
# from ENTRY.buyWindow import Ui_BuyW
# from ENTRY.sellWindow import Ui_SellW
from database_conn import  *
from configReader import *
from MODEL.tableTB import ModelTB
from Theme.dt2 import dt1
# from Application.GetLogs import getLogFile
import logging
# from GetLogs import getLogFile
# from PyQt5.QtWidgets import QFileDialog
from Subclass.titlebar import tBar
import datetime

from py_vollib.black_scholes.implied_volatility import implied_volatility as iv
from py_vollib.black_scholes.greeks.analytical import delta
from py_vollib.black_scholes.greeks.analytical import gamma
from py_vollib.black_scholes.greeks.analytical import rho
from py_vollib.black_scholes.greeks.analytical import theta
from py_vollib.black_scholes.greeks.analytical import vega



class DeltaSummary(QMainWindow):
    def __init__(self,parent=None):
        try:
            super(DeltaSummary, self).__init__(parent=None)
            #####################################################################
            loc1 = getcwd().split('Application')
            ui_login = path.join(loc1[0] , 'Resourses','UI','deltaSummary.ui')
            uic.loadUi(ui_login, self)

            flags = Qt.WindowFlags(Qt.FramelessWindowHint)
            self.setWindowFlags(flags)
            self.title = tBar('Delta Summary')
            self.headerFrame.layout().addWidget(self.title, 0, 0)
            self.title.setStyleSheet('  border-radius: 4px;background-color: rgb(83, 99, 118);')
            self.title.sgPoss.connect(self.movWin)
            self.setStyleSheet(dt1)
            #############################################################################3

            self.leSearch = QLineEdit()
            self.leSearch.setPlaceholderText('Search')
            self.leSearch.setFixedWidth(150)

            ###############################################################################
            self.isStatusBarOpen = False
            self.FolioName = 'HMT'
            self.customIvDict={}
            self.futurePDict = {}
            ###############################################################################

            self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source = readConfig1()

            self.tables_details()
            self.createShortcuts()
            self.createSlots()
            self.createAnimations()
            self.today1 = int(datetime.datetime.today().strftime('%Y%m%d'))
            QSizeGrip(self.frameGrip)

        except:
            logging.error(sys.exc_info())
    def UpdateLTP(self,a):
        # print('Delta Summary',a)
        try:
            fltr = np.asarray([a['Token']])
            lua1 = self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr)]
            # print(lua.size)
            if(lua1.size!=0):
                lua = lua1[0]
                # print('Delta Summary',lua)
                if(lua[4] in ['CE','PE']):
                    # print(self.futureTokenDict)
                    futureToken = self.futureTokenDict[lua[1]]
                    S = self.futurePDict[futureToken][1]
                    # print(lua[1],futureToken,S)
                    if(S!=0):
                        K = float(lua[3])
                        flag = lua[4][0].lower()
                        t= (int(lua[2])-self.today1)/365
                        r=0.0001

                        # print(S, K, t, r, flag)
                        imp_v = iv(a['LTP'], S, K, t, r, flag)

                        dlt= delta(flag,S,K,t,r,imp_v)*lua[6]
                        gma = gamma(flag,S,K,t,r,imp_v)*lua[6]
                        thta = theta(flag,S,K,t,r,imp_v)*lua[6]
                        vga = vega(flag,S,K,t,r,imp_v)*lua[6]
                        mtm = lua[14] + (a['LTP']*lua[6])

                        # print(dlt)
                    # else:
                    #     self.subscription_feed(futureToken)
                        self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr),[5,7,8,9,10,11,12]] = [imp_v,mtm,a['LTP'],dlt,gma,thta,vga]
                        ind = self.modelDR.index(0, 0)
                        ind1 = self.modelDR.index(0, 1)
                        self.modelDR.dataChanged.emit(ind, ind1)
                    else:
                        mtm = lua[14] - (a['LTP'] * lua[6])
                        self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr), [7, 8]] = [mtm, a['LTP']]
                        ind = self.modelDR.index(0, 0)
                        ind1 = self.modelDR.index(0, 1)
                        self.modelDR.dataChanged.emit(ind, ind1)


                else:
                    mtm = lua[14] + (a['LTP'] * lua[6])
                    self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr), [7, 8]] = [mtm, a['LTP']]
                    ind = self.modelDR.index(0, 0)
                    ind1 = self.modelDR.index(0, 1)
                    self.modelDR.dataChanged.emit(ind, ind1)




        except:
            print(traceback.print_exc(),a)

    def updateOpenPosition(self,openPos):
        for i in openPos.keys():
            # print('updateOpenPosition',i,openPos[i])
            if (self.deltaRep.size == 0):
                self.deltaRep = dt.Frame(
                    [[i], [openPos[i][2]], [openPos[i][3]], [openPos[i][4]], [openPos[i][5]], [0.00],
                     [openPos[i][0]], [0.0], [0.0], [0.0], [0.0],
                     [0.0], [0.0], [0.0]]).to_numpy()

                self.modelDR.setDta(self.deltaRep)
                self.modelDR.insertRows()
            else:
                fltr = np.asarray([i])
                lua = self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr)]
                if (lua.size == 0):
                    anm = dt.Frame(
                        [[i], [openPos[i][2]], [openPos[i][3]], [openPos[i][4]], [openPos[i][5]], [0.00],
                         [openPos[i][0]], [0.0], [0.0], [0.0], [0.0],
                         [0.0], [0.0], [0.0]]).to_numpy()

                    self.deltaRep = np.vstack([self.deltaRep, anm])
                    self.modelDR.setDta(self.deltaRep)
                    self.modelDR.insertRows()
                # else:
                #     xyz = self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr), 6]
                #     newApiQty = xyz + qty
                #     self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr), 6] = newApiQty

    def updateTradeSocket(self,trd):

        print('deltaSummary tradeUpdate',trd)

        if (trd[4] != self.FolioName):

            ######### as token in str in UAT##################
            token = int(trd[1])
            ######### as qty in str in UAT also reffer BUY and Buy  ##################
            if (trd[7] == 'Buy'):
                qty = int(trd[10])
            else:
                qty = -int(trd[10])
            #######################################################

            if (self.deltaRep.size == 0):
                self.deltaRep = dt.Frame(
                    [[token], [trd[3]], [trd[4]], [trd[5]], [trd[6]], [0.00],
                     [qty], [0.0], [0.0], [0.0], [0.0],
                     [0.0], [0.0], [0.0]]).to_numpy()

                self.modelDR.setDta(self.deltaRep)
                self.modelDR.insertRows()

                self.deltaSum = dt.Frame([[trd[3]],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]]).to_numpy()
                self.modelDS.setDta(self.deltaSum)
                self.modelDS.insertRows()

            else:
                fltr = np.asarray([token])
                lua = self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr)]
                if (lua.size == 0):
                    anm = dt.Frame(
                        [[token], [trd[3]], [trd[4]], [trd[5]], [trd[6]], [0.00],
                         [qty], [0.0], [0.0], [0.0], [0.0],
                         [0.0], [0.0], [0.0]]).to_numpy()
                    self.deltaRep = np.vstack([self.deltaRep, anm])
                    self.modelDR.setDta(self.deltaRep)
                    self.modelDR.insertRows()
                else:
                    xyz = self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr), 6]
                    newApiQty = xyz + qty
                    self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr), 6] = newApiQty
                ind = self.modelDR.index(0, 0)
                ind1 = self.modelDR.index(0, 1)
                self.modelDR.dataChanged.emit(ind, ind1)

                fltr = np.asarray([trd[3]])
                lua = self.deltaSum[np.in1d(self.deltaSum[:, 0], fltr)]
                if (lua.size == 0):
                    anm = dt.Frame([[trd[3]],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]]).to_numpy()
                    self.deltaSum = np.vstack([self.deltaSum, anm])
                    self.modelDS.setDta(self.deltaSum)
                    self.modelDS.insertRows()

                    ind = self.modelDS.index(0, 0)
                    ind1 = self.modelDS.index(0, 1)
                    self.modelDS.dataChanged.emit(ind, ind1)



    def updateGetTrade(self,tradeLog):

        # print('updateGetTrade deltasum',tradeLog)
        for i in tradeLog:
            # if (i[4] != self.FolioName):
    #         ######### as token in str in UAT##################
            token = int(i[1])
            ######### as qty in str in UAT also reffer BUY and Buy  ##################
            if (i[7] == 'Buy'):
                qty = int(i[10])
            else:
                qty= -int(i[10])

            # print('self.deltaRep.size', i, 'qty' , qty)

            #######################################################

            if (self.deltaRep.size == 0):
                # print('self.deltaRep.size uu', self.deltaRep.size)

                self.deltaRep = dt.Frame(
                    [[token], [i[3]], [i[4]], [i[5]], [i[6]], [0.00],
                     [qty],[0.0],[0.0], [0.0], [0.0],
                     [0.0], [0.0], [0.0],[float(i[12])*-qty]]).to_numpy()
                # print('6677hhd',[i[12]*-qty])
                # print('dsfh',self.deltaRep)
                self.modelDR.setDta(self.deltaRep)
                self.modelDR.insertRows()


                self.deltaSum = dt.Frame([[i[3]],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]]).to_numpy()
                self.modelDS.setDta(self.deltaSum)
                self.modelDS.insertRows()


            else:
                fltr = np.asarray([token])
                lua = self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr)]
                if (lua.size == 0):
                    anm = dt.Frame(
                    [[token], [i[3]], [i[4]], [i[5]], [i[6]], [0.00],
                     [qty],[0.0],[0.0], [0.0], [0.0],
                     [0.0], [0.0], [0.0],[float(i[12])*-qty]]).to_numpy()
                    self.deltaRep = np.vstack([self.deltaRep, anm])
                    self.modelDR.setDta(self.deltaRep)
                    self.modelDR.insertRows()
                else:
                    xyz = self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr), 6]
                    xyz = self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr)][0]
                    # print(xyz)
                    newApiQty = xyz[6] + qty
                    newAmt =   xyz[14] + (float(i[12])*-qty)
                    self.deltaRep[np.in1d(self.deltaRep[:, 0], fltr), [6,14]] = [newApiQty,newAmt]

                fltr = np.asarray([i[3]])
                lua = self.deltaSum[np.in1d(self.deltaSum[:, 0], fltr)]
                if (lua.size == 0):
                    anm = dt.Frame([[i[3]], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0]]).to_numpy()
                    self.deltaSum = np.vstack([self.deltaSum, anm])
                    self.modelDS.setDta(self.deltaSum)
                    self.modelDS.insertRows()

                    ind = self.modelDS.index(0, 0)
                    ind1 = self.modelDS.index(0, 1)
                    self.modelDS.dataChanged.emit(ind, ind1)

        # print('deltaRep',self.deltaRep)


    def filtr(self):
        try:
            self.smodelT.setFilterFixedString(self.listView.selectedIndexes()[0].data())
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())



    def updateGetApi(self,data):
        try:

            self.deltaSum = data
            self.modelDS = ModelTB(self.ApiTrade,self.heads)
            self.smodelDS.setSourceModel(self.modelDS)
            self.tableView.setModel(self.smodelDS)
            self.rcount = self.deltaSum.shape[0]
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())



    def updateSocketTB(self,poss):
        try:
            self.deltaSum = np.vstack([self.deltaSum, poss])
            self.modelDS.insertRows()
            self.modelDS.setDta(self.deltaSum)
            ind = self.modelDS.index(0, 0)
            ind1 = self.modelDS.index(0, 1)
            self.modelDS.dataChanged.emit(ind, ind1)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())

    def tables_details(self):
        try:
            #############################################################################################################
            self.headsR = ['ExchangeInstrumentID',
                           'Symbol','Expiry','Strike_price','C/P','Last_IV',
                           'Qty','MTM','LTP','DELTA','GAMMA',
                           'THETA','VEGA','IV','AMT']
            self.heads = ['Symbol',
                          'CE_IV','PE_IV','MTM','DELTA','GAMMA',
                          'THETA','VEGA']

            self.deltaSum = np.empty((0,8))
            # np.empty((0, 36))
            self.deltaRep = np.empty((0,15))

            #############################################################################################################
            #############################################
            self.modelDS = ModelTB(self.deltaSum,self.heads)
            self.smodelDS = QSortFilterProxyModel()
            self.smodelDS.setSourceModel(self.modelDS)
            self.tableView.setModel(self.smodelDS)

            self.modelDR = ModelTB(self.deltaRep,self.headsR)
            self.smodelDR = QSortFilterProxyModel()
            self.smodelDR.setSourceModel(self.modelDR)
            self.tv_deltaReport.setModel(self.smodelDR)

            self.tableView.horizontalHeader().setSectionsMovable(True)
            self.tableView.verticalHeader().setSectionsMovable(True)
            self.tableView.setDragDropMode(self.tableView.InternalMove)
            self.tableView.setDragDropOverwriteMode(False)
            # self.tableView.clicked.connect(self.tvs6)
        except:
            print(traceback.print_exc())
            logging.error(sys.exc_info())

    def refresh_config(self):
        try:
            self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.source = readConfig1()
        except:
            logging.error(sys.exc_info())



    def setCustomIv(self):
        if(self.lbSymbol.text() in self.customIvDict.keys()):
            pass
        else:
            self.customIvDict[self.lbSymbol.text()] = {}
            #ceIV  #peIV  #calcIV  #

    def createSlots(self):
        self.bt_min.clicked.connect(self.hide)
        self.bt_close.clicked.connect(self.hide)
        self.cxbStatusbar.stateChanged.connect(self.showStatusBar)

    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.hide)


    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)


    def createAnimations(self):
        self.animSB = QPropertyAnimation(self.statusBar1, b"maximumHeight")


    def showStatusBar(self):
        if(self.cxbStatusbar.isChecked()==True):
            print(self.cxbStatusbar.isChecked())
            self.animSB.setDuration(50)
            self.animSB.setStartValue(0)
            self.animSB.setEndValue(80)
            self.animSB.start()
            self.isStatusBarOpen=True
        else:
            self.animSB.setDuration(50)
            self.animSB.setStartValue(80)
            self.animSB.setEndValue(0)
            self.animSB.start()
            self.isStatusBarOpen = False


    def subscription_feed(self,token, seg = 2, streamType=1501):
        try:
            # print('token %s,seg %s,st %s'%(token,seg,streamType),type(token))

            sub_url = self.URL + '/marketdata/instruments/subscription'
            payloadsub = {"instruments": [{"exchangeSegment": seg,"exchangeInstrumentID": token}],"xtsMessageCode": streamType}
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


    def get_summarised_data(self):
        try:
            symList = self.deltaSum[:,0]
            print(symList,'symList')
            for i in symList:
                fltr = np.asarray([i])
                lua = self.deltaRep[np.in1d(self.deltaRep[:, 1], fltr)]
                iv = np.average(lua[:,5])
                mtm = np.sum(lua[:,7])
                delta = np.sum(lua[:,9])
                gamma = np.sum(lua[:,10])
                theta = np.sum(lua[:,11])
                vega = np.sum(lua[:,12])
                self.deltaSum[np.in1d(self.deltaSum[:, 0], fltr), [1,2,3,4,5,6,7]] = [iv,iv,mtm,delta,gamma,theta,vega]
            ind = self.modelDS.index(0, 0)
            ind1 = self.modelDS.index(0, 1)
            self.modelDS.dataChanged.emit(ind, ind1)
        except:
            print(traceback.print_exc())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = DeltaSummary()
    form.show()
    sys.exit(app.exec_())
