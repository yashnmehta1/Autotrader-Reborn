import traceback
import sys
import logging
import json
import datetime
import time
from Application.Utils.getMasters import getMaster
import  requests

from Application.Utils.configReader import writeMD,refresh



def subscribeToken(self, token, seg, streamType=1501):
    try:
        if (seg == 'NSEFO'):
            segment = 2
        elif (seg == 'NSECM'):
            segment = 1
        ## ****** CD PENDING
        # print('segment',segment)
        sub_url = self.URL + '/marketdata/instruments/subscription'
        payloadsub = {"instruments": [{"exchangeSegment": segment, "exchangeInstrumentID": token}],
                      "xtsMessageCode": streamType}

        payloadsubjson = json.dumps(payloadsub)

        # print(payloadsubjson)
        req = requests.request("POST", sub_url, data=payloadsubjson, headers=self.MDheaders)

        # print(req.text)

        if ('subscribed successfully' in req.text or 'Already Subscribed' in req.text):
            pass
        else:
            logging.error(req.text)

        ####################### database working passage deleted if required retrive from backup ##################
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())


def unSubscription_feed(self, token, seg, streamType=1501):
    try:
        if (seg == 'NSEFO'):
            segment = 2
        elif (seg == 'NSECM'):
            segment = 1
        ## ****** CD PENDING
        sub_url = self.URL + '/marketdata/instruments/subscription'
        payloadsub = {"instruments": [{"exchangeSegment": segment, "exchangeInstrumentID": token}],
                      "xtsMessageCode": streamType}
        payloadsubjson = json.dumps(payloadsub)
        req = requests.request("PUT", sub_url, data=payloadsubjson, headers=self.MDheaders)

        logging.info(req.text)
        print(req.text)

        if ('subscribed successfully' in req.text or 'Already Subscribed' in req.text):
            pass
        else:
            logging.error(req.text)

        ####################### database working passage deleted if required retrive from backup ##################
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())

def login(self):
    try:

        self.login.pbLogin.setEnabled(False)
        self.login.label.append('Logging in to Marketdata API..')
        refresh(self)
        payload = {
            "secretKey": self.MDSecret,
            "appKey": self.MDKey,
            "source": self.Source
        }
        login_url = self.URL + '/marketdata/auth/login'

        login_access = requests.post(login_url, json=payload)
        logging.info(login_access.text)
        # print(login_access.text)


        if login_access.status_code == 200:
            data = login_access.json()
            result = data['result']
            if data['type'] == 'success':
                a = 'successfull'
                result = data['result']

                token = result['token']
                userID = result['userID']
                writeMD(token, userID)
                self.login.updateMDstatus(data['type'])
                self.login.label.append('MARKETDATA API Logged In.\nDownloadin contract masters...')
                self.login.updateIAstatus(data['type'])
                self.fo_contract, self.eq_contract, self.cd_contract, self.contract_heads = getMaster(
                    self.login.cbCmaster.isChecked())
                self.shareContract()
                self.login.label.append('ContractMaster_fo downloaded.\nLogging in to Interactive API..')

            else:
                self.login.pbLogin.setEnable(True)

        else:
            self.login.pbLogin.setEnabled(True)
            logging.info(str(login_access.text).replace('\n', '\t\t\t\t'))
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())

def getQuote(self, token, seg, streamType):
    try:
        if (seg == 'NSEFO'):
            segment = 2
        elif (seg == 'NSECM'):
            segment = 1
        quote_url = self.URL + '/marketdata/instruments/quotes'
        payload_quote = {"instruments": [{"exchangeSegment": segment,"exchangeInstrumentID": token}],"xtsMessageCode": streamType,"publishFormat": "JSON"}
        quote_json = json.dumps(payload_quote)
        data = requests.request("POST", quote_url, data=quote_json, headers=self.MDheaders)
        # print(data.text)
        data1 = data.json()
        d = data1['result']['listQuotes'][0]
        d = json.loads(d)
        ltp = [d['AskInfo']['Price'],d['BidInfo']['Price']]
        return ltp
    except:
        print(sys.exc_info(),'get Quote')
