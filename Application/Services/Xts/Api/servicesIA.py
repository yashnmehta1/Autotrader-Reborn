import logging
import traceback
import sys
import requests
from Application.Utils.configReader import readDefaultClient,writeITR,refresh,all_refresh_config
from PyQt5.QtCore import pyqtSlot,pyqtSignal
import numpy as np
import datatable as dt
import time
import threading
from Application.Views.Models.tableOrder import ModelOB



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
        print('resJson',aoid,resJson,)
        logging.info(place_order_url.text)
    except:
        print(traceback.print_exc(),resJson)
        logging.error(sys.exc_info()[1])

##############################################################################################################

def get_open_poss(self):
    try:
        print('in get_open_pos')
        if (self.Source == 'TWSAPI'):
            url = self.URL + '/interactive/portfolio/dealerpositions?dayOrNet=DayWise'
        elif (self.Source == 'WEBAPI'):
            url = self.URL + '/interactive/portfolio/positions?dayOrNet=DayWise'
        req = requests.request("GET", url, headers=self.IAheaders)
        data_p = req.json()
        dailyPos = data_p['result']['positionList']
        print(dailyPos)
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


                print('dpos',dpos)
                for i2, i1 in enumerate(NetPos):
                    print('i1',i1)
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
                                print(clientId,'filteredArry1',filteredArry1,'qty',qty,'serialNo',serialNo)
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

def get_position(self):
    try:
        get_open_poss(self)
        print('in get_pos')
        self.NetPos.lastSerialNo = 0
        if(self.Source=='TWSAPI'):
            url = self.URL + '/interactive/portfolio/dealerpositions?dayOrNet=NetWise'
        elif(self.Source=='WEBAPI'):
            url = self.URL + '/interactive/portfolio/positions?dayOrNet=NetWise'
        req = requests.request("GET", url, headers=self.IAheaders)
        print('in get_pos',req.text)
        data_p = req.json()

        aaa = data_p['result']['positionList']

        if(aaa!=[]):
            for j,i in enumerate(aaa):
                try:
                    try:
                        if (i['ExchangeSegment'] == 'NSEFO'):
                            ins_details = self.fo_contract[int(i['ExchangeInstrumentId']) - 35000]
                        elif (i['ExchangeSegment'] == 'NSECM'):
                            ins_details = self.eq_contract[int(i['ExchangeInstrumentId'])]
                        elif (i['ExchangeSegment'] == 'NSECD'):
                            ins_details = self.cd_contract[int(i['ExchangeInstrumentId'])]

                    except:
                        logging.error(sys.exc_info()[1])
                        print(traceback.print_exc())

                    qty = int(i['Quantity'])
                    if (qty != 0):
                        amt = float(i['NetAmount'])
                        avgp = amt / qty
                    else:
                        avgp = 0.0
                    clientId = '*****'  if ('PRO' in i['AccountID']) else i['AccountID']

                    self.NetPos.Apipos[j,:] = dt.Frame([
                        [self.userID],
                        [clientId], [i['ExchangeSegment']],[int(i['ExchangeInstrumentId'])],[ins_details[4]],[ins_details[3]],
                        [ins_details[6]],[ins_details[7]],[ins_details[8]],[int(i['Quantity'])],[float(i['MTM'])],
                        [0],[float(i['RealizedMTM'])],[float(i['NetAmount'])],[avgp],[ins_details [11]],
                        [ins_details[14]],[ins_details[9]],[j]]).to_numpy()

                    self.NetPos.lastSerialNo +=1
                    self.NetPos.modelP.lastSerialNo +=1
                    self.NetPos.modelP.insertRows()
                    self.NetPos.modelP.rowCount()
                except:
                    print(traceback.print_exc(),'error in getPOs i',i)
            ind = self.NetPos.modelP.index(0, 0)
            ind1 = self.NetPos.modelP.index(0, 1)

            self.NetPos.modelP.dataChanged.emit(ind, ind1)
            print('self.NetPos.Apipos',self.NetPos.Apipos)
    except:
        print(traceback.print_exc())

def get_Pending(self):
    try:
        ApiOrder = np.empty((0, 22))
        ApiOrder1 = np.empty((0, 22))
        if(self.Source=='WEBAPI'):
            url = self.URL + '/interactive/orders'
            req = requests.request("GET", url, headers=self.IAheaders)
            data_p = req.json()
            noOfPendingOrder = 0
            if(data_p['result']!=[]):
                for j,i in enumerate(data_p['result']):
                    print('get_pending_order',j,i)
                    Qty1 = i['LeavesQuantity'] if(i['OrderSide'].upper()=='BUY') else -i['LeavesQuantity']
                    ######################################## contract working ##########################################
                    try:
                        if (i['ExchangeSegment'] == 'NSEFO'):
                            ah = self.fo_contract[int(i['ExchangeInstrumentID']) - 35000]
                            # print('ah',ah)
                            ins = [ah[4], ah[3], ah[6], ah[7], ah[8], ah[11], ah[14], ah[9], ah[0], ah[5]]
                            # self.cntrcts[int(i['ExchangeInstrumentID'])] = ins
                        elif (i['ExchangeSegment'] == 'NSECM'):
                            ah = self.eq_contract[int(i['ExchangeInstrumentID'])]
                            # print('ah',ah)
                            ins = [ah[4], ah[3], ah[6], ah[7], ah[8], ah[11], ah[14], ah[9], ah[0], ah[5]]
                            # self.cntrcts[int(i['ExchangeInstrumentID'])] = ins
                        elif (i['ExchangeSegment'] == 'NSECD'):
                            ah = self.cd_contract[int(i['ExchangeInstrumentID'])]
                            # print('ah',ah)
                            ins = [ah[4], ah[3], ah[6], ah[7], ah[8], ah[11], ah[14], ah[9], ah[0], ah[5]]
                            # self.cntrcts[int(i['ExchangeInstrumentId'])] = ins

                    except:
                        logging.error(sys.exc_info()[1])
                        print(traceback.print_exc())
                    orderSide = i['OrderSide'].replace('BUY','Buy').replace('SELL','Sell')
                    anm =dt.Frame([[i['ClientID']],
                                                            [i['ExchangeInstrumentID']], [ ins[0]], [ins[1]],[ins[2]], [ins[3]],
                                                            [ins[4]],[orderSide],[(i['AppOrderID'])],[i['OrderType']], [i['OrderStatus']],
                                                            [i['OrderQuantity']],[i['LeavesQuantity']],[i['OrderPrice']],[i['OrderStopPrice']], [i['OrderUniqueIdentifier']],
                                                            [i['OrderGeneratedDateTime']],[i['ExchangeTransactTime']],[i['CancelRejectReason']],[ins[8]],[ins[9]],
                                                            [i['OrderAverageTradedPrice']]]).to_numpy()

                    self.OrderBook.ApiOrder[j, :] = anm
                    # self.OrderBook.rcount = self.TradeW.ApiTrade.shape[0]
                    self.OrderBook.lastSerialNo += 1
                    self.OrderBook.modelO.lastSerialNo += 1
                    self.OrderBook.modelO.rowCount()
                    self.OrderBook.modelO.insertRows()
                    #############################################################################################
                    if(i['OrderStatus'] in ['PartiallyFilled','New','Replaced'] ):              #and i['OrderUniqueIdentifier']==self.FolioNo
                        self.PendingW.ApiOrder[noOfPendingOrder, :] = anm

                        noOfPendingOrder +=1
                        self.PendingW.rcount = self.TradeW.ApiTrade.shape[0]

                        self.PendingW.lastSerialNo += 1
                        self.PendingW.modelO.lastSerialNo += 1
                        self.PendingW.modelO.rowCount()
                        self.PendingW.modelO.insertRows()

                    #     self.ApiOrderList = np.vstack([self.ApiOrderList, np.array([[str(i['AppOrderID']), i['ExchangeInstrumentID'], Qty1]])])
                    #     fltr = np.asarray([i['ExchangeInstrumentID']])
                    #     lua = self.ApiOrderSummary[np.in1d(self.ApiOrderSummary[:, 0], fltr)]
                    #     if (lua.size != 0):
                    #         prevQty = lua[0][1]
                    #         self.ApiOrderSummary[np.in1d(self.ApiOrderSummary[:, 0], fltr), 1] = prevQty + Qty1
                    #         self.sgAPQ.emit([i['ExchangeInstrumentID'],prevQty + Qty1])
                    #     else:
                    #         self.ApiOrderSummary = np.vstack([self.ApiOrderSummary,np.array([[i['ExchangeInstrumentID'], Qty1]])])
                    #         self.sgAPQ.emit([i['ExchangeInstrumentID'], Qty1])
                    #
                    # fltr = np.asarray(['New','Replaced','PartiallyFilled'])
                    # ApiOrder1 = ApiOrder[np.in1d(ApiOrder[:, 10], fltr)]



                ind = self.PendingW.modelO.index(0, 0)
                ind1 = self.PendingW.modelO.index(0, 1)

                self.PendingW.modelO.dataChanged.emit(ind, ind1)


                ind = self.OrderBook.modelO.index(0, 0)
                ind1 = self.OrderBook.modelO.index(0, 1)

                self.OrderBook.modelO.dataChanged.emit(ind, ind1)


        else:
            jk = 0
            for kl in self.client_list:
                url = self.URL + '/interactive/orders?clientID=' + kl
                req = requests.request("GET", url, headers=self.IAheaders)
                data_p = req.json()
                if (data_p['result'] != []):
                    for j, i in enumerate(data_p['result']):
                        Qty1 = i['LeavesQuantity'] if (i['OrderSide'].upper() == 'BUY') else -i['LeavesQuantity']
                        ######################################## contract working ##########################################
                        try:
                            if (i['ExchangeSegment'] == 'NSEFO'):
                                ah = self.fo_contract[int(i['ExchangeInstrumentID']) - 35000]
                                # print('ah',ah)
                                ins = [ah[4], ah[3], ah[6], ah[7], ah[8], ah[11], ah[14], ah[9], ah[0], ah[5]]
                                # self.cntrcts[int(i['ExchangeInstrumentID'])] = ins
                            elif (i['ExchangeSegment'] == 'NSECM'):
                                ah = self.eq_contract[int(i['ExchangeInstrumentID'])]
                                # print('ah',ah)
                                ins = [ah[4], ah[3], ah[6], ah[7], ah[8], ah[11], ah[14], ah[9], ah[0], ah[5]]
                                # self.cntrcts[int(i['ExchangeInstrumentID'])] = ins
                            elif (i['ExchangeSegment'] == 'NSECD'):
                                ah = self.cd_contract[int(i['ExchangeInstrumentID'])]
                                # print('ah',ah)
                                ins = [ah[4], ah[3], ah[6], ah[7], ah[8], ah[11], ah[14], ah[9], ah[0], ah[5]]
                                # self.cntrcts[int(i['ExchangeInstrumentId'])] = ins
                        except:
                            logging.error(sys.exc_info()[1])
                        ######################################## contract working ##########################################
                        bs = i['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell')

                        # if (jk == 0):
                        #     n2darray = dt.Frame([[i['ClientID']], [i['ExchangeInstrumentID']], [ins[0]],
                        #                           [ins[1]], [ins[2]], [ins[3]], [ins[4]],
                        #                           [i['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell')],
                        #                           [i['AppOrderID']], [i['OrderType']], [i['OrderStatus']],
                        #                           [i['OrderQuantity']],
                        #                           [i['LeavesQuantity']], [i['OrderPrice']], [i['OrderStopPrice']],
                        #                           [i['OrderUniqueIdentifier']], [i['OrderGeneratedDateTime']],
                        #                           [i['ExchangeTransactTime']],
                        #                           [i['CancelRejectReason']], [ins[8]], [ins[9]],
                        #                           [i['OrderAverageTradedPrice']]]).to_numpy()
                        # else:
                        n2darray = dt.Frame([[i['ClientID']], [i['ExchangeInstrumentID']], [ins[0]],
                                              [ins[1]], [ins[2]], [ins[3]], [ins[4]],
                                              [i['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell')],
                                              [str(i['AppOrderID'])], [i['OrderType']], [i['OrderStatus']], [i['OrderQuantity']],
                                              [i['LeavesQuantity']], [i['OrderPrice']], [i['OrderStopPrice']],
                                              [i['OrderUniqueIdentifier']],
                                              [i['OrderGeneratedDateTime']],
                                              [i['ExchangeTransactTime']], [i['CancelRejectReason']], [ins[8]], [ins[9]],
                                              [i['OrderAverageTradedPrice']]]).to_numpy()
                        ApiOrder = np.vstack([ApiOrder, n2darray])
                        #############################################################################################
                        if (i['OrderStatus'] in ['PartiallyFilled', 'New', 'Replaced'] and i[
                            'OrderUniqueIdentifier'] == self.FolioNo):
                            self.ApiOrderList = np.vstack(
                                [self.ApiOrderList, np.array([[i['AppOrderID'], i['ExchangeInstrumentID'], Qty1]])])

                            fltr = np.asarray([i['ExchangeInstrumentID']])
                            lua = self.ApiOrderSummary[np.in1d(self.ApiOrderSummary[:, 0], fltr)]
                            if (lua.size != 0):
                                prevQty = lua[0][1]
                                self.ApiOrderSummary[np.in1d(self.ApiOrderSummary[:, 0], fltr), 1] = prevQty + Qty1
                                self.sgAPQ.emit([i['ExchangeInstrumentID'], prevQty + Qty1])
                            else:
                                self.ApiOrderSummary = np.vstack(
                                    [self.ApiOrderSummary, np.array([[i['ExchangeInstrumentID'], Qty1]])])
                                self.sgAPQ.emit([i['ExchangeInstrumentID'], Qty1])
                        jk += 1
                    fltr = np.asarray(['New', 'Replaced', 'PartiallyFilled'])
                    ApiOrder1 = ApiOrder[np.in1d(ApiOrder[:, 10], fltr)]
                time.sleep(0.5)
            # print('ApiOrderApiOrderApiOrderApiOrder',ApiOrder)
            # print('ApiOrder1',ApiOrder1)
            self.sgGetOrder.emit(ApiOrder)
            self.sgGetPOrder.emit(ApiOrder1)


    ####################################################
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())

def get_Trades(self):
    try:
        if(self.Source=='WEBAPI'):
            ApiTrade = np.empty((0, 23))
            url = self.URL + '/interactive/orders/trades'
            req = requests.request("GET", url, headers=self.IAheaders)
            data_p = req.json()




            if(data_p['result'] != []):
                for j,i in enumerate(data_p['result']):

                    if (i['ExchangeSegment'] == 'NSEFO'):
                        ins_details = self.fo_contract[int(i['ExchangeInstrumentID']) - 35000]
                    elif (i['ExchangeSegment'] == 'NSECM'):
                        ins_details = self.eq_contract[int(i['ExchangeInstrumentID'])]
                    elif (i['ExchangeSegment'] == 'NSECD'):
                        ins_details = self.cd_contract[int(i['ExchangeInstrumentID'])]

                    orderSide = i['OrderSide'].replace('BUY','Buy').replace('SELL','Sell')
                    tradedQty = i['LastTradedQuantity']
                    qty = tradedQty if (orderSide == 'Buy') else -tradedQty
                    netValue = qty * i['LastTradedPrice']

                    self.TradeW.ApiTrade[j,:]= dt.Frame([[i['ClientID']],
                        [i['ClientID']], [i['ExchangeInstrumentID']],[ins_details[4]],[ins_details[3]], [ins_details[6]],
                            [ins_details[7]], [ins_details[8]],[orderSide],[i['AppOrderID']],[i['OrderType']],
                        [tradedQty], [i['OrderStatus']],[i['OrderAverageTradedPrice']],[i['ExchangeTransactTime']], [i['OrderUniqueIdentifier']],
                        [i['ExchangeOrderID']],[i['LastTradedPrice']],[qty],[netValue],[ins_details[0]],
                            [ins_details[11]],[ins_details[14]],['openValue']
                    ]).to_numpy()



                    self.TradeW.lastSerialNo += 1
                    self.TradeW.modelT.lastSerialNo += 1
                    self.TradeW.modelT.rowCount()
                    self.TradeW.modelT.insertRows()

                    ind = self.TradeW.modelT.index(0, 0)
                    ind1 = self.TradeW.modelT.index(0, 1)

                    self.TradeW.modelT.dataChanged.emit(ind, ind1)

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
            print('get Trade signal is emitted')
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

        print(login_url, login_access.text,'\n',payload)

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
                for i in client_codes_r:
                    if (i[:3] == 'PRO'):
                        self.client_list.append('*****')
                    else:
                        self.client_list.append(i)

                dclient = readDefaultClient()
                if (dclient in self.client_list):
                    self.defaultClient = dclient

                writeITR(token, self.userID, self.client_list)
                self.login.updateIAstatus(data['type'])


                refresh(self)


                th1 = threading.Thread(target=get_Trades, args=(self,))
                self.IAS.start_socket_io()

                th2 = threading.Thread(target=get_Pending, args=(self, ))
                th3 = threading.Thread(target=get_position, args=(self,))

                th1.start()
                th2.start()
                th3.start()
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
