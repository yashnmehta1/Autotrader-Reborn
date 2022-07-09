import json
import logging

import numpy as np
import sys
import traceback
import datatable as dt



def update_on_position(self, data):
    try:
        data1 = json.loads(data)

        if (data1['ExchangeSegment'] == 'NSEFO'):
            ins_details = self.fo_contract[int(data1['ExchangeInstrumentID']) - 35000]
        elif (data1['ExchangeSegment'] == 'NSECM'):
            ins_details = self.eq_contract[int(data1['ExchangeInstrumentID'])]
        elif (data1['ExchangeSegment'] == 'NSECD'):
            ins_details = self.cd_contract[int(data1['ExchangeInstrumentID'])]

        rmtm = float((data1['RealizedMTM']).replace(',', ''))
        nv = float(data1['NetValue'].replace(',', ''))
        nv = rmtm if (nv == 0) else nv
        #
        # isRecordExist = False
        clientId = '*****' if ('PRO' in data1['AccountID']) else data1['AccountID']

        if (clientId not in self.openPosDict.keys()):
            self.openPosDict[clientId] = {}

        token = int(data1['ExchangeInstrumentID'])
        if (token not in self.openPosDict[clientId].keys()):
            self.openPosDict[clientId][token] = [0, 0.0]

        # fltr0 = np.asarray([token])



        # filteredArray0 = self.Apipos[np.in1d(self.Apipos[:, 3], fltr0)]
        #
        # if (filteredArray0.size != 0):
        #     fltr0 = np.asarray([data1['ExchangeSegment']])
        #     filteredArray1 = filteredArray0[np.in1d(filteredArray0[:, 2], fltr0)]
        #     if (filteredArray1.size != 0):
        #         fltr0 = np.asarray([data1['AccountID']])  # clientID with a small c
        #         filteredArray2 = filteredArray1[np.in1d(filteredArray1[:, 2], fltr0)]
        #
        #         if (filteredArray2.size != 0):
        #             isRecordExist = True

        qty = int(data1['NetPosition'])
        amt = nv
        # print('amt',amt,type(amt),'qty',qty,type(qty))
        if (qty != 0):
            avgp = amt / qty
        else:
            avgp = 0.0
        mtm = float((data1['MTM']).replace(',', ''))

        pos = dt.Frame(
            [[data1['LoginID']],
            [data1['AccountID']], [data1['ExchangeSegment']], [token],[ins_details[4]],[ins_details[3]],
            [ins_details[6]],[ins_details[7]],[ins_details[8]],[qty], [mtm],
            [0], [rmtm], [nv],[avgp],[ins_details [11]],
            [ins_details[14]],[ins_details[9]],[1000]]).to_numpy()

        self.sgAPIpos.emit(pos)

    except:
        print(sys.exc_info(), 'on_position')
        print(traceback.print_exc())


def update_on_order(self, data):
    try:
        data1 = json.loads(data)
        logging.info(data)
        try:
            if (data1['ExchangeSegment'] == 'NSEFO'):
                ah = self.fo_contract[int(data1['ExchangeInstrumentID']) - 35000]
                # print('ah',ah)
                ins = [ah[4], ah[3], ah[6], ah[7], ah[8], ah[11], ah[14], ah[9], ah[0], ah[5]]
                # self.cntrcts[int(data1['ExchangeInstrumentID'])] = ins
            elif (data1['ExchangeSegment'] == 'NSECM'):
                ah = self.eq_contract[int(data1['ExchangeInstrumentID'])]
                # print('ah',ah)
                ins = [ah[4], ah[3], ah[6], ah[7], ah[8], ah[11], ah[14], ah[9], ah[0], ah[5]]
                # self.cntrcts[int(data1['ExchangeInstrumentID'])] = ins
            elif (data1['ExchangeSegment'] == 'NSECD'):
                ah = self.cd_contract[int(data1['ExchangeInstrumentID'])]
                # print('ah',ah)
                ins = [ah[4], ah[3], ah[6], ah[7], ah[8], ah[11], ah[14], ah[9], ah[0], ah[5]]
                # self.cntrcts[int(data1['ExchangeInstrumentId'])] = ins
        except:
            logging.error(sys.exc_info()[1])
            print(traceback.print_exc())
        orderSide = data1['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell')
        n2darray =dt.Frame( [[data1['ClientID']],
                    [data1['ExchangeInstrumentID']], [ins[0]],[ins[1]], [ins[2]], [ins[3]],
                    [ins[4]],[orderSide],[data1['AppOrderID']], [data1['OrderType']], [data1['OrderStatus']],
                    [data1['OrderQuantity']],[data1['LeavesQuantity']], [data1['OrderPrice']], [data1['OrderStopPrice']],[data1['OrderUniqueIdentifier']],
                    [data1['OrderGeneratedDateTime']],[data1['ExchangeTransactTime']],[data1['CancelRejectReason']], [ins[8]], [ins[9]],
                    [data1['OrderAverageTradedPrice']]]).to_numpy()


        self.sgPendSoc.emit(n2darray)
        self.on_pending_order_work(data1, ins)

        if (data1['OrderStatus'] == 'Filled'):
            self.sgComplOrd.emit([int(data1['ExchangeInstrumentID']), data1['OrderSide'], data1['OrderQuantity'],
                                  float(data1['OrderAverageTradedPrice'].replace(',', '')), data1['AppOrderID'],
                                  data1['OrderUniqueIdentifier'], data1['OrderType']])
        if (data1['OrderStatus'] == 'Rejected'):
            self.sgRejection.emit()
        self.sgStatusUp.emit(data)


    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())


def update_on_trade(self, data):
    try:
        data1 = json.loads(data)
        # print('on_trade',data1)
        logging.info(data)
        # passing new trade to trade table#########################################################################

        if (data1['ExchangeSegment'] == 'NSEFO'):
            ins_details = self.fo_contract[int(data1['ExchangeInstrumentID']) - 35000]
        elif (data1['ExchangeSegment'] == 'NSECM'):
            ins_details = self.eq_contract[int(data1['ExchangeInstrumentID'])]
        elif (data1['ExchangeSegment'] == 'NSECD'):
            ins_details = self.cd_contract[int(data1['ExchangeInstrumentID'])]

        orderSide = data1['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell')

        tradedQty = data1['LastTradedQuantity']
        qty = tradedQty if (orderSide == 'Buy') else -tradedQty
        netValue = qty * data1['LastTradedPrice']

        #####################################################################################################################
        trades = dt.Frame([
            [data1['LoginID']],
            [data1['ClientID']], [data1['ExchangeInstrumentID']], [ins_details[4]], [ins_details[3]], [ins_details[6]],
            [ins_details[7]], [ins_details[8]], [orderSide], [data1['AppOrderID']], [data1['OrderType']],
            [tradedQty], [data1['OrderStatus']], [data1['OrderAverageTradedPrice']], [data1['ExchangeTransactTime']],
            [data1['OrderUniqueIdentifier']],
            [data1['ExchangeOrderID']], [data1['LastTradedPrice']], [qty], [netValue], [ins_details[0]],
            [ins_details[11]], [ins_details[14]], ['openValue']]).to_numpy()

        self.sgTrdSoc.emit(trades)
        self.sgStatusUp.emit(data)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])



