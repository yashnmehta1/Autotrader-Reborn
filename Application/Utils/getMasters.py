import time
import traceback
import datetime
import numpy as np
import pandas as pd
import datatable as dt
import requests
import sys
from Application.Utils.configReader import readConfig_All
import json
import numpy
from  os import getcwd,path
from Application.Utils.bhavCpy import get_bhavcopy


loc1 = getcwd().split('Application')
contractDir = path.join(loc1[0], 'Application','Masters', 'contract_df.csv')
contractDir1 = path.join(loc1[0], 'Application','Masters')
downloadLoc = path.join(loc1[0], 'Downloads')

file_contract_fo = path.join(contractDir1, 'contract_fo.csv')
file_contract_eq = path.join(contractDir1, 'contract_eq.csv')
file_contract_idx = path.join(contractDir1, 'contract_idx.json')
file_contract_cd = path.join(contractDir1, 'contract_cd.csv')









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
    if(a == ''):
        return ' '
    if(a == 0):
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
            return 26000
        elif(b=='Nifty Bank'):
            return  26001
        elif (b == 'Nifty Fin Service'):
            return 26002

    else:

        a = str(a)
        aa = a.replace('110010000', '')
        aaa = aa.replace('11001000', '')

        return int(aaa)



def strkwork1( z):
    if (z == '0.00'):
        x = ' '
    if (z == 0):
        x = ' '
    else:
        x = '%.2f' % z
    return x

def expWork1( z):
    try:
        x = datetime.datetime.strptime(z, '%d-%b-%Y').strftime('%Y%m%d')
        return x
    except:
        print(traceback.print_exc())
        return ' '




def assetTokenWork( a):

    a = str(a)
    aa = a.replace('110010000', '')
    aaa = aa.replace('11001000', '')
    return aaa

def foBHavcp4Masters():
    pass

def getMaster(validation):
    try:
        Symbol_Expiry_Dict = {}
        mheaders, iheaders, mToken, iToken, apiip, userid, source, market_data_appKey, market_data_secretKey, ia_appKey, ia_secretKey, clist, DClient, broadcastMode = readConfig_All()

        if(validation==True):
            get_bhavcopy()

            sub_url = apiip + '/marketdata/instruments/master'

            ###################################### NSE FNO #################################
            payloadsub = {"exchangeSegmentList": ["NSEFO"]}
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("POST", sub_url, data=payloadsubjson, headers=mheaders)
            data_p = req.json()
            abc = data_p['result']
            ####################################################################################

            ############################# Save as Raw Text ###############################
            contractFO_raw1 = path.join(downloadLoc,'contractFO_raw.txt')
            with open (contractFO_raw1,'w') as f:
                f.write(abc)
            f.close()
            ####################################################################################
            contractFo1 = pd.read_csv(contractFO_raw1, header=None, sep='|'
                                      ,names=['ExchangeSegment', 'Token', 'instrument_type1', 'symbol', 'Stock_name',
                                              'instrument_type', ' NameWithSeries', 'InstrumentID', 'PriceBand.High',
                                              'PriceBand.Low','FreezeQty', 'tick_size', 'lot_size', 'Multiplier',
                                              'UnderlyingInstrumentId','IndexName','ContractExpiration', 'strike1', 'OptionType'])

            contractFo1 = contractFo1[contractFo1['instrument_type1']!=4] # type 4 is spread contract that we should include but on later stage of product dev

            contractFo1['Exchange'] = 'NSEFO'
            # contractFo1['Segment'] = 'F'
            contractFo1['Segment'] = contractFo1['OptionType'].apply(segwork)
            contractFo1['option_type'] = contractFo1['OptionType'].apply(otwork)
            contractFo1['strike1'] = contractFo1['strike1'].fillna(0)
            contractFo1['strike1'] = contractFo1['strike1'].astype('float')
            contractFo1['strike_price'] = contractFo1['strike1'].apply(spwork)
            contractFo1['exp'] = contractFo1['ContractExpiration'].apply(expwork)
            contractFo1['asset_token'] = contractFo1[['UnderlyingInstrumentId','IndexName']].apply(lambda x: assetTokenWork1(x.UnderlyingInstrumentId, x.IndexName), axis=1)
            contractFo1['FreezeQty'] = contractFo1['FreezeQty'] - 1

            cndf1 = contractFo1[['Exchange',
                                 'Segment','Token', 'symbol', 'Stock_name', 'instrument_type',
                                 'exp', 'strike_price', 'option_type','asset_token', 'tick_size',
                                 'lot_size', 'strike1','Multiplier','FreezeQty','PriceBand.High',
                                 'PriceBand.Low']]

            cndfo = dt.Frame(cndf1)
            d = cndf1.to_numpy()
            contract_fo = cndf1.to_numpy()

            contract_fo = (contract_fo[contract_fo[:, 2].argsort()])
            strat_point = (contract_fo[0][2])
            end_point = (contract_fo[-1][2])

            print('strat_point',strat_point,'end_point',end_point)
            gap = end_point - strat_point
            temp_df1 = np.arange(start=35000, stop=gap + 35001, step=1)
            raw_token = contract_fo[:, 2]
            total_token = np.hstack([raw_token, temp_df1])
            v, r = np.unique(total_token, return_counts=True)


            unique_token = v[np.where(r == 1)]
            print(unique_token,unique_token.shape)

            temp_rows = np.empty((unique_token.shape[0], 17), dtype=object)
            temp_rows[:, 2] = unique_token
            temp_rows[:, [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,15,16]] = ['NSEFO',
                                                                                   'x', '', '', '', '',
                                                                                   '', '', 0.0,0.0, 0,
                                                                                   0.0, 0.0, 0,0.0,0.0]

            contract_fo1 = np.vstack([contract_fo, temp_rows])
            contract_fo = (contract_fo1[contract_fo1[:, 2].argsort()])

            contract_fox = contract_fo[contract_fo[:, 2].argsort()]
            iklo = 35000


            for i in contract_fox:
                if(iklo!=i[2]):
                    # print(iklo,i)
                    time.sleep(1)
                iklo +=1

            ##################### adding extra columns for additional fields ##########
            bdf = np.zeros((contract_fo.shape[0], 21),dtype=object)
            contract_fo = np.hstack([contract_fo, bdf])
            ################################################################

            ########################  Expiry Type #########################
            unique_symbols = np.unique(contract_fo[:, 3])

            for i in unique_symbols:
                # time.sleep(2)
                Symbol_Expiry_Dict[i] = ['', '', '', '', '', '', '']
                fltr = np.asarray([i])
                filteredDf = contract_fo[np.in1d(contract_fo[:, 3], fltr)]

                fltr1 = np.asarray(['OPTIDX'])
                filteredDf1 = filteredDf[np.in1d(filteredDf[:, 5], fltr1)]
                unique_exp = np.unique(filteredDf[:, 6])
                unique_exp = unique_exp[unique_exp.argsort()]

                for jk, ik in enumerate(unique_exp):

                    fltr1 = np.asarray([ik])
                    token_list1 = filteredDf1[np.in1d(filteredDf1[:, 6], fltr1), 2]
                    token_list = np.subtract(token_list1, 35000).tolist()

                    if (jk == 0):
                        Symbol_Expiry_Dict[i][0] = ik
                        contract_fo[token_list, 37] = 1
                    elif (jk == 1):
                        Symbol_Expiry_Dict[i][1] = ik
                        contract_fo[token_list, 37] = 2
                    else:
                        Symbol_Expiry_Dict[i][2] = ik
                        contract_fo[token_list, 37] = 3
                fltr1 = np.asarray(['FUTSTK', 'FUTIDX'])
                filteredDf1 = filteredDf[np.in1d(filteredDf[:, 5], fltr1)]

                unique_exp = np.unique(filteredDf1[:, 6])
                unique_exp = unique_exp[unique_exp.argsort()]

                for jk, ik in enumerate(unique_exp):
                    fltr1 = np.asarray([ik])
                    token_list1 = filteredDf[np.in1d(filteredDf[:, 6], fltr1), 2]
                    token_list = np.subtract(token_list1, 35000).tolist()

                    if (jk == 0):
                        if (ik == Symbol_Expiry_Dict[i][0]):
                            Symbol_Expiry_Dict[i][3] = ik
                            contract_fo[token_list, 37] = 4
                        else:
                            Symbol_Expiry_Dict[i][4] = ik
                            contract_fo[token_list, 37] = 5
                    elif (jk == 1):
                        Symbol_Expiry_Dict[i][5] = ik
                        contract_fo[token_list, 37] = 6
                    else:
                        Symbol_Expiry_Dict[i][6] = ik
                        contract_fo[token_list, 37] = 7

            ################################################################


            ###################### working for strike diff ####################
            unique_symbols = np.unique(contract_fo[:, 3])
            for i in unique_symbols:
                if (i != ''):
                    fltr = np.asarray([i])
                    filteredDf = contract_fo[np.in1d(contract_fo[:, 3], fltr)]
                    fltr1 = np.asarray(['OPTSTK', 'OPTIDX'])
                    filteredDf1 = filteredDf[np.in1d(filteredDf[:, 5], fltr1)]

                    uniquq_strk = np.unique(filteredDf1[:, 7]).astype('float')
                    uniquq_strk = uniquq_strk[uniquq_strk.argsort()]
                    median1 = round(uniquq_strk.shape[0] / 2)
                    strikeDiff = float(uniquq_strk[median1]) - float(uniquq_strk[median1 - 1])
                    contract_fo[np.where(contract_fo[:, 3] == i), 36] = strikeDiff
            ################################################################


            # # ############################## future token ##############################
            # fltr = np.asarray(['NSEFO'])
            # lua = contract_fo[np.in1d(contract_fo[:, 0], fltr)]
            # fltr1 = np.asarray(['FUTIDX', 'FUTSTK'])
            # lua1 = lua[np.in1d(lua[:, 5], fltr1)]
            #
            # for i in unique_symbols:
            #     if (i != ''):
            #         lua2 = lua1[np.in1d(lua1[:, 3], np.asarray([i]))]
            #         # print(lua2)
            #         xxxx = lua2[lua2[:, 6].argsort()][0][2]
            #         contract_fo[np.where(contract_fo[:, 3] == i), 17] = xxxx
            #         # futureTokenDict[i] = xxxx

            ####################################################################

            ###################### bhavcopy fo ###################
            a = pd.read_csv(path.join(downloadLoc,'fo_bhav.csv'))
            a['EXPIRY_DT'] = a['EXPIRY_DT'].apply(expWork1)
            a['STRIKE_PR'] = a['STRIKE_PR'].apply(strkwork1)
            a['OPTION_TYP'] = a['OPTION_TYP'].replace('XX', ' ')
            b = a.to_numpy()

            c = (b[b[:, 3].argsort()])
            contract_fo = contract_fo[contract_fo[:, 2].argsort()]

            for i in unique_symbols:
                fltr = np.asarray([i])
                filertDf = contract_fo[np.in1d(contract_fo[:, 3], fltr)]
                filertBC = c[np.in1d(c[:, 1], fltr)]

                for ik in filertBC:
                    xx = filertDf[np.where(filertDf[:, 6] == ik[2])]
                    yy = xx[np.where(xx[:, 7] == ik[3])]
                    if (yy.shape[0] > 1):
                        zz = yy[np.where(yy[:, 8] == ik[4])]
                    else:
                        zz = yy
                    try:
                        contract_fo[zz[0][2] - 35000, [18,19,22]] = [ik[9],ik[9],ik[12]]
                        # contract_fo[zz[0][2] - 35000, 17] = ik[9]
                    except:
                        # print('bhavcopy error',ik)

                        pass

            # ############################## future token ##############################
            fltr = np.asarray(['NSEFO'])
            lua = contract_fo[np.in1d(contract_fo[:, 0], fltr)]
            fltr1 = np.asarray(['FUTIDX', 'FUTSTK'])
            lua1 = lua[np.in1d(lua[:, 5], fltr1)]

            for i in unique_symbols:
                if (i != ''):
                    lua2 = lua1[np.in1d(lua1[:, 3], np.asarray([i]))]
                    xxxx = lua2[lua2[:, 6].argsort()][0][2]
                    contract_fo[np.where(contract_fo[:, 3] == i), 17] = xxxx


            contract_fo[:,17] = contract_fo[:,17].astype('int')

            ####################################################################

            ################## working for moneyness ##########################

            # for op in contract_fo:
            #
            #     if(iklo==op[2]):
            #         print(iklo)
            #     else:
            #         print(iklo,op)
            #         time.sleep(0.1)
            #     iklo +=1

            for i in unique_symbols:
                if (i != ''):
                    fltr = np.asarray([i])
                    filterDf2 = contract_fo[np.in1d(contract_fo[:, 3], fltr)]

                    tkn = int(filterDf2[0][15])



                    prce = contract_fo[tkn - 35000, 18]
                    strikeDif1 = contract_fo[tkn - 35000, 36]
                    # print('filterDf2',i,filterDf2[0][15],prce,strikeDif1)
                    try:
                        atm = int(prce / strikeDif1) * strikeDif1
                    except:
                        print('error',i,prce,tkn)

                    if(i=='RELIANCE'):
                        atm= 2800.00


                    fltr = np.asarray(['CE'])
                    filterDf3 = filterDf2[np.in1d(filterDf2[:, 8], fltr)]

                    atmToken = filterDf3[np.where(filterDf3[:, 12] == atm), 2][0]
                    atmToken1 = np.subtract(atmToken, 35000).tolist()

                    contract_fo[atmToken1, 31] = 1

                    otmToken = filterDf3[np.where(filterDf3[:, 12] > atm), 2][0]
                    # print(i, atmToken1)
                    otmToken1 = np.subtract(otmToken, 35000).tolist()
                    contract_fo[otmToken1, 31] = 3

                    itmToken = filterDf3[np.where(filterDf3[:, 12] < atm), 2][0]
                    itmToken1 = np.subtract(itmToken, 35000).tolist()
                    contract_fo[itmToken1, 31] = 5

                    fltr = np.asarray(['PE'])
                    filterDf3 = filterDf2[np.in1d(filterDf2[:, 8], fltr)]

                    atmToken = filterDf3[np.where(filterDf3[:, 12] == atm), 2][0]
                    atmToken1 = np.subtract(atmToken, 35000).tolist()
                    contract_fo[atmToken1, 31] = 2

                    otmToken = filterDf3[np.where(filterDf3[:, 12] < atm), 2][0]
                    otmToken1 = np.subtract(otmToken, 35000).tolist()
                    contract_fo[otmToken1, 31] = 4

                    itmToken = filterDf3[np.where(filterDf3[:, 12] > atm), 2][0]
                    itmToken1 = np.subtract(itmToken, 35000).tolist()
                    contract_fo[itmToken1, 31] = 6

            ########################################################################

            contract_fo1=contract_fo[:,[2,4,8,4]]
            fltr2 = np.asarray(['CE'])
            contract_fo1_ce1 = contract_fo1[np.in1d(contract_fo1[:, 2], fltr2)]
            contract_fo1_ce2 = contract_fo1_ce1[:,[0,1,3]]

            for j,i in enumerate(contract_fo1_ce2):
                if(contract_fo1_ce2[j,1] != ''):
                    contract_fo1_ce2[j,1] = contract_fo1_ce2[j,1][:-2]

            fltr2 = np.asarray(['PE'])
            contract_fo1_pe1 = contract_fo1[np.in1d(contract_fo1[:, 2], fltr2)]
            contract_fo1_pe2 = contract_fo1_pe1[:,[0,1,3]]

            for j,i in enumerate(contract_fo1_pe2):
                if(contract_fo1_pe2[j,1] != ''):
                    contract_fo1_pe2[j,1] = contract_fo1_pe2[j,1][:-2]





            ##################### adding extra columns for additional fields ##########
            bdf = np.zeros((contract_fo.shape[0], 1))
            contract_fo = np.hstack([contract_fo, bdf])
            ################################################################

            contract_fo_pd= pd.DataFrame(contract_fo)
            contract_fo1_ce_pd = pd.DataFrame(contract_fo1_ce2,columns=['a','b','c']).set_index('b')
            contract_fo1_pe_pd = pd.DataFrame(contract_fo1_pe2,columns=['e','b','f']).set_index('b')

            contract_fo1_ce_pd1=contract_fo1_ce_pd.join(contract_fo1_pe_pd).set_index('a')
            contract_fo1_pe_pd1=contract_fo1_pe_pd.join(contract_fo1_ce_pd).set_index('e')



            # print(contract_fo1_ce_pd1.iloc[0,:])
            # print(contract_fo1_pe_pd1)


            for i in contract_fo:
                if(i[8] == 'CE'):
                    contract_fo[i[2]-35000,38] = contract_fo1_ce_pd1.loc[i[2],'e']
            for i in contract_fo:
                if(i[8] == 'PE'):
                    try:
                        contract_fo[i[2]-35000,38] = contract_fo1_pe_pd1.loc[i[2],'a']
                    except:
                        print('error',i[2],contract_fo1_pe_pd1.loc[i[2]])


            non_nan_array = np.where(contract_fo[:,1]=='x')
            contract_fo[non_nan_array,38] = contract_fo[non_nan_array,38].astype('int')

            np.savetxt(file_contract_fo,contract_fo, delimiter=',',fmt='%s')
            fo_contract_df11 = pd.DataFrame(contract_fo)



            ############ option chain master #########################

            payloadsub = {"exchangeSegmentList": ["NSECM"]}
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("POST", sub_url, data=payloadsubjson, headers=mheaders)
            data_p = req.json()
            abc = data_p['result']
            ContractEQ1 = path.join(downloadLoc,'ContractEQ')
            with open(ContractEQ1, 'w') as f:
                f.write(abc)
            f.close()
            contractEq1 = pd.read_csv(ContractEQ1, header=None, sep='|',index_col=False
                                      ,names=['ExchangeSegment',
                                              'Token','InstrumentType','symbol','Stock_name','exp',' NameWithSeries','InstrumentID',
                                              'PriceBand.High','PriceBand.Low','FreezeQty','tick_size','lot_size','Multiplier'])

            contractEq1['Multiplier'] = 1
            contractEq1['Exchange'] = 'NSECM'
            contractEq1['Segment'] = 'E'
            contractEq1['option_type'] = ' '
            contractEq1['strike_price'] =' '
            contractEq1['instrument_type'] ='Equity'
            contractEq1['asset_token'] =' '
            contractEq1['strike1'] =0.0


            # print(contractEq1.loc[:,'FreezeQty'])


            cndEq = contractEq1[['Exchange',
                                 'Segment','Token', 'symbol','Stock_name','instrument_type',
                                 'exp','strike_price','option_type','asset_token','tick_size',
                                 'lot_size','strike1','Multiplier','FreezeQty','PriceBand.High',
                                 'PriceBand.Low']]

            contract_eq = cndEq.to_numpy()

            ##################### indexing by tokens for master EQ #####################
            contract_eq = (contract_eq[contract_eq[:, 2].argsort()])
            strat_point = 0
            end_point = (contract_eq[-1][2])
            gap = end_point - strat_point
            # print(strat_point,end_point,gap)
            temp_df1 = np.arange(start=0, stop=gap + 5000, step=1)
            raw_token = contract_eq[:, 2]
            total_token = np.hstack([raw_token, temp_df1])
            v, r = np.unique(total_token, return_counts=True)
            unique_token = v[np.where(r == 1)]
            temp_rows = np.empty((unique_token.shape[0], 17), dtype=object)
            temp_rows[:, 2] = unique_token
            temp_rows[:, [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,15,16]] = ['NSECM', 'x', '', '', '', '', '', '', 0.0,
                                                                                   0.0, 0, '', 0.0, 0,0.0,0.0]

            contract_eq = np.vstack([contract_eq, temp_rows])
            contract_eq = (contract_eq[contract_eq[:, 2].argsort()])
            ##################### adding extra columns for additional fields ##########
            bdf = np.zeros((contract_eq.shape[0], 21))
            contract_eq = np.hstack([contract_eq, bdf])
            Eq_contract_df1=pd.DataFrame(contract_eq)

            np.savetxt(file_contract_eq,contract_eq, delimiter=',',fmt='%s')


            ################################################################






            ##################################################################### #####################################################################
            # payloadsub = {"exchangeSegmentList": ["MCXFO"]}
            # payloadsubjson = json.dumps(payloadsub)
            # req = requests.request("POST", sub_url, data=payloadsubjson, headers=mheaders)
            # data_p = req.json()
            #
            # abc = data_p['result']
            # # print(data_p)
            # ContractMCX1 = os.path.join(loc1[0] ,'Resourses','ContractMCX')
            # with open(ContractMCX1, 'w') as f:
            #     f.write(abc)
            # f.close()
            #
            # contractMCX1 = pd.read_csv(ContractMCX1, header=None, sep='|'
            #                            , names=['ExchangeSegment', 'Token', 'instrument_type1', 'symbol', 'Stock_name',
            #                                     'instrument_type', ' NameWithSeries', 'InstrumentID', 'PriceBand.High',
            #                                     'PriceBand.Low',
            #                                     'FreezeQty', 'tick_size', 'lot_size', 'Multiplier', 'UnderlyingInstrumentId',
            #                                     'IndexName',
            #                                     'ContractExpiration', 'strike1', 'OptionType'])
            #
            #
            # contractMCX1 = contractMCX1[contractMCX1['instrument_type1'] != 4]
            # contractMCX1['Segment'] = contractMCX1['OptionType'].apply(segwork)
            # contractMCX1['option_type'] = contractMCX1['OptionType'].apply(otwork)
            # contractMCX1['Exchange'] = 'MCXFO'
            #
            #
            # contractMCX1['strike1'] = contractMCX1['strike1'].fillna(' ')
            # contractMCX1['strike_price'] = contractMCX1['strike1'].apply(spwork)
            # contractMCX1['exp'] = contractMCX1['ContractExpiration'].apply(expwork)
            # contractMCX1['asset_token'] = contractMCX1['UnderlyingInstrumentId'].apply(assetTokenWork)
            #
            # cndfMCX1 = contractMCX1[['Exchange','Segment','Token', 'symbol', 'Stock_name', 'instrument_type', 'exp', 'strike_price', 'option_type',
            #                      'asset_token', 'tick_size', 'lot_size', 'strike1','FreezeQty']]
            #
            # cndMCX = dt.Frame(cndfMCX1)
            ##########################################################################################################################################


            payloadsub = {"exchangeSegmentList": ["NSECD"]}
            payloadsubjson = json.dumps(payloadsub)
            req = requests.request("POST", sub_url, data=payloadsubjson, headers=mheaders)
            data_p = req.json()
            abc = data_p['result']
            # print(abc)
            contractCD_raw = path.join(downloadLoc,'contractCD_raw.txt')
            with open (contractCD_raw,'w') as f:
                f.write(abc)
            f.close()
            contractCD1 = pd.read_csv(contractCD_raw, header=None, sep='|'
                                      ,names=['ExchangeSegment',
                                              'Token', 'instrument_type1', 'symbol', 'Stock_name','instrument_type',
                                              'NameWithSeries', 'InstrumentID', 'PriceBand.High','PriceBand.Low','FreezeQty',
                                              'tick_size', 'lot_size', 'Multiplier',
                                              'UnderlyingInstrumentId','IndexName','ContractExpiration', 'strike1', 'OptionType'])
            contractCD1 = contractCD1[contractCD1['instrument_type1']!=4]
            contractCD1['Exchange'] = 'NSECD'
            # contractCD1['Segment'] = 'F'
            contractCD1['Segment'] = contractCD1['OptionType'].apply(segwork)
            contractCD1['option_type'] = contractCD1['OptionType'].apply(otwork)
            contractCD1['strike1'] = contractCD1['strike1'].fillna('')
            contractCD1['strike_price'] = contractCD1['strike1'].apply(spwork)
            contractCD1['exp'] = contractCD1['ContractExpiration'].apply(expwork)
            contractCD1['asset_token'] = contractCD1['UnderlyingInstrumentId'].apply(assetTokenWork)
            cndCD1 = contractCD1[['Exchange',
                                  'Segment','Token', 'symbol', 'Stock_name', 'instrument_type',
                                  'exp', 'strike_price', 'option_type','asset_token', 'tick_size',
                                  'lot_size', 'strike1','Multiplier','FreezeQty','PriceBand.High',
                                  'PriceBand.Low']]


            contract_cd = cndCD1.to_numpy()

            ##################### indexing by tokens for master EQ #####################
            contract_cd = (contract_cd[contract_cd[:, 2].argsort()])
            strat_point = 0
            end_point = (contract_cd[-1][2])
            gap = end_point - strat_point
            # print('NSECDS',strat_point,end_point,gap)
            temp_df1 = np.arange(start=0, stop=gap + 5000, step=1)
            raw_token = contract_cd[:, 2]
            total_token = np.hstack([raw_token, temp_df1])
            v, r = np.unique(total_token, return_counts=True)
            unique_token = v[np.where(r == 1)]
            temp_rows = np.empty((unique_token.shape[0], 17), dtype=object)
            temp_rows[:, 2] = unique_token
            temp_rows[:, [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,15,16]] = ['NSECD', 'x', '', '', '', '', '', '', 0.0,
                                                                                   0.0, 0, '', 0.0, 0,0.0,0.0]
            contract_cd = np.vstack([contract_cd, temp_rows])
            contract_cd = (contract_cd[contract_cd[:, 2].argsort()])
            ##################### adding extra columns for additional fields ##########
            bdf = np.zeros((contract_cd.shape[0], 21))
            contract_cd = np.hstack([contract_cd, bdf])
            ################################################################
            cd_contract_df1=pd.DataFrame(contract_cd)
            cndfCD = dt.Frame(cndCD1)

            np.savetxt(file_contract_cd,contract_cd, delimiter=',',fmt='%s')

            ##########################################################################################################################################
            heads = ['Exchange',
                     'Segment', 'Token', 'symbol', 'Stock_name', 'instrument_type',
                     'exp', 'strike_price', 'option_type', 'asset_token', 'tick_size',
                     'lot_size', 'strike1', 'Multiplier', 'FreezeQty','pbHigh',
                     'pbLow', 'futureToken','close', 'ltp','bid',
                     'ask', 'oi','prev_day_oi', 'iv','delta',
                     'gamma', 'theta','vega', 'theoritical_price','PPR',
                     'moneyness', 'Volume','amt', 'Avg1MVol','ATP',
                     'strike_diff', 'expiry_type','cpToken'
                     ]


            # for i in contract_fo:
            #     print(i)

            # contract_df = pd.concat([fo_contract_df11,Eq_contract_df1,cd_contract_df1])
            # contract_df.columns = heads
            # # contract_df['instrument_type'] =  contract_df['instrument_type'].fillna('Equity')
            #
            # contract_df.to_csv(contractDir,index=False)
            # contract_full = contract_df.to_numpy()

            return contract_fo,contract_eq,contract_cd,heads
        else:


            try:
                sub_url = apiip + '/marketdata/instruments/indexlist?exchangeSegment=1'
                # print(sub_url)
                ###################################### NSE FNO #################################
                payloadsub = {"exchangeSegmentList": ["NSECM"]}
                payloadsubjson = json.dumps(payloadsub)
                req = requests.request("GET", sub_url,  headers=mheaders)


                data_p = req.json()
                indexList = data_p['result']['indexList']
                # print('indexList',indexList)
                indexDict = {}
                indexDict1 = {}
                for i in indexList:
                    x =i.split('_')
                    indexDict[x[0]] = [x[1],0.0,0.0]
                    indexDict1[x[1]] = x[0]
                # print(indexDict)
                ####################################################################################
            except:
                print(traceback.print_exc())


            # contract_df = pd.read_csv(contractDir,low_memory=False,)
            contract_fo = pd.read_csv(file_contract_fo,low_memory=False,header=None).to_numpy()
            nan_array = np.where(contract_fo[:,1] == 'x')
            non_nan_array = np.where(contract_fo[:,1] != 'x')
            contract_fo[nan_array,6] =  ''


            contract_fo[non_nan_array,6] = contract_fo[non_nan_array,6].astype('int')
            contract_fo[non_nan_array,6] = contract_fo[non_nan_array,6].astype('str')

            contract_eq = pd.read_csv(file_contract_eq,low_memory=False,header=None).to_numpy()
            contract_cd = pd.read_csv(file_contract_cd,low_memory=False,header=None).to_numpy()



            # contract_dt = dt.Frame(contract_df)
            # contract_full = contract_dt.to_numpy()
            heads = ['Exchange',
                     'Segment', 'Token', 'symbol', 'Stock_name', 'instrument_type',
                     'exp', 'strike_price', 'option_type', 'asset_token', 'tick_size',
                     'lot_size', 'strike1', 'Multiplier', 'FreezeQty','pbHigh', #pb priceband
                     'pbLow', 'futureToken','close', 'ltp','bid',
                     'ask', 'oi','prev_day_oi', 'iv','delta',
                     'gamma', 'theta','vega', 'theoritical_price','PPR',
                     'moneyness', 'Volume','amt', 'Avg1MVol','ATP',
                     'strike_diff', 'expiry_type','cpToken','days2Exp'
                     ]

            ############ option chain master #########################
            return contract_fo,contract_eq,contract_cd,heads

    except:
        print(traceback.print_exc())
        print(sys.exc_info(), "@download master")




# a,b,c,d = getMaster(False)
# xx=a[np.where(a[:,3] =='BANKNIFTY')][0,17]
#
#
# futureToken = a[xx-35000, 36]
#
# print(futureToken)