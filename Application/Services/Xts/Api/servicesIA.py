import logging
import traceback
import sys
import requests
from PyQt5.QtCore import pyqtSlot,pyqtSignal
import numpy as np
import datatable as dt
import time
import threading
from Application.Views.Models.tableOrder import ModelOB
from Application.Utils.configReader import readDefaultClient,writeITR,refresh,all_refresh_config
from Application.Utils.supMethods import get_ins_details
# from Application.Utils.createTables import ta
from Application.Utils.updation import updateGetOrderTable,updateGetPendingOrderTable,pendingW_datachanged_full,\
    orderW_datachanged_full,PosionW_datachanged_full,updateGetPosition_NP,tradeW_datachanged_full,updateGetTradeTable,updateGetPosition_AMW



def getOrderPayloadWEBApi(exchange,clientID, token,orderSide, qty,limitPrice,validity, disQty, triggerPrice,uid,
                          orderType,productType):
    payload_order_place = {
        "exchangeSegment": exchange,
        "exchangeInstrumentID": token,
        "productType": productType,
        "orderType": orderType,
        "orderSide": orderSide,
        "timeInForce": validity,
        "disclosedQuantity": disQty,
        "orderQuantity": qty,
        "limitPrice": limitPrice,
        "stopPrice": triggerPrice,
        "orderUniqueIdentifier": uid
    }

    return payload_order_place


def getOrderPayloadTWSApi(exchange, clientID, token,  orderSide, qty,limitPrice,  validity, disQty, triggerPrice,uid,
                          orderType,productType):
    payload_order_place = {
        "clientID": clientID,
        "exchangeSegment": exchange,
        "exchangeInstrumentID": token,
        "productType": productType,
        "orderType": orderType,
        "orderSide": orderSide,
        "timeInForce": validity,
        "disclosedQuantity": disQty,
        "orderQuantity": qty,
        "limitPrice": limitPrice,
        "stopPrice": triggerPrice,
        "orderUniqueIdentifier": uid
    }
    return payload_order_place


def PlaceOrder( self,exchange, clientID, token,  orderSide, qty, limitPrice,  validity,
               disQty, triggerPrice,uid,orderType="LIMIT", productType="NRML",):


    try:
        if(self.Source == 'TWSAPI'):
            payload = getOrderPayloadTWSApi(exchange, clientID, token, orderSide, qty, limitPrice,  validity,
               disQty, triggerPrice,uid,orderType,productType)
        else:
            payload = getOrderPayloadWEBApi(exchange, clientID, token, orderSide, qty, limitPrice,  validity,
               disQty, triggerPrice,uid,orderType,productType)

        place_order_url = requests.post(self.URL+'/interactive/orders', json=payload,
                                        headers=self.IAheaders)

        resJson = place_order_url.json()
        aoid = resJson['result']['AppOrderID']
        # print('resJson',aoid,resJson,)
        logging.info(place_order_url.text)
    except:
        print(traceback.print_exc(),resJson)
        logging.error(sys.exc_info()[1])

##############################################################################################################

def getOpenPosition(self):
    try:
        # print('in get_open_pos')
        if (self.Source == 'TWSAPI'):
            url = self.URL + '/interactive/portfolio/dealerpositions?dayOrNet=DayWise'
        elif (self.Source == 'WEBAPI'):
            url = self.URL + '/interactive/portfolio/positions?dayOrNet=DayWise'
        req = requests.request("GET", url, headers=self.IAheaders)
        data_p = req.json()
        dailyPos = data_p['result']['positionList']
        # print(dailyPos)
        if (self.Source == 'TWSAPI'):
            Neturl = self.URL + '/interactive/portfolio/dealerpositions?dayOrNet=NetWise'
        elif (self.Source == 'WEBAPI'):
            Neturl = self.URL + '/interactive/portfolio/positions?dayOrNet=NetWise'

        Netreq = requests.request("GET", Neturl, headers=self.IAheaders)
        Netdata_p = Netreq.json()
        NetPos = Netdata_p['result']['positionList']

        if(NetPos != []):

            self.openPossA = np.empty((0, 6))
            dpos = np.empty((0, 6))
            npos = np.empty((0, 6))

            if (dailyPos == []):
                for i2, i1 in enumerate(NetPos):
                    rmtm = float((i1['RealizedMTM']))
                    nv1 = float((i1['NetAmount']))
                    nv = rmtm if (nv1 == 0) else nv1

                    qty = int((i1['Quantity']).replace(',', ''))
                    token = int(i1['ExchangeInstrumentId'])
                    clientId = '*****'  if ('PRO' in i1['AccountID']) else i1['AccountID']

                    pos1 = dt.Frame([[clientId], [token], [qty], [nv],[i2],[i1['ExchangeSegment']]])
                    self.openPossA = np.vstack([self.openPossA, pos1])
            else:

                for i2, i1 in enumerate(dailyPos):

                    rmtm = float((i1['RealizedMTM']).replace(',', ''))
                    nv1 = float((i1['NetAmount']).replace(',', ''))
                    nv = rmtm if (nv1 == 0) else nv1
                    qty = int((i1['Quantity']).replace(',', ''))
                    token = int(i1['ExchangeInstrumentId'])
                    clientId = '*****'  if ('PRO' in i1['AccountID']) else i1['AccountID']

                    dpos1 = dt.Frame([[clientId], [token], [qty], [nv],[i2],[i1['ExchangeSegment']]])
                    dpos = np.vstack([dpos, dpos1])


                # print('dpos',dpos)
                for i2, i1 in enumerate(NetPos):
                    # print('i1',i1)
                    rmtm = float((i1['RealizedMTM']).replace(',', ''))
                    nv1 = float((i1['NetAmount']).replace(',', ''))
                    nv = rmtm if (nv1 == 0) else nv1
                    qty = int((i1['Quantity']).replace(',', ''))
                    token = int(i1['ExchangeInstrumentId'])
                    clientId = '*****'  if ('PRO' in i1['AccountID']) else i1['AccountID']



                    if(clientId not in self.openPosDict.keys()):
                        self.openPosDict[clientId]={}
                    if (token in dpos[:,1]):
                        fltr = np.asarray([token])
                        filteredArry  = dpos[np.in1d(dpos[:, 1], fltr)]
                        if(filteredArry.size >0):
                            fltr1 = np.asarray([i1['AccountID']])
                            filteredArry1 = filteredArry[np.in1d(filteredArry[:, 0], fltr1)]

                            if (filteredArry1.size > 0):
                                serialNo = filteredArry1[0,4]
                                # print(clientId,'filteredArry1',filteredArry1,'qty',qty,'serialNo',serialNo)
                                fnv = nv - dpos[serialNo,3]
                                Open_Quantity = qty - dpos[serialNo,2]
                            else:
                                fnv = nv
                                Open_Quantity = qty
                        else:
                            fnv = nv
                            Open_Quantity = qty
                    else:
                        fnv = nv
                        Open_Quantity = qty
                    self.openPosDict[clientId][token] = [Open_Quantity,fnv]
                    pos1 = dt.Frame([[clientId], [token], [Open_Quantity], [fnv],[i2],[i1['ExchangeSegment']]])
                    self.openPossA = np.vstack([self.openPossA, pos1])
        else:
            pass

        # for ixc in self.openPossA:
        #     print(ixc)
    except:
        print(traceback.print_exc())

def getPositionBook(self):
    try:
        getOpenPosition(self)
        self.IAS.openPosDict = self.openPosDict
        # print("open pos disk", self.openPosDict)
        self.NetPos.lastSerialNo = 0
        if(self.Source=='TWSAPI'):
            url = self.URL + '/interactive/portfolio/dealerpositions?dayOrNet=NetWise'
        elif(self.Source=='WEBAPI'):
            url = self.URL + '/interactive/portfolio/positions?dayOrNet=NetWise'
        req = requests.request("GET", url, headers=self.IAheaders)
        data_p = req.json()

        aaa = data_p['result']['positionList']
        # print(aaa)
        if(aaa!=[]):

            for j,i in enumerate(aaa):
                try:
                    token  = int(i['ExchangeInstrumentId'])
                    clientId = '*****' if ('PRO' in i['AccountID']) else i['AccountID']
                    ins_details = get_ins_details(self,i['ExchangeSegment'],token)
                    qty = int(i['Quantity'])
                    amt =  float(i['NetAmount'])
                    avgp =  amt/qty if (qty != 0) else 0.0
                    openQty = self.openPosDict[clientId][token][0]
                    openAmount = self.openPosDict[clientId][token][1]
                    dayQty = qty - openQty
                    dayAmount = amt - openAmount


                    pos = dt.Frame([
                        [self.userID],
                        [clientId], [i['ExchangeSegment']],[int(i['ExchangeInstrumentId'])],[ins_details[4]],[ins_details[3]],
                        [ins_details[6]],[ins_details[7]],[ins_details[8]],[int(i['Quantity'])],[float(i['MTM'])],
                        [0],[float(i['RealizedMTM'])],[float(i['NetAmount'])],[avgp],[ins_details [11]],
                        [ins_details[14]],[ins_details[9]],[j],[openQty],[openAmount],
                        [dayQty],[dayAmount] ]).to_numpy()


                    updateGetPosition_NP(self, pos, j )
                    updateGetPosition_AMW(self, pos[0])

                except:
                    print(traceback.print_exc(),'error in getPOs i',i)

           # PosionW_datachanged_full(self)
         #   return pos[:ser_no+1,:]
    except:
        print(traceback.print_exc())

def getOrderBook(self,ifFlush = False):
    try:
        if(self.Source=='WEBAPI'):
            url = self.URL + '/interactive/orders'
            req = requests.request("GET", url, headers=self.IAheaders)
            data_p = req.json()
            noOfPendingOrder = 0


            ApiOrder = np.empty((15000, 23), dtype=object)
            PendingOrder = np.empty((15000, 23), dtype=object)
            j=0
            if(data_p['result']!=[]):
                for j,i in enumerate(data_p['result']):
                    exchange = i["ExchangeSegment"]
                    token = i["ExchangeInstrumentID"]
                    ######################################## contract working ##########################################
                    ins_details = get_ins_details(self, exchange, token )
                    Qty1 = i['LeavesQuantity'] if(i['OrderSide'].upper()=='BUY') else -i['LeavesQuantity']
                    orderSide = i['OrderSide'].replace('BUY','Buy').replace('SELL','Sell')
                    order =dt.Frame([[(i['AppOrderID'])],
                            [i['ClientID']],[i['ExchangeInstrumentID']], [ ins_details[4]], [ins_details[3]],[ins_details[6]],
                            [ins_details[7]],[ins_details[8]],[orderSide],[i['OrderType']], [i['OrderStatus']],
                            [i['OrderQuantity']],[i['LeavesQuantity']],[i['OrderPrice']],[i['OrderStopPrice']], [i['OrderUniqueIdentifier']],
                            [i['OrderGeneratedDateTime']],[i['ExchangeTransactTime']],[i['CancelRejectReason']],[ins_details[0]],[ins_details[5]],
                            [i['OrderAverageTradedPrice']],[Qty1]]).to_numpy()

                    ApiOrder[j, :] =order
                    #############################################################################################

                    if(i['OrderStatus'] in ['PartiallyFilled','New','Replaced'] ):              #and i['OrderUniqueIdentifier']==self.FolioNo
                        PendingOrder[noOfPendingOrder,:] = order
                        noOfPendingOrder += 1


            """ 
            check what should be returt with apiorder j or j+1
            """


            return ApiOrder,j+1,PendingOrder,noOfPendingOrder+1

        else:
            jk = 0
            for kl in self.client_list:
                url = self.URL + '/interactive/orders?clientID=' + kl
                req = requests.request("GET", url, headers=self.IAheaders)
                data_p = req.json()
                noOfPendingOrder = 0

                if (data_p['result'] != []):
                    for j, i in enumerate(data_p['result']):
                        ######################################## contract working ##########################################
                        ins_details = get_ins_details(self, i)
                        ######################################## contract working ##########################################
                        Qty1 = i['LeavesQuantity'] if (i['OrderSide'].upper() == 'BUY') else -i['LeavesQuantity']
                        orderSide = i['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell')

                        order = dt.Frame([[i['AppOrderID']],
                                        [i['ClientID']],[i['ExchangeInstrumentID']], [ins_details[4]], [ins_details[3]], [ins_details[6]],
                                        [ins_details[7]],[ins_details[8]],[orderSide], [i['OrderType']], [i['OrderStatus']],
                                        [i['OrderQuantity']],[i['LeavesQuantity']], [i['OrderPrice']], [i['OrderStopPrice']],[i['OrderUniqueIdentifier']],
                                        [i['OrderGeneratedDateTime']],[i['ExchangeTransactTime']], [i['CancelRejectReason']], [ins_details[0]], [ins_details[5]],
                                        [i['OrderAverageTradedPrice']],[Qty1]]).to_numpy()
                        #############################################################################################
                        updateGetOrderTable(self, order, j)

                        if (i['OrderStatus'] in ['PartiallyFilled', 'New', 'Replaced']):  # and i['OrderUniqueIdentifier'] == self.FolioNo
                            updateGetPendingOrderTable(self, order, noOfPendingOrder)
                            noOfPendingOrder += 1

                        jk += 1

        pendingW_datachanged_full(self)
        orderW_datachanged_full(self)
    ####################################################
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())

def get_Trades(self,requestClass):
    try:
        if(self.Source=='WEBAPI'):
            url = self.URL + '/interactive/orders/trades'
            req = requests.request("GET", url, headers=self.IAheaders)
            data_p = req.json()

            if(data_p['result'] != []):
                for j,i in enumerate(data_p['result']):

                    exchange = i['ExchangeSegment']
                    token = i['ExchangeInstrumentID']
                    ins_details = get_ins_details(self,exchange,token)
                    orderSide = i['OrderSide'].replace('BUY','Buy').replace('SELL','Sell')
                    tradedQty = i['LastTradedQuantity']
                    qty = tradedQty if (orderSide == 'Buy') else -tradedQty
                    netValue =  - qty *  i['LastTradedPrice']
                    trades = np.zeros((0,24),dtype=object)
                    trade = dt.Frame([
                        [i['ClientID']],
                        [i['ClientID']], [i['ExchangeInstrumentID']],[ins_details[4]],[ins_details[3]], [ins_details[6]],
                        [ins_details[7]], [ins_details[8]],[orderSide],[i['AppOrderID']],[i['OrderType']],
                        [tradedQty], [i['OrderStatus']],[i['OrderAverageTradedPrice']],[i['ExchangeTransactTime']], [i['OrderUniqueIdentifier']],
                        [i['ExchangeOrderID']],[i['LastTradedPrice']],[qty],[netValue],[ins_details[0]],
                        [ins_details[11]],[ins_details[14]],['openValue']
                        ]).to_numpy()
                    trades = np.vstack([trades,trade])

                    if(requestClass=='main'):
                        updateGetTradeTable(self,trade,j)
                        self.FolioPos.updateGetApitrd(trades)
        else:
            jk = 0
            ApiTrade = np.empty((0, 24))
            for kl in self.client_list:
                url = self.URL + '/interactive/orders/trades?clientID=' + kl
                req = requests.request("GET", url, headers=self.IAheaders)
                data_p = req.json()
                if (data_p['result'] != []):
                    for j, i in enumerate(data_p['result']):
                        if(i['LoginID']==self.userID):
                            if (i['ExchangeSegment'] == 'NSEFO'):
                                ins_details = self.fo_contract[int(i['ExchangeInstrumentID']) - 35000]
                            elif (i['ExchangeSegment'] == 'NSECM'):
                                ins_details = self.eq_contract[int(i['ExchangeInstrumentID'])]
                            elif (i['ExchangeSegment'] == 'NSECD'):
                                ins_details = self.cd_contract[int(i['ExchangeInstrumentID'])]

                            orderSide = i['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell')
                            tradedQty = i['LastTradedQuantity']
                            qty = tradedQty if(orderSide == 'Buy') else -tradedQty
                            netValue = qty * i['LastTradedPrice']

                            trades = dt.Frame([
                            [i['LoginID']],
                            [i['ClientID']], [i['ExchangeInstrumentID']], [ins_details[4]],[ins_details[3]], [ins_details[6]],
                            [ins_details[7]], [ins_details[8]],[orderSide],[i['AppOrderID']], [i['OrderType']],
                            [tradedQty],[i['OrderStatus']],[i['OrderAverageTradedPrice']], [i['ExchangeTransactTime']],[i['OrderUniqueIdentifier']],
                            [i['ExchangeOrderID']],[i['LastTradedPrice']],[qty],[netValue],[ins_details[0]],
                            [ins_details[11]],[ins_details[14]],['openValue']]).to_numpy()
                            self.sgGTrdSoc.emit(trades)
                            ApiTrade = np.vstack([ApiTrade, trades])
                            jk+=1
            self.sgGetTrd.emit(ApiTrade)
            # print('get Trade signal is emitted')

        tradeW_datachanged_full(self)
    except:
        print('get trade eeror',traceback.print_exc())

def get_balance(self):
    try:

        url = self.URL + '/interactive/user/balance?clientID='+ self.DefaultClient
        req = requests.request("GET", url, headers=self.IAheaders)
        data_p = req.json()
        cashAvailable=data_p['result']['BalanceList'][self.Mrglvl]['limitObject']['RMSSubLimits']['cashAvailable']
        collateral=data_p['result']['BalanceList'][self.Mrglvl]['limitObject']['RMSSubLimits']['collateral']
        marginUtilized=data_p['result']['BalanceList'][self.Mrglvl]['limitObject']['RMSSubLimits']['marginUtilized']
        netMarginAvailable=data_p['result']['BalanceList'][self.Mrglvl]['limitObject']['RMSSubLimits']['netMarginAvailable']
        self.lbTMargin.setText('%.2f'%(float(cashAvailable) + float(collateral)))
        self.lbUMargin.setText('%.2f'%float(marginUtilized))
        self.lbFMargin.setText('%.2f'%float(netMarginAvailable))
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())

def login(self):
    try:
        refresh(self)

        payload = {"secretKey": self.IASecret, "appKey": self.IAKey, "source": self.Source}
        login_url = self.URL + '/interactive/user/session'
        login_access = requests.post(login_url, json=payload)

        # print(login_url, login_access.text,'\n',payload)

        if login_access.status_code == 200:
            data = login_access.json()
            result = data['result']

            if data['type'] == 'success':
                token = result['token']
                self.login.label.append('Interactive API Logged In')
                #####################################  clist  ###########################################################
                client_codes_r = result['clientCodes']
                self.loggedInUser = result['userID']
                self.client_list = []
                self.clientFolios = {'A0001':[]}
                self.FolioPos.clientFolios = {'A0001':[]}
                self.FolioPos.cbClient.addItem('A0001')

                for i in client_codes_r:
                    if (i[:3] == 'PRO'):
                        self.client_list.append('*****')
                        self.FolioPos.clientFolios['*****'] = ['MANUAL_*****']
                        self.FolioPos.cbClient.addItem('*****')

                    else:
                        self.client_list.append(i)
                        self.FolioPos.clientFolios[i] = ['MANUAL_'+i]
                        self.FolioPos.cbClient.addItem(i)

                dclient = readDefaultClient()
                if (dclient in self.client_list):
                    self.defaultClient = dclient

                writeITR(token, self.userID, self.client_list)
                self.login.updateIAstatus(data['type'])


                refresh(self)

                th3 = threading.Thread(target=getPositionBook, args=(self,))
                th3.start()
                th1 = threading.Thread(target=get_Trades, args=(self,'main'))
                self.IAS.start_socket_io()
                #
                th2 = threading.Thread(target=getOrderBook, args=(self, ))
                #
                #
                th1.start()
                th2.start()

                all_refresh_config(self)

                self.login.pbNext.show()


            else:
                a = 'Check API Details'
                self.login.updateIAstatus(a)


        else:
            logging.info(str(login_access.text).replace('\n', '\t\t\t\t'))
            ################# check if success ############
        refresh(self)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info())

def cancel_order(self,cancledOrderist):
    try:

        for i in cancledOrderist:
            cancle_url = self.URL + "/interactive/orders?appOrderID=" + str(
                i['AppOrderId']) + "&orderUniqueIdentifier=" + str(i['FolioNO']) + "&clientID=" + i['clientId']

            cancle_order_r = requests.delete(cancle_url, headers=self.IAheaders)
            print(cancle_order_r.text)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])

