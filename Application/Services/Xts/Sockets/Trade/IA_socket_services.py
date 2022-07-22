import json
import logging

import numpy as np
import sys
import traceback
import datatable as dt
from Application.Utils.supMethods import get_ins_details


def update_on_position(self, data):
    try:
        data1 = json.loads(data)

        exchange = data1['ExchangeSegment']
        token = int(data1['ExchangeInstrumentID'])
        ins_details = get_ins_details(self,exchange,token)

        rmtm = float((data1['RealizedMTM']).replace(',', ''))
        nv = float(data1['NetValue'].replace(',', ''))
        nv = rmtm if (nv == 0) else nv
        qty = int(data1['NetPosition'])
        amt = nv
        mtm = float((data1['MTM']).replace(',', ''))
        clientId = '*****' if ('PRO' in data1['AccountID']) else data1['AccountID']

        if (clientId not in self.openPosDict.keys()):
            self.openPosDict[clientId] = {}

        if (token not in self.openPosDict[clientId].keys()):
            self.openPosDict[clientId][token] = [0, 0.0]


        openQty = self.openPosDict[data1['AccountID']][token][0]
        openAmt = self.openPosDict[data1['AccountID']][token][1]
        dayQty = qty - openQty
        dayAmount = amt - openAmt

        if (qty != 0):
            avgp = amt / qty
        else:
            avgp = 0.0
        # print("open pos dict",token,clientId, self.openPosDict)
        #     print("open pos dict - token", self.openPosDict)
        pos = dt.Frame(
            [[data1['LoginID']],
            [data1['AccountID']], [data1['ExchangeSegment']], [token],[ins_details[4]],[ins_details[3]],
            [ins_details[6]],[ins_details[7]],[ins_details[8]],[qty], [mtm],
            [0], [rmtm], [nv],[avgp],[ins_details [11]],
            [ins_details[14]],[ins_details[9]],[1000],[openQty],[openAmt],
             [dayQty],[dayAmount]]).to_numpy()

        self.sgAPIpos.emit(pos)
    except:
        print(sys.exc_info(), 'on_position')
        print(traceback.print_exc())


def update_on_order(self, data):
    try:
        data1 = json.loads(data)
        logging.info(data)
        exchange = data1['ExchangeSegment']
        token = int(data1['ExchangeInstrumentID'])
        ins_details = get_ins_details(self,exchange,token)
        orderSide = data1['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell')
        qty1 =data1['OrderQuantity'] if orderSide == "Buy" else  -data1['OrderQuantity']
        n2darray =dt.Frame( [[data1['AppOrderID']],
                            [data1['ClientID']],[data1['ExchangeInstrumentID']], [ins_details[4]],[ins_details[3]], [ins_details[6]],
                            [ins_details[7]],[ins_details[8]],[orderSide], [data1['OrderType']], [data1['OrderStatus']],
                            [data1['OrderQuantity']],[data1['LeavesQuantity']], [data1['OrderPrice']], [data1['OrderStopPrice']],[data1['OrderUniqueIdentifier']],
                            [data1['OrderGeneratedDateTime']],[data1['ExchangeTransactTime']],[data1['CancelRejectReason']], [ins_details[0]], [ins_details[5]],
                            [data1['OrderAverageTradedPrice']],[qty1]]).to_numpy()
        self.sgPendSoc.emit(n2darray)

        if (data1['OrderStatus'] == 'Filled'):
            self.sgComplOrd.emit([int(data1['ExchangeInstrumentID']), data1['OrderSide'], data1['OrderQuantity'],
                                  float(data1['OrderAverageTradedPrice'].replace(',', '')), data1['AppOrderID'],
                                  data1['OrderUniqueIdentifier'], data1['OrderType']])
        if (data1['OrderStatus'] == 'Rejected'):
            self.sgRejection.emit()
        # self.sgStatusUp.emit(data)
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())


def update_on_trade(self, data):
    try:
        data1 = json.loads(data)
        logging.info(data)
        # passing new trade to trade table#########################################################################

        exchange = data1['ExchangeSegment']
        token = int(data1['ExchangeInstrumentID'])
        ins_details =get_ins_details(self,exchange,token)

        orderSide = data1['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell')
        tradedQty = data1['LastTradedQuantity']
        qty = tradedQty if (orderSide == 'Buy') else -tradedQty
        netValue = -qty * data1['LastTradedPrice']
        #####################################################################################################################
        trades = dt.Frame([
            [data1['LoginID']],
            [data1['ClientID']], [data1['ExchangeInstrumentID']], [ins_details[4]], [ins_details[3]], [ins_details[6]],
            [ins_details[7]], [ins_details[8]], [orderSide], [data1['AppOrderID']], [data1['OrderType']],
            [tradedQty], [data1['OrderStatus']], [data1['OrderAverageTradedPrice']], [data1['ExchangeTransactTime']],[data1['OrderUniqueIdentifier']],
            [data1['ExchangeOrderID']], [data1['LastTradedPrice']], [qty], [netValue], [ins_details[0]],
            [ins_details[11]], [ins_details[14]], ['openValue']]).to_numpy()

        self.sgTrdSoc.emit(trades)
        self.sgStatusUp.emit(data)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])