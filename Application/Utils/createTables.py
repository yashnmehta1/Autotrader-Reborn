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
from Application.Views.Models import tableNP
from Application.Views.Models import tableOrder
from Application.Views.Models import tableO
from PyQt5.QtCore import QSortFilterProxyModel,Qt
from Application.Views.Models import ProxyModel

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


def tables_details_mw_basic(self):
    try:
        self.marketWB.heads = ['Token',
                      'Exchange', 'Segment', 'symbol', 'exp', 'strike_price',
                      'C/P', 'Bid', 'Ask', 'LTP', 'CHNG',
                      '%CH', 'OPEN', 'HIGH', 'LOW', 'CLOSE',
                      'IV', 'tick_size', 'Lot_size', 'FreezQ', 'FToken',
                      'AToken', 'SerialNo','StockName']

        #############################################################################################################
        self.marketWB.table = np.zeros((500, 24), dtype=object)
        self.marketWB.model = tableMW.ModelPosition(self.marketWB.table, self.marketWB.heads)
        self.marketWB.model.setDta(self.marketWB.table)
        self.marketWB.smodel = QSortFilterProxyModel()
        self.marketWB.smodel.setSourceModel(self.marketWB.model)
        self.marketWB.tableView.setModel(self.marketWB.smodel)

        self.marketWB.smodel.setDynamicSortFilter(False)
        self.marketWB.smodel.setFilterKeyColumn(3)
        self.marketWB.smodel.setFilterCaseSensitivity(False)
        #############################################
        self.marketWB.tableView.horizontalHeader().setSectionsMovable(True)
        self.marketWB.tableView.verticalHeader().setSectionsMovable(True)
        self.marketWB.tableView.verticalHeader().setFixedWidth(30)
        self.marketWB.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.marketWB.tableView.setDragDropMode(self.marketWB.tableView.InternalMove)
        self.marketWB.tableView.setDragDropOverwriteMode(False)
        self.marketWB.tableView.setColumnWidth(0, 0)
        self.marketWB.tableView.setColumnWidth(1, 0)
        self.marketWB.tableView.setColumnWidth(2, 0)
        self.marketWB.tableView.setColumnWidth(4, 85)
        self.marketWB.tableView.setColumnWidth(5, 75)
        self.marketWB.tableView.setColumnWidth(6, 40)
        self.marketWB.tableView.horizontalHeader().moveSection(28, 0)
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
        self.smodelT.setFilterKeyColumn(3)
        self.smodelT.setFilterCaseSensitivity(False)
        self.tableView.setModel(self.smodelT)
        self.tableView.horizontalHeader().setSectionsMovable(True)
        self.tableView.verticalHeader().setSectionsMovable(True)
        self.tableView.setDragDropMode(self.tableView.InternalMove)
        self.tableView.setDragDropOverwriteMode(False)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info())

def tables_details_np(self):
    try:
        #############################################################################################################

        self.heads = ['UserID',
                      'ClientID','Segment','ExchangeInstrumentID', 'TradingSymbol', 'symbol',
                      'Expiry','Stike_price','C/P','Quantity', 'MTM',
                      'LTP', 'RealizedMTM','NetAmount','AvgPrice','lotsize',
                      'maxQ','AssetToken','SerialNo','OpenQty','OpenAmt',
                      'DayQ','DayAmt']

        self.Apipos =  np.zeros((1000, 23),dtype=object)
        self.sectionDict={}
        for j,i in enumerate(self.heads):
            self.sectionDict[j]=i
        #############################################################################################################

        #############################################
        self.modelP = tableNP.ModelPosition(self.Apipos,self.heads)
        self.smodelP = QSortFilterProxyModel()
        self.smodelP.setSourceModel(self.modelP)

        self.smodelP.setDynamicSortFilter(False)
        self.smodelP.setFilterKeyColumn(4)
        self.smodelP.setFilterCaseSensitivity(False)

        self.tableView.setModel(self.smodelP)


        self.tableView.horizontalHeader().setSectionsMovable(True)
        self.tableView.verticalHeader().setSectionsMovable(True)
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.tableView.setStyleSheet(
        #     'background-color: rgb(50, 50, 50);selection-background-color: transparent;color: rgb(245, 245, 245);')
        self.tableView.setDragDropMode(self.tableView.InternalMove)
        # self.tableView.horizontalHeader().setStyleSheet('color : black')
        self.tableView.setDragDropOverwriteMode(False)
        # a=QtWidgets.QtableView.horizontalHeader()
        # a.moveSection()
        self.tableView.setColumnWidth(0,0)
        self.tableView.setColumnWidth(2,0)
        self.tableView.setColumnWidth(3,0)
        self.tableView.setColumnWidth(14,0)
        self.tableView.setColumnWidth(15,0)
        self.tableView.setColumnWidth(16,0)

        # self.tableView.clicked.connect(self.tvs6)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])

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
        self.table = np.zeros((1000, 27), dtype=object)
        #############################################################################################################
        self.modelFP = tableFP.ModelPosition(self.table, self.heads)
        self.smodelFP = QSortFilterProxyModel()
        self.smodelFP.setSourceModel(self.modelFP)
        self.smodelFP.setDynamicSortFilter(False)
        self.smodelFP.setFilterKeyColumn(3)
        self.smodelFP.setFilterCaseSensitivity(False)



        self.tableView.setModel(self.smodelFP)
        self.tableView.horizontalHeader().setSectionsMovable(True)
        self.tableView.verticalHeader().setSectionsMovable(True)
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.setDragDropMode(self.tableView.InternalMove)
        self.tableView.setDragDropOverwriteMode(False)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])


def tables_details_ob(self):
    try:
        #############################################################################################################

        self.ApiOrder = np.zeros((15000,25),dtype=object)
        self.heads = ['AppOrderID',
                      'ClientID','ExchangeInstrumentID', 'Instrument','Symbol','Expiry',
                      'Strike_price','C/P','OrderSide', 'OrderType','OrderStatus',
                        'OrderQuantity', 'LeavesQuantity', 'OrderPrice','OrderStopPrice','OrderUniqueIdentifier',
                      'OrderGeneratedDateTime','ExchangeTransactTime','CancelRejectReason','Exchange','Instrument',
                      'AvgPrice',"Qty1",'ProductType','validity']

        #############################################################################################################

        #############################################
        self.modelO = tableOrder.ModelOB(self.ApiOrder,self.heads)
        self.smodelO = QSortFilterProxyModel()
        self.smodelO.setSourceModel(self.modelO)
        self.tableView.setModel(self.smodelO)
        self.smodelO.setFilterCaseSensitivity(True)
        self.smodelO.setFilterKeyColumn(1)



        self.tableView.horizontalHeader().setSectionsMovable(True)
        self.tableView.verticalHeader().setSectionsMovable(True)
        self.tableView.setDragDropMode(self.tableView.InternalMove)
        self.tableView.setDragDropOverwriteMode(False)
        self.tableView.verticalHeader().setMaximumSectionSize(8)
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
    except:
        logging.error(sys.exc_info()[1])



def tables_details_pob(self):
    try:
        self.ApiOrder = np.zeros((1000,25),dtype=object)
        self.heads = ['AppOrderID',
                      'ClientID','ExchangeInstrumentID', 'Instrument','Symbol','Expiry',
                      'Strike_price','C/P','OrderSide',  'OrderType','OrderStatus',
            'OrderQuantity', 'LeavesQuantity', 'OrderPrice','OrderStopPrice','OrderUniqueIdentifier',
              'OrderGeneratedDateTime','ExchangeTransactTime','CancelRejectReason','Exchange','Instrument',
                      'AvgPrice', 'Qty1', 'ProductType','validity'] #productType validity
        self.visibleColumns = len(self.heads)

        #############################################################################################################

        #############################################
        self.modelO = tableO.ModelOB(self.ApiOrder,self.heads,False)
        self.smodelO = QSortFilterProxyModel()
        self.smodelO.setSourceModel(self.modelO)
        self.tableView.setModel(self.smodelO)
        self.smodelO.setDynamicSortFilter(False)
        self.smodelO.setFilterCaseSensitivity(False)
        self.smodelO.setFilterKeyColumn(1)

        self.tableView.horizontalHeader().setSectionsMovable(True)
        self.tableView.verticalHeader().setSectionsMovable(True)
        self.tableView.setDragDropMode(self.tableView.InternalMove)
        self.tableView.setDragDropOverwriteMode(False)
        self.tableView.verticalHeader().setMaximumSectionSize(8)
        #self.tableView.setColumnHidden(1, True)

        # self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)

    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])

