import time
import traceback
from bs4 import BeautifulSoup


import numpy as np
import pandas as pd
import datatable as dt
import requests
import sys
from configReader import readConfig1
import json
from database_conn import *
import numpy
import os
import datetime


loc1 = os.getcwd().split('\Application')
contractDir = loc1[0] + '\\Resourses\\ContractMasters\\contract_df.csv'
# print()

def segwork( a):
    if (a == 3.0 or a == 4.0):
        aa= 'O'
    else:
        aa= 'F'

    return aa


def otwork( a):
    if (a == 3):
        return 'CE'
    elif (a == 4):
        return 'PE'
    else:
        return ' '


def spwork( a):
    if(a == ' '):
        return ' '
    elif (isinstance(a, float) or isinstance(a, int)):
        return '%.2f' % a


def expwork(a):
    try:
        if isinstance(a, int) or isinstance(a, float):
            aa = ' '
        else:
            aa = a.replace('-', '')[0:8]
    except:
        print(sys.exc_info(),'exp a: ',type(a))
    return aa


def assetTokenWork1( a,b):
    if(a==-1):
        if(b=='Nifty 50'):
            return '26000'
        elif(b=='Nifty Bank'):
            return  '26001'
        elif (b == 'Nifty Fin Service'):
            return '26002'

    else:

        a = str(a)
        aa = a.replace('110010000', '')
        aaa = aa.replace('11001000', '')
        return aaa




def assetTokenWork( a):

    a = str(a)
    # print(a,b)


    aa = a.replace('110010000', '')
    aaa = aa.replace('11001000', '')
    return aaa


def get_contract_master_FNO(validation):
    try:

        if(validation==True):
            mheaders, iheaders, mToken, iToken, apiip, userid, source = readConfig1()
            sub_url = apiip + '/marketdata/instruments/master'
            payloadsub = {"exchangeSegmentList": ["NSEFO"]}
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("POST", sub_url, data=payloadsubjson, headers=mheaders)
            data_p = req.json()
            abc = data_p['result']
            # print(abc)




            with open ('../Resourses/contractFO_raw.txt','w') as f:
                f.write(abc)
            f.close()

            contractFo1 = pd.read_csv('../Resourses/contractFO_raw.txt', header=None, sep='|'
                                      ,names=['ExchangeSegment', 'Token', 'instrument_type1', 'symbol', 'Stock_name',
                                                'instrument_type', ' NameWithSeries', 'InstrumentID', 'PriceBand.High',
                                                'PriceBand.Low','FreezeQty', 'tick_size', 'lot_size', 'Multiplier',
                                                 'UnderlyingInstrumentId','IndexName','ContractExpiration', 'strike1', 'OptionType'])

            contractFo1 = contractFo1[contractFo1['instrument_type1']!=4]

            contractFo1['Exchange'] = 'NSEFO'
            # contractFo1['Segment'] = 'F'
            contractFo1['Segment'] = contractFo1['OptionType'].apply(segwork)
            contractFo1['option_type'] = contractFo1['OptionType'].apply(otwork)
            contractFo1['strike1'] = contractFo1['strike1'].fillna(' ')
            contractFo1['strike_price'] = contractFo1['strike1'].apply(spwork)
            contractFo1['exp'] = contractFo1['ContractExpiration'].apply(expwork)
            # contractFo1['asset_token'] = contractFo1['UnderlyingInstrumentId'].apply(assetTokenWork)
            contractFo1['asset_token'] = contractFo1[['UnderlyingInstrumentId','IndexName']].apply(lambda x: assetTokenWork1(x.UnderlyingInstrumentId, x.IndexName), axis=1)
            # contractFo1['asset_token'] = contractFo1['IndexName'] if(contractFo1['instrument_type'][:-3]=='IDX')  else contractFo1['asset_token']

            contractFo1['FreezeQty'] = contractFo1['FreezeQty'] - 1
            cndf1 = contractFo1[['Exchange','Segment','Token', 'symbol', 'Stock_name', 'instrument_type', 'exp', 'strike_price', 'option_type',
                                 'asset_token', 'tick_size', 'lot_size', 'strike1','Multiplier','FreezeQty']]
            cndfo = dt.Frame(cndf1)
            print(cndf1)
            print('contract master downloaded')


            payloadsub = {"exchangeSegmentList": ["NSECM"]}
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("POST", sub_url, data=payloadsubjson, headers=mheaders)
            data_p = req.json()

            abc = data_p['result']
            with open('../Resourses/ContractEQ', 'w') as f:
                f.write(abc)
            f.close()
            contractEq1 = pd.read_csv('../Resourses/ContractEQ', header=None, sep='|',index_col=False
                                      ,names=['ExchangeSegment','Token','InstrumentType','symbol','Stock_name','exp',' NameWithSeries','InstrumentID','PriceBand.High','PriceBand.Low',' FreezeQty','tick_size','lot_size','Multiplier'])

            # print(contractEq1)

            contractEq1['Multiplier'] = 1
            contractEq1['Exchange'] = 'NSECM'
            contractEq1['Segment'] = 'E'
            contractEq1['option_type'] = 'E'
            contractEq1['strike_price'] ='E'

            cndEq = contractEq1[['Exchange','Segment','Token', 'Stock_name','symbol','exp','strike_price','option_type','tick_size', 'lot_size','Multiplier' ]]

            ##################################################################### #####################################################################
            payloadsub = {"exchangeSegmentList": ["MCXFO"]}
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("POST", sub_url, data=payloadsubjson, headers=mheaders)
            data_p = req.json()

            abc = data_p['result']
            # print(data_p)
            with open('../Resourses/ContractMCX', 'w') as f:
                f.write(abc)
            f.close()

            contractMCX1 = pd.read_csv('../Resourses/ContractMCX', header=None, sep='|'
                                       , names=['ExchangeSegment', 'Token', 'instrument_type1', 'symbol', 'Stock_name',
                                                'instrument_type', ' NameWithSeries', 'InstrumentID', 'PriceBand.High',
                                                'PriceBand.Low',
                                                'FreezeQty', 'tick_size', 'lot_size', 'Multiplier', 'UnderlyingInstrumentId',
                                                'IndexName',
                                                'ContractExpiration', 'strike1', 'OptionType'])


            contractMCX1 = contractMCX1[contractMCX1['instrument_type1'] != 4]
            contractMCX1['Segment'] = contractMCX1['OptionType'].apply(segwork)
            contractMCX1['option_type'] = contractMCX1['OptionType'].apply(otwork)
            contractMCX1['Exchange'] = 'MCXFO'


            contractMCX1['strike1'] = contractMCX1['strike1'].fillna(' ')
            contractMCX1['strike_price'] = contractMCX1['strike1'].apply(spwork)
            contractMCX1['exp'] = contractMCX1['ContractExpiration'].apply(expwork)
            contractMCX1['asset_token'] = contractMCX1['UnderlyingInstrumentId'].apply(assetTokenWork)

            cndfMCX1 = contractMCX1[['Exchange','Segment','Token', 'symbol', 'Stock_name', 'instrument_type', 'exp', 'strike_price', 'option_type',
                                 'asset_token', 'tick_size', 'lot_size', 'strike1','FreezeQty']]

            cndMCX = dt.Frame(cndfMCX1)
        ##########################################################################################################################################


            payloadsub = {"exchangeSegmentList": ["NSECD"]}
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("POST", sub_url, data=payloadsubjson, headers=mheaders)
            data_p = req.json()
            abc = data_p['result']
            # print(abc)
            with open ('../Resourses/contractCD_raw.txt','w') as f:
                f.write(abc)
            f.close()
            contractCD1 = pd.read_csv('../Resourses/contractCD_raw.txt', header=None, sep='|'
                                      ,names=['ExchangeSegment', 'Token', 'instrument_type1', 'symbol', 'Stock_name',
                                                'instrument_type', ' NameWithSeries', 'InstrumentID', 'PriceBand.High',
                                                'PriceBand.Low','FreezeQty', 'tick_size', 'lot_size', 'Multiplier',
                                                 'UnderlyingInstrumentId','IndexName','ContractExpiration', 'strike1', 'OptionType'])
            contractCD1 = contractCD1[contractCD1['instrument_type1']!=4]
            contractCD1['Exchange'] = 'NSECD'
            # contractCD1['Segment'] = 'F'
            contractCD1['Segment'] = contractCD1['OptionType'].apply(segwork)
            contractCD1['option_type'] = contractCD1['OptionType'].apply(otwork)
            contractCD1['strike1'] = contractCD1['strike1'].fillna(' ')
            contractCD1['strike_price'] = contractCD1['strike1'].apply(spwork)
            contractCD1['exp'] = contractCD1['ContractExpiration'].apply(expwork)
            contractCD1['asset_token'] = contractCD1['UnderlyingInstrumentId'].apply(assetTokenWork)
            cndCD1 = contractCD1[['Exchange','Segment','Token', 'symbol', 'Stock_name', 'instrument_type', 'exp', 'strike_price', 'option_type',
                                 'asset_token', 'tick_size', 'lot_size', 'strike1','Multiplier','FreezeQty']]
            cndfCD = dt.Frame(cndCD1)
            ##########################################################################################################################################

            contract_df = pd.concat([cndf1,cndEq,cndfMCX1,cndCD1])
            contract_df['instrument_type'] =  contract_df['instrument_type'].fillna('Equity')
            # contract_df['option_type'] =  contract_df['option_type'].fillna('XX')
            # contract_df['strike_price'] =  contract_df['strike_price'].fillna('XX')

            contract_df.to_csv('../Resourses/ContractMasters/contract_df.csv',index=False)

            contract_dt = dt.Frame(contract_df)

        else:
            print('in download master false part')
            contract_df = pd.read_csv(contractDir,low_memory=False,)

            contract_dt = dt.Frame(contract_df)


        contract_df.to_sql("contract_NFO",dbconn,if_exists='replace',index=False)
        sumdf1=contract_df[contract_df['instrument_type']=='FUTIDX']
        sumdf=sumdf1[sumdf1['symbol']=='NIFTY'].to_numpy()

        return contract_dt.to_numpy(),sumdf

    except:
        print(traceback.print_exc())
        print(sys.exc_info(), "@download master")

a,b=get_contract_master_FNO(False)



fltr = np.asarray(['NSEFO'])
# lua = a[np.in1d(a[:, 0], fltr)][:,2]
lua = a[np.in1d(a[:, 0], fltr)]

print(lua.shape)
fltr = np.asarray(['OPTSTK'])
lua = lua[np.in1d(lua[:, 5], fltr)]
fltr = np.asarray(['20220127'])
lua = lua[np.in1d(lua[:, 6], fltr)]
# print(lua.argsort())
print(lua.shape)


#
# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=192.168.102.59;'
#                       'Database=RMS;'
#                       'UID=sa;PWD=Yash@852;'
#                       )
# cursor = conn.cursor()
#
#
#
#
# # print(lua)
# mheaders, iheaders, mToken, iToken, apiip, userid, source = readConfig1()
# c = datetime.datetime.today().strftime('%b %d %Y 071500')
# b = datetime.datetime.today().strftime('%b %d %Y 153000')
# # b = datetime.datetime.utcfromtimestamp(a).strftime('%b %d %Y 153000')
#
# sql = """select distinct(b.nToken) from tprice a
# left join script_master b
# on a.symbol collate database_default = b.sSymbol
# and a.exp collate database_default=b.nExpiryDate and a.strike collate database_default = b.nStrikePrice and a.option_type collate database_default=b.sOptionType"""
#
# cursor.execute(sql)
# for id in cursor:
#     token = int(id[0])
#
#     url = '%s/marketdata/instruments/ohlc?exchangeSegment=%s&exchangeInstrumentID=%s&startTime=%s&endTime=%s&compressionValue=%s' % (
#         apiip, 'NSEFO',
#         token, c, b, 1)
#     axxx = requests.get(url, headers=mheaders)
#     print(axxx.text)
#
#     # fltr1 = np.asarray(['FUTIDX','FUTSTK'])
#     # lua1 = lua[np.in1d(lua[:, 5], fltr1)]
#     #
#     # xxxx = np.unique(lua1[lua1[:, 6].argsort()][:,6])[1]
#
#     # fltr3 = np.asarray([xxxx])
#     # lua2 = lua1[np.in1d(lua1[:, 6], fltr3)][:,1:6]
#     # futureTokenDict = {}
#     # for i in lua2:
#     #     futureTokenDict[i[2]] = i[1]
