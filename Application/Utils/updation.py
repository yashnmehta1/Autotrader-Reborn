import sys
import traceback
import numpy as np
import  datatable as dt
import threading
import logging
from Application.Services.Xts.Api.servicesMD import subscribeToken
from Application.Utils.supMethods import get_ins_details


def updateCashIndex(self, token, ltp):
    # print('in updateCashIndex',token)
    if (token == 26000):
        self.PrcNFT.setText('%.2f' % ltp)
    elif (token == 26001):
        self.PrcBNF.setText('%.2f' % ltp)

    elif (token == 26002):
        self.PrcVIX.setText('%.2f' % ltp)




def UpdateLTP_MW(self, a):
    try:
        # print('in marketwatch update' ,a)
        if (self.marketW.table.size != 0):
            #print("1")
            x = (np.unique(self.marketW.table[:, 0]))

            if (a['Token'] in x):
             #   print("2")
                fltr = np.asarray([a['Token']])
                self.marketW.model.dta1 = self.marketW.table[:, [7, 8, 9]].tolist()
                x = self.marketW.table[np.in1d(self.marketW.table[:, 0], fltr), 30]
                editableList = [9, 7, 8, 10, 11, 15, 18, 19, 20, 21]
                for i in x:
                    netValue = self.marketW.table[i, 16]
                    qty = self.marketW.table[i, 14]
                    mtm = (qty * a['LTP']) + netValue
                    ch = a['LTP'] - a['CLOSE']

                    self.marketW.table[i, editableList] = [a['LTP'], a['Bid'], a['Ask'], ch, a['%CH'], mtm,a['OPEN'],a['HIGH'],a['LOW'],a['CLOSE']]
                    for j in editableList:
                        ind = self.marketW.model.index(i, j)
                        # ind1 = self.marketW.model.index(i,1)
                        self.marketW.model.dataChanged.emit(ind, ind)
                # print(self.marketW.table)
        totaolmtm=np.sum(self.marketW.table[:,15])
        self.label.setText('%.2f'%totaolmtm)

    except:

        print(traceback.print_exc())

def UpdateLTP_MW_basic(self, a):
    try:
        # print('in marketwatch update' ,a)
        if (self.marketWB.table.size != 0):
            x = (np.unique(self.marketWB.table[:, 0]))

            if (a['Token'] in x):
                fltr = np.asarray([a['Token']])
                self.marketWB.model.dta1 = self.marketWB.table[:, [7, 8, 9]].tolist()
                x = self.marketWB.table[np.in1d(self.marketWB.table[:, 0], fltr), 22]
                editableList = [9, 7, 8, 10, 11, 12, 13, 14, 15]
                for i in x:
                    netValue = self.marketWB.table[i, 16]
                    qty = self.marketWB.table[i, 14]
                    mtm = (qty * a['LTP']) + netValue
                    ch = a['LTP'] - a['CLOSE']

                    self.marketWB.table[i, editableList] = [a['LTP'], a['Bid'], a['Ask'], ch, a['%CH'],a['OPEN'],a['HIGH'],a['LOW'],a['CLOSE']]
                    for j in editableList:
                        ind = self.marketWB.model.index(i, j)
                        # ind1 = self.marketWB.model.index(i,1)
                        self.marketWB.model.dataChanged.emit(ind, ind)
                # print(self.marketWB.table)

    except:

        print(traceback.print_exc())

def UpdateLTP_NP(self, data):
    try:
        # print('in positon up' ,data)
        if (self.NetPos.Apipos.size != 0):
            #print("1")
            x = (np.unique(self.NetPos.Apipos[:, 3]))
            # print("NP : ",x)
            if (data['Token'] in x):
                fltr = np.asarray([data['Token']])
                #self.marketW.model.dta1 = self.NetPos.Apipos[:, [7, 8, 9]].tolist()
                serialNos = self.NetPos.Apipos[np.in1d(self.NetPos.Apipos[:, 3], fltr), 18]
                editableList = [11, 10]

                for i in serialNos:
                    netValue = self.NetPos.Apipos[i, 13]
                    qty = self.NetPos.Apipos[i, 9]
                    mtm = (qty * data['LTP']) + netValue
                    self.NetPos.Apipos[i, editableList] = [data['LTP'],  mtm]
                    for j in editableList:
                        ind = self.NetPos.modelP.index(i, j)
                        self.NetPos.modelP.dataChanged.emit(ind, ind)

    except:
        print(traceback.print_exc())


def UpdateLTP_FP(self, data):
    try:
        # print('in positon up' ,data)
        if (self.FolioPos.table.size != 0):
            # print("1")
            x = (np.unique(self.FolioPos.table[:, 5]))
            # print("NP : ",x)
            if (data['Token'] in x):
                fltr = np.asarray([data['Token']])
                # self.marketW.model.dta1 = self.NetPos.table[:, [7, 8, 9]].tolist()
                serialNos = self.FolioPos.table[np.in1d(self.FolioPos.table[:, 5], fltr), 25]  # 30 serial no
                editableList = [20, 21]

                for i in serialNos:
                    netValue = self.FolioPos.table[i, 14]
                    qty = self.FolioPos.table[i, 13]
                    mtm = (qty * data['LTP']) + netValue
                    self.FolioPos.table[i, editableList] = [data['LTP'], mtm]
                    for j in editableList:
                        ind = self.FolioPos.modelFP.index(i, j)
                        self.FolioPos.modelFP.dataChanged.emit(ind, ind)

    except:
        print(traceback.print_exc())


def updateGetPosition_NP(self,pos, rowNo):
    self.NetPos.Apipos[rowNo, :] = pos
    self.NetPos.lastSerialNo += 1
    self.NetPos.modelP.lastSerialNo += 1
    self.NetPos.modelP.insertRows()
    self.NetPos.modelP.rowCount()

# advance market watch -  get
def updateGetPosition_AMW(self,pos):
    try:

        """           
        please add scenario where record already exist
        """

        i =pos
        exchange = i[2]
        token = i[3]
        ins_details = get_ins_details(self,exchange,token)

        assetToken = ins_details[9]
        anm = dt.Frame(
            [[token],
            [exchange], [ins_details[5]], [ins_details[3]],[ins_details[6]], [ins_details[7]],
            [ins_details[8]], [0.0], [0.00], [0.00], ['+0.00'],
             ['+0.00'], [i[19]],[i[21]], [i[9]], [0.0],
             [i[13]], [0.0],[0.0], [0.0], [0.0],
             [0.0], [0.0],[ins_details[10]], [ins_details[11]], [ins_details[14]],
             [ins_details[17]], [assetToken],[i[1]], [self.userID], [self.marketW.lastSerialNo],
             [i[20]],[ins_details[4]]
            ]).to_numpy()

        self.marketW.table[self.marketW.lastSerialNo, :] = anm
        self.marketW.lastSerialNo +=1
        self.marketW.model.lastSerialNo += 1

        self.marketW.model.rowCount()
        self.marketW.model.insertRows()
        self.marketW.model.dta1.append([0, 0, 0])

        self.marketW.model.color.append(['transparent', 'transparent', 'transparent'])
        ind = self.marketW.model.index(0, 0)
        ind1 = self.marketW.model.index(0, 31)

        self.marketW.model.dataChanged.emit(ind, ind1)
        th1 = threading.Thread(target=subscribeToken,
                               args=(self,token, exchange, 1501))
        th1.start()

    except:
        print(traceback.print_exc(), sys.exc_info())

# adavance market watch - update
def update_Position_socket_MW(self,pos):
    for i in pos:
        isRecordExist = False
        fltr0 = np.asarray([i[3]])
        filteredArray0 =  self.marketW.table[np.in1d(self.marketW.table[:, 0], fltr0)]
        if (filteredArray0.size != 0):
            fltr = np.asarray([i[2]])
            filteredArray1 =  filteredArray0[np.in1d(filteredArray0[:, 1], fltr)]

            if (filteredArray1.size != 0):
                fltr = np.asarray([i[1]])
                filteredArray2 = filteredArray1[np.in1d(filteredArray1[:, 28], fltr)]

                if (filteredArray2.size != 0):
                    isRecordExist = True

        if(isRecordExist ==False):
            try:
                exchange = i[2]
                token = i[3]
                if(exchange == 'NSEFO'):
                    ins_detail = self.fo_contract[token - 35000]
                elif(exchange == 'NSECD'):
                    ins_detail = self.cd_contract[token]
                elif(exchange == 'NSECM'):
                    ins_detail = self.eq_contract[token]
                assetToken = ins_detail[9]
                anm = dt.Frame(
                    [[token],
                        [exchange], [ins_detail[5]], [ins_detail[3]],[ins_detail[6]], [ins_detail[7]],
                        [ins_detail[8]], [0.0], [0.00], [0.00], ['+0.00'],
                     ['+0.00'], [0],[0], [i[4]], [0.0],
                     [i[8]], [0.0],[0.0], [0.0], [0.0],
                     [0.0], [0.0],[0.0], [0], [0],
                     [0], [assetToken],[i[1]], [self.userID], [self.marketW.lastSerialNo],[i[3]],[ins_detail[4]]
                    ]).to_numpy()



                self.marketW.table[self.marketW.lastSerialNo, :] = anm
                self.marketW.lastSerialNo +=1
                self.marketW.model.lastSerialNo += 1

                self.marketW.model.rowCount()
                self.marketW.model.insertRows()
                self.marketW.model.dta1.append([0, 0, 0])



                self.marketW.model.color.append(['transparent', 'transparent', 'transparent'])

                ind = self.marketW.model.index(0, 0)
                ind1 = self.marketW.model.index(0, 31)
                self.marketW.model.dataChanged.emit(ind, ind1)
                th1 = threading.Thread(target=self.subscription_feed,
                                       args=(token, exchange, 1501))
                th1.start()

            except:
                print(traceback.print_exc(), sys.exc_info())

        else:
            print('updateposseockt filteredArray2',filteredArray2)
            serialNo = filteredArray2[0][30]


            print('serialNo',serialNo)
            if(self.Source == 'TWSAPI'):
                openQty = self.marketW.table[serialNo,12]
                day =  i[21] - openQty
                net =   i[9]
                netValue =  i[13]

            elif(self.Source == 'WEBAPI'):
                openValue = self.marketW.table[serialNo,31]
                openQty = self.marketW.table[serialNo,12]
                day =  i[9]
                net =   i[9] + openQty
                netValue =  i[13] + openValue

            self.marketW.table[serialNo,[13,14,16]] = [day,net,netValue]

            ind = self.marketW.model.index(0, 0)
            ind1 = self.marketW.model.index(0, 31)
            self.marketW.model.dataChanged.emit(ind, ind1)
    print('update get posion finished')

def update_Position_Socket_NP(self,pos):
    for i in pos:
        isRecordExist = False
        fltr0 = np.asarray([i[3]])
        print('update_Position_Socket_NP',i)
        filteredArray0 =  self.NetPos.Apipos[np.in1d(self.NetPos.Apipos[:, 3], fltr0)]

        if (filteredArray0.size != 0):
            fltr = np.asarray([i[2]])
            filteredArray1 =  filteredArray0[np.in1d(filteredArray0[:, 2], fltr)]

            if (filteredArray1.size != 0):
                fltr = np.asarray([i[1]])
                filteredArray2 = filteredArray1[np.in1d(filteredArray1[:, 1], fltr)]

                if (filteredArray2.size != 0):
                    isRecordExist = True

        if(isRecordExist ==False):
            try:
                exchange = i[2]
                token = i[3]

                print('pos',pos)
                print('pos[0]',pos[0])

                pos[0,18] = self.NetPos.lastSerialNo

                self.NetPos.Apipos[self.NetPos.lastSerialNo, :] = pos
                self.NetPos.lastSerialNo +=1
                self.NetPos.modelP.lastSerialNo += 1

                self.NetPos.modelP.rowCount()
                self.NetPos.modelP.insertRows()
                self.NetPos.modelP.dta1.append([0, 0, 0])

                ind = self.NetPos.modelP.index(0, 0)
                ind1 = self.NetPos.modelP.index(0, 1)
                self.NetPos.modelP.dataChanged.emit(ind, ind1)

                th1 = threading.Thread(target=self.subscription_feed,
                                       args=(token, exchange, 1501))
                th1.start()

            except:
                print(traceback.print_exc(), sys.exc_info())

        else:
            print('updateposseockt filteredArray2',filteredArray2)
            serialNo = filteredArray2[0][18]


            print('serialNo',serialNo)
            if(self.Source == 'TWSAPI'):
                openValue = i[20]
                openQty = i[19]
                day =  i[9] - openQty
                net =   i[9]
                netValue =  i[13]

            elif(self.Source == 'WEBAPI'):
                openValue = i[20]
                openQty = i[19]
                day =  i[9]
                net =   i[9] + openQty
                netValue =  i[13]+openValue

            self.NetPos.Apipos[serialNo,[21,9,13]] = [day,net,netValue]

            ind = self.NetPos.modelP.index(0, 0)
            ind1 = self.NetPos.modelP.index(0, 1)
            self.NetPos.modelP.dataChanged.emit(ind, ind1)
    print('update get posion finished')

def updateOpenPosition(self,openPosArray):
    for i in openPosArray:
        isRecordExist = False
        fltr0 = np.asarray([i[1]])
        filteredArray0 =  self.marketW.table[np.in1d(self.marketW.table[:, 0], fltr0)]
        if (filteredArray0.size != 0):
            fltr = np.asarray([i[5]])
            filteredArray1 =  filteredArray0[np.in1d(filteredArray0[:, 1], fltr)]
            # print('openpos filteredArray1 ', filteredArray1[0,28])

            if (filteredArray1.size != 0):
                fltr = np.asarray([i[0]])
                filteredArray2 = filteredArray1[np.in1d(filteredArray1[:, 28], fltr)]
                # print('openpos filteredArray2 ', filteredArray2)

                if (filteredArray2.size != 0):
                    isRecordExist = True

        if(isRecordExist ==False):
            try:
                exchange = i[5]
                token = i[1]
                if(exchange == 'NSEFO'):
                    ins_detail = self.fo_contract[token - 35000]
                elif(exchange == 'NSECD'):
                    ins_detail = self.cd_contract[token]
                elif(exchange == 'NSECM'):
                    ins_detail = self.eq_contract[token]

                assetToken = ins_detail[9]
                anm = dt.Frame(
                    [[token],
                        [exchange], [ins_detail[5]], [ins_detail[3]],[ins_detail[6]], [ins_detail[7]],
                        [ins_detail[8]], [0.0], [0.00], [0.00], ['+0.00'],
                        ['+0.00'], [i[2]],[0], [0], [0.0],
                         [0.0], [0.0],[0.0], [0.0], [0.0],
                         [0.0], [0.0],[0.0], [0], [0],
                     [0], [assetToken],[i[0]], [self.userID], [self.marketW.lastSerialNo],
                     [i[3]],[ins_detail[4]]
                    ]).to_numpy()
                self.marketW.table[self.marketW.lastSerialNo, :] = anm
                self.marketW.lastSerialNo += 1
                self.marketW.model.lastSerialNo += 1


                self.marketW.model.rowCount()
                self.marketW.model.insertRows()
                self.marketW.model.dta1.append([0, 0, 0])

                self.marketW.model.color.append(['transparent', 'transparent', 'transparent'])
                # self.marketW.smodel.sort(self.marketW.sortColumn, self.marketW.sortOrder)

                ind = self.marketW.model.index(0, 0)
                ind1 = self.marketW.model.index(0, 31)
                self.marketW.model.dataChanged.emit(ind, ind1)

                th1 = threading.Thread(target=self.subscription_feed,
                                       args=(token, exchange, 1501))
                th1.start()

            except:
                print(traceback.print_exc(), sys.exc_info())

        else:
            pass
    print('update open posion finished')

def updateGetTradeApi(self,data):
    try:
        self.lastSerialNo = 0
        self.modelT.lastSerialNo = 0
        for i  in data:
            self.ApiTrade[self.lastSerialNo] = i
            self.modelT.insertRows()
            self.modelT.lastSerialNo += 1
            self.lastSerialNo += 1
            self.modelT.rowCount()

        # ind = self.modelT.index(0, 0)
        # ind1 = self.modelT.index(0, 1)
        # self.modelT.dataChanged.emit(ind, ind1)

    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info())

def updateSocketTB(self,trd):
    try:
        self.TradeW.ApiTrade[self.TradeW.modelT.lastSerialNo,:] =  trd
        self.TradeW.lastSerialNo +=1
        self.TradeW.modelT.lastSerialNo +=1
        self.TradeW.modelT.insertRows()
        self.TradeW.modelT.rowCount()

        if(self.isVisible()):
            ind = self.TradeW.modelT.index(0, 0)
            ind1 = self.TradeW.modelT.index(0, 1)
            self.TradeW.modelT.dataChanged.emit(ind, ind1)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info())

def updateGetTradeTable(self,trade,rowNo):
    self.TradeW.ApiTrade[rowNo, :] = trade
    self.TradeW.lastSerialNo += 1
    self.TradeW.modelT.lastSerialNo += 1
    self.TradeW.modelT.rowCount()
    self.TradeW.modelT.insertRows()


def updateGetOrderTable(self,order,rowNo):
    self.OrderBook.ApiOrder[rowNo, :] = order
    self.OrderBook.lastSerialNo += 1
    self.OrderBook.modelO.lastSerialNo += 1
    self.OrderBook.modelO.rowCount()
    self.OrderBook.modelO.insertRows()
    #############################################################################################


def updateGetPendingOrderTable(self,order,rowNo):

    """
    first flush data
    then
    restore
    """

    self.PendingW.ApiOrder = data
    self.PendingW.modelO = ModelOB(self.PendingW.ApiOrder,self.PendingW.heads)
    self.PendingW.smodelO.setSourceModel(self.PendingW.modelO)
    self.PendingW.tableView.setModel(self.PendingW.smodelO)
    self.PendingW.rcount = self.PendingW.ApiOrder.shape[0]


###############################################
def pendingW_datachanged_full(self):
    ind = self.PendingW.modelO.index(0, 0)
    ind1 = self.PendingW.modelO.index(0, 1)
    self.PendingW.modelO.dataChanged.emit(ind, ind1)
def orderW_datachanged_full(self):
    ind = self.OrderBook.modelO.index(0, 0)
    ind1 = self.OrderBook.modelO.index(0, 1)
    self.OrderBook.modelO.dataChanged.emit(ind, ind1)
def tradeW_datachanged_full(self):
    ind = self.TradeW.modelT.index(0, 0)
    ind1 = self.TradeW.modelT.index(0, 1)
    self.TradeW.modelT.dataChanged.emit(ind, ind1)
def PosionW_datachanged_full(self):
    ind = self.NetPos.modelP.index(0, 0)
    ind1 = self.NetPos.modelO.index(0, 1)
    self.NetPos.modelP.dataChanged.emit(ind, ind1)
def marketW_datachanged_full(self):
    ind = self.OrderBook.modelO.index(0, 0)
    ind1 = self.OrderBook.modelO.index(0, 1)
    self.OrderBook.modelO.dataChanged.emit(ind, ind1)





# def updateGetADVMWTable(self,pos, rowNo):
#     self.marketW.table[rowNo, :] = pos
#     self.marketW.lastSerialNo += 1
#     self.marketW.model.lastSerialNo += 1
#     self.marketW.model.insertRows()
#     self.marketW.model.rowCount()



#
# def updateGetPosition(self,ApiPos):
#     for i in ApiPos:
#         isRecordExist = False
#         fltr0 = np.asarray([i[3]])
#         filteredArray0 =  self.marketW.table[np.in1d(self.marketW.table[:, 0], fltr0)]
#
#         if (filteredArray0.size != 0):
#             fltr = np.asarray([i[2]])
#             filteredArray1 =  filteredArray0[np.in1d(filteredArray0[:, 1], fltr)]
#             # print('get pos filteredArray1',filteredArray1,[i[1]])
#             if (filteredArray1.size != 0):
#                 fltr = np.asarray([i[1]])
#                 filteredArray2 = filteredArray1[np.in1d(filteredArray1[:, 28], fltr)]
#                 if (filteredArray2.size != 0):
#                     isRecordExist = True
#
#         if(isRecordExist ==False):
#             try:
#                 exchange = i[2]
#                 token = i[3]
#                 if(exchange == 'NSEFO'):
#                     ins_detail = self.fo_contract[token - 35000]
#                 elif(exchange == 'NSECD'):
#                     ins_detail = self.cd_contract[token]
#                 elif(exchange == 'NSECM'):
#                     ins_detail = self.eq_contract[token]
#                 assetToken = ins_detail[9]
#                 anm = dt.Frame(
#                     [[token],
#                     [exchange], [ins_detail[5]], [ins_detail[3]],[ins_detail[6]], [ins_detail[7]],
#                     [ins_detail[8]], [0.0], [0.00], [0.00], ['+0.00'],
#                      ['+0.00'], [0],[i[4]], [i[4]], [0.0],
#                      [i[8]], [0.0],[0.0], [0.0], [0.0],
#                      [0.0], [0.0],[0.0], [0], [0],
#                      [0], [assetToken],[i[1]], [self.userID], [self.marketW.lastSerialNo],
#                      [0],[ins_detail[4]]
#                     ]).to_numpy()
#
#                 self.marketW.table[self.marketW.lastSerialNo, :] = anm
#                 self.marketW.lastSerialNo +=1
#                 self.marketW.model.lastSerialNo += 1
#
#                 self.marketW.model.rowCount()
#                 self.marketW.model.insertRows()
#                 self.marketW.model.dta1.append([0, 0, 0])
#
#                 self.marketW.model.color.append(['transparent', 'transparent', 'transparent'])
#                 ind = self.marketW.model.index(0, 0)
#                 ind1 = self.marketW.model.index(0, 31)
#
#                 self.marketW.model.dataChanged.emit(ind, ind1)
#                 th1 = threading.Thread(target=self.subscription_feed,
#                                        args=(token, exchange, 1501))
#                 th1.start()
#
#             except:
#                 print(traceback.print_exc(), sys.exc_info())
#
#         else:
#
#             serialNo = filteredArray2[0][30]
#
#             if(self.source == 'TWSAPI'):
#                 # openValue = filteredArray2[serialNo,31]
#                 openQty = self.marketW.table[serialNo,12]
#                 day =  i[4] - openQty
#                 net =   i[4]
#                 netValue =  i[8]
#
#             elif(self.source == 'WEBAPI'):
#                 openValue = self.marketW.table[serialNo,31]
#                 openQty = self.marketW.table[serialNo,12]
#                 day =  i[4]
#                 net =   i[4] + openQty
#                 netValue =  i[8] + openValue
#
#             print('openpos update',day,net)
#             self.marketW.table[serialNo,[13,14,16]] = [day,net,netValue]
#
#             ind = self.marketW.model.index(0, 0)
#             ind1 = self.marketW.model.index(0, 31)
#             self.marketW.model.dataChanged.emit(ind, ind1)
#     print('update get posion finished')
#
