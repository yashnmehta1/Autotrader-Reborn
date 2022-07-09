import socketio
import sys
from Application.Utils.configReader import *


class MDSocket_io(socketio.Client):

    def __init__(self, token, userID, reconnection=True, reconnection_attempts=0, reconnection_delay=1,
                 reconnection_delay_max=5, randomization_factor=0.5, logger=False, binary=False, json=None, **kwargs):
        self.sid = socketio.Client(logger=False)
        self.eventlistener = self.sid
        self.MDheaders, self.IAheaders, self.MDToken, self.IAToken, self.port, self.userID, self.source ,self.MDKey,self.MDSecret,self.IAKey,self.IASecret,self.client_list,DClient,broadcastMode= readConfig_All()
        self.broadcastMode = 'Partial'
        publishFormat = 'JSON'
        token = token
        port = f'{self.port}/?token='
        self.connection_url = port + token + '&userID=' + self.userID + '&publishFormat=' + publishFormat + '&broadcastMode=' + self.broadcastMode


    def connect(self, headers={}, transports='websocket', namespaces=None, socketio_path='/marketdata/socket.io',
                verify=False):
        try:
            url = self.connection_url
            self.sid.connect(url, headers, transports, namespaces, socketio_path)
            self.sid.wait()
            self.sid.disconnect()
        except:
            print(sys.exc_info(),'soc connect')


    def get_emitter(self):
        return self.eventlistener
