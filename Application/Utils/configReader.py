import sys
import traceback
import datetime
import logging
import os
import Application.Utils.cst
import base64
import json
#######################################################################################################################

global MDheaders,IAheaders,MDtoken,IAToken,URL,userID,Source,MDKey,MDSecret,IAKey,IASecret,cList,DClient,broadcastMode
loc1 = os.getcwd().split('Application')
config_location =os.path.join( loc1[0],  'Resourses','config_json.json')

#######################################################################################################################
def readConfig_All():
    try:
        f1 = open(config_location)
        jConfig = json.load(f1)
        MDtoken = jConfig['MDToken']['token']
        IAToken = jConfig['IAToken']['token']
        userID = jConfig['userID']
        URL = jConfig['url']
        Source = jConfig['Credentials']['source']
        MDKey = jConfig['Credentials'] ['marketdata_appkey']
        MDSecret =jConfig['Credentials'] ['marketdata_secretkey']
        IAKey = jConfig['Credentials'] ['interactive_appkey']
        IASecret = jConfig['Credentials'] ['interactive_secretkey']
        cList = jConfig['IAToken'] ['Client_list']
        IAheaders = {
            'authorization': IAToken,
            'Content-Type': 'application/json'
        }
        MDheaders = {
            'authorization': MDtoken,
            'Content-Type': 'application/json'
        }
        # loginid = jConfig['MDToken'] ['loginid']
        DClient = jConfig['DefaultClient']
        broadcastMode = jConfig ['broadcastmode']
        f1.close()
        return (MDheaders,IAheaders,MDtoken,IAToken,URL,userID,Source,MDKey,MDSecret,IAKey,IASecret,cList,DClient,broadcastMode)
    except:
        logging.error(sys.exc_info()[1])
#####################################################################################
#####################################################################################


def writeITR(token,userID,client_list):
    try:
        # print('IAS Token',token)
        f1 = open(config_location)
        jConfig = json.load(f1)
        f1.close()
        now = datetime.datetime.now()
        current_date = now.strftime("%y-%m-%d")
        current_time = now.strftime("%H:%M:%S")

        jConfig['IAToken'] ['token']= token
        jConfig ['userID']= userID
        jConfig['IAToken'] ['login_date']= current_date
        jConfig['IAToken'] ['login_time']= current_time
        jConfig['IAToken'] ['Client_list']= client_list

        jConfig_new = json.dumps(jConfig,indent=4)

        f2 = open(config_location,'w')
        f2.write(jConfig_new)
        f2.close()
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])



def writeMD(token,userID):
    try:
        f1 = open(config_location)
        jConfig = json.load(f1)
        f1.close()
        now = datetime.datetime.now()
        current_date = now.strftime("%y-%m-%d")
        current_time = now.strftime("%H:%M:%S")

        jConfig['MDToken']['token'] =token
        jConfig['userID'] =userID
        jConfig['MDToken']['login_time']= current_time

        jConfig_new = json.dumps(jConfig,indent=4)

        f2 = open(config_location,'w')
        f2.write(jConfig_new)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])

def writeURL(a):
    try:
        if(a=='ARHAM_DIRECT'):
            url = cst.ZD
        elif(a=='ARHAM_WEB'):
            url = cst.ZW
        elif (a =='TRADECIRCLE_DIRECT' ):
            url = cst.SD
        elif (a == 'TRADECIRCLE_WEB'):
            url = cst.SW
        elif (a == 'UAT'):
            url = cst.XD
        elif (a == 'UAT_WEB'):
            url = cst.XW
        url1 = base64.urlsafe_b64decode(url.encode("utf-8")).decode('utf-8')
        f1 = open(config_location)
        jConfig = json.load(f1)
        jConfig[ 'url']= url1

        f1.close()
        jConfig_new = json.dumps(jConfig,indent=4)
        f2 = open(config_location,'w')
        f2.write(jConfig_new)
    except:
        logging.error(sys.exc_info()[1])



# def updateConfig(MDKey = '',MDSecret = '',IAKey = '',IASecret = '',LoginID = ''):
#
#     ######################################################################################
#     if(MDKey != ''):
#         config.set('Credentials', 'marketdata_appkey', MDKey)
#     elif(MDSecret != ''):
#         config.set('Credentials', 'marketdata_secretkey', MDSecret)
#     elif(IAKey != ''):
#         config.set('Credentials', 'interactive_appkey', IAKey)
#     elif(IASecret != ''):
#         config.set('Credentials', 'interactive_secretkey', IASecret)
#     elif(LoginID != ''):
#         config.set('MDToken', 'loginid', LoginID)
#     ########################################################################################
#
#     with open(config_location, 'w') as f:
#         config.write(f)
#


def readLoginId():
    try:
        f1 = open(config_location)
        jConfig = json.load(f1)
        loginid = jConfig['MDToken'] ['loginid']
        f1.close()

        return loginid
    except:
        logging.error(sys.exc_info()[1])



def get_udp_port(self):
    try:
        f1 = open(config_location)
        jConfig = json.load(f1)
        self.port_fo = jConfig['UDP_FO']
        self.port_cash = jConfig['UDP_CASH']
        f1.close()
    except:
        logging.error(sys.exc_info()[1])




def readClist():
    try:
        f1 = open(config_location)
        jConfig = json.load(f1)
        cList = jConfig['IAToken'] ['Client_list']
        f1.close()
        return cList
    except:
        logging.error(sys.exc_info()[1])

def readBroadcastMode():
    try:
        f1 = open(config_location)
        jConfig = json.load(f1)
        broadcastMode = jConfig ['broadcastmode']

        f1.close()

        return broadcastMode
    except:
        logging.error(sys.exc_info()[1])


def readDefaultClient():
    try:
        f1 = open(config_location)
        jConfig = json.load(f1)
        DClient = jConfig['DefaultClient']

        f1.close()

        return DClient
    except:
        logging.error(sys.exc_info()[1])

def refresh(self):
    # print(readConfig_All())readConfig_All
    try:
        # print('config file refreshed for ',self)
        self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.URL, self.userID, self.Source, self.MDKey, self.MDSecret, self.IAKey, self.IASecret, self.clist, self.DClient, self.broadcastMode = readConfig_All()
    except:
        print(traceback.print_exc())

def all_refresh_config(self):
    try:
        # print('cofing all refresh start')
        refresh(self)
        refresh(self.LiveFeed)
        refresh(self.IAS)
        refresh(self.marketW)
        refresh(self.PendingW)
        refresh(self.snapW)
        refresh(self.multiModifyW)
        # print('cofing all refresh end')
    except:
        print(traceback.print_exc(),'all config refresh')
