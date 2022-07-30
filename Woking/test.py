import  requests
from Application.Utils.configReader import *

print( os.getcwd())
loc1 = os.getcwd().split('Woking')
config_location =os.path.join( loc1[0],  'Resourses','config_json.json')
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
def getQuote(token, seg, streamType):
    try:
        MDheaders, IAheaders, MDtoken, IAToken, URL, userID, Source, MDKey, MDSecret, IAKey, IASecret, cList, DClient, broadcastMode = readConfig_All()
        if (seg == 'NSEFO'):
            segment = 2
        elif (seg == 'NSECM'):
            segment = 1
        quote_url = URL + '/marketdata/instruments/quotes'
        payload_quote = {"instruments": [{"exchangeSegment": segment,"exchangeInstrumentID": token}],"xtsMessageCode": streamType,"publishFormat": "JSON"}
        quote_json = json.dumps(payload_quote)
        data = requests.request("POST", quote_url, data=quote_json, headers=MDheaders)
        print(data.text)
        data1 = data.json()
        d = data1['result']['listQuotes'][0]
        d = json.loads(d)
        ltp = [d['AskInfo']['Price'],d['BidInfo']['Price']]
        return ltp
    except:
        print(sys.exc_info(),'get Quote')


getQuote(53734,'NSEFO',1501)