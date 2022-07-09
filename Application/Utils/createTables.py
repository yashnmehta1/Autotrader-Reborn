import sys
import traceback
import logging
import numpy as np
import pandas as pd
import datatable as dt
from Application.Views.Models import tableMW
from Application.Views.Models import tableTB
from Application.Views.Models import tableFP
from Application.Views.Models import ProxyModel
from PyQt5.QtCore import QSortFilterProxyModel,Qt


def tables_details_mw(self):
    try:
        self.marketW.heads = ['Token',
                      'Exchange', 'Segment', 'symbol', 'exp', 'strike_price',
                      'C/P', 'Bid', 'Ask', 'LTP', 'CHNG',
                      '%CH', 'CFP', 'DAY', 'NET', 'MTM',
                      'NetValue', 'NetAvg', 'OPEN', 'HIGH', 'LOW',
                      'CLOSE', 'IV', 'tick_size', 'Lot_size', 'FreezQ',
                      'FToken', 'AToken', 'ClientID', 'UserID', 'SerialNo',
                      'openAmt', 'StockName']

        #############################################################################################################
        self.marketW.table = np.zeros((500, 33), dtype=object)
        self.marketW.model = tableMW.ModelPosition(self.marketW.table, self.marketW.heads)
        self.marketW.model.setDta(self.marketW.table)
        self.marketW.smodel = QSortFilterProxyModel()
        self.marketW.smodel.setSourceModel(self.marketW.model)
        self.marketW.tableView.setModel(self.marketW.smodel)

        self.marketW.smodel.setDynamicSortFilter(False)
        self.marketW.smodel.setFilterKeyColumn(3)
        self.marketW.smodel.setFilterCaseSensitivity(False)
        #############################################
        self.marketW.tableView.horizontalHeader().setSectionsMovable(True)
        self.marketW.tableView.verticalHeader().setSectionsMovable(True)
        self.marketW.tableView.verticalHeader().setFixedWidth(30)
        self.marketW.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.marketW.tableView.setDragDropMode(self.marketW.tableView.InternalMove)
        self.marketW.tableView.setDragDropOverwriteMode(False)
        self.marketW.tableView.setColumnWidth(0, 0)
        self.marketW.tableView.setColumnWidth(1, 0)
        self.marketW.tableView.setColumnWidth(2, 0)
        self.marketW.tableView.setColumnWidth(4, 85)
        self.marketW.tableView.setColumnWidth(5, 75)
        self.marketW.tableView.setColumnWidth(6, 40)
        self.marketW.tableView.horizontalHeader().moveSection(28, 0)
    except:
        print(traceback.print_exc())

def tables_details_tb(self):
    try:
        #############################################################################################################
        self.heads = ['UserID',
                      'ClientID', 'ExchangeInstrumentID',  'Instrument','Symbol','Expiry',
                      'Strike_price','C/P','OrderSide', 'AppOrderID','OrderType',
                      'LastTradedQuantity', 'OrderStatus', 'OrderAverageTradedPrice','ExchangeTransactTime', 'OrderUniqueIdentifier',
                      'ExchangeOrderID','TradedPrice']

        self.ApiTrade =  np.empty((20000, 24),dtype=object)
        #############################################################################################################
        self.lastSerialNo = 0
        #############################################
        self.modelT = tableTB.ModelTB(self.ApiTrade,self.heads)
        self.smodelT = QSortFilterProxyModel()
        self.smodelT.setSourceModel(self.modelT)
        self.smodelT.setDynamicSortFilter(False)
        self.smodelT.setFilterKeyColumn(2)
        self.smodelT.setFilterCaseSensitivity(False)
        self.tableView.setModel(self.smodelT)
        self.tableView.horizontalHeader().setSectionsMovable(True)
        self.tableView.verticalHeader().setSectionsMovable(True)
        self.tableView.setDragDropMode(self.tableView.InternalMove)
        self.tableView.setDragDropOverwriteMode(False)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info())



def tables_details_fp(self):
    try:
        #############################################################################################################
        self.heads = ['UserID',
                               'ClientID', 'S_type', 'FolioNo', 'Exchange', 'ExchangeInstrumentID',
                               'StockName', 'symbol', 'Expiry', 'Stike_price', 'C/P',
                               'OpenQty', 'DayQty', 'NetQty', 'NetValue', 'NetAvg',
                               'buyQ', 'AbuyAvg', 'SellQ', 'SellAvg', 'LTP',
                               'MTM', 'lotsize', 'FreezQty', 'OpenValue', 'SerialNo',
                               'DayValue'
                               ]
        self.lastSerialNo = 0
        self.table = np.empty((1000, 27), dtype=object)
        #############################################################################################################
        self.modelFP = tableFP.ModelPosition(self.table, self.heads)
        self.smodelFP = ProxyModel.ProxyModel()
        self.smodelFP.setSourceModel(self.modelFP)
        self.smodelFP.setDynamicSortFilter(False)
        self.smodelFP.setFilterKeyColumn(4)
        self.smodelFP.setFilterCaseSensitivity(False)
        self.tableView.setModel(self.smodelFP)
        self.tableView.horizontalHeader().setSectionsMovable(True)
        self.tableView.verticalHeader().setSectionsMovable(True)
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.rightClickMenu)
        self.tableView.setDragDropMode(self.tableView.InternalMove)
        self.tableView.setDragDropOverwriteMode(False)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])
