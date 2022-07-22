import traceback
import sys
import logging
from PyQt5.QtWidgets import QFileDialog
import numpy as np


def filtr(self):
    try:
        self.smodelT.setFilterFixedString(self.listView.selectedIndexes()[0].data())
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info())


def create_trade_csv(self):
    try:
        name = QFileDialog.getSaveFileName(self, 'Save File')
        np.savetxt(name[0], self.ApiTrade, delimiter=',')
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info())


def get_csv(self):
    np.savetxt(self.csvPath, self.ApiTrade, delimiter=',')
    # self.ApiTrade.tofile("foo.csv", sep=",")


def get_Trades(self):
    try:
        url = self.URL + '/interactive/orders/trades'
        req = requests.request("GET", url, headers=self.IAheaders)
        data_p = req.json()

        if (data_p['result'] != []):
            for j, i in enumerate(data_p['result']):
                try:
                    if (int(i['ExchangeInstrumentID']) in self.cntrcts.keys()):
                        ins = self.cntrcts[(i['ExchangeInstrumentID'])]
                    else:
                        fltr = np.asarray([i['ExchangeInstrumentID']])
                        ah = self.Contract_df[np.in1d(self.Contract_df[:, 2], fltr)][0]
                        ins = [ah[4], ah[3], ah[6], ah[7], ah[8], ah[11], ah[14], ah[9], ah[0], ah[5]]
                        self.cntrcts[int(i['ExchangeInstrumentID'])] = ins
                except:
                    logging.error(sys.exc_info()[1])
                    print(traceback.print_exc())
                    # ins = ['', '', '', '', '']

                if (j == 0):
                    ApiTrade = np.array([[i['ClientID'], i['ExchangeInstrumentID'], ins[0],
                                          ins[1], ins[2], ins[3], ins[4],
                                          i['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell'),
                                          i['AppOrderID'], i['OrderType'], i['LastTradedQuantity'], i['OrderStatus'],
                                          i['OrderAverageTradedPrice'], i['ExchangeTransactTime'],
                                          i['OrderUniqueIdentifier'],
                                          i['ExchangeOrderID']], [i['LastTradedPrice']]])
                else:
                    trades = np.array([[i['ClientID'], i['ExchangeInstrumentID'], ins[0],
                                        ins[1], ins[2], ins[3], ins[4],
                                        i['OrderSide'].replace('BUY', 'Buy').replace('SELL', 'Sell'),
                                        i['AppOrderID'], i['OrderType'], i['LastTradedQuantity'], i['OrderStatus'],
                                        i['OrderAverageTradedPrice'], i['ExchangeTransactTime'],
                                        i['OrderUniqueIdentifier'],
                                        i['ExchangeOrderID']], [i['LastTradedPrice']]])
                    ApiTrade = np.vstack([ApiTrade, trades])
        else:
            ApiTrade = np.empty((0, 16))

        self.modelT = ModelTB(ApiTrade, self.heads)
        # self.TradeW.smodelT = QSortFilterProxyModel()
        self.smodelT.setSourceModel(self.modelT)
        self.tableView.setModel(self.smodelT)

    except:
        print(traceback.print_exc())



def changeFilter(self,a):
    self.smodelT.setFilterFixedString(a)
