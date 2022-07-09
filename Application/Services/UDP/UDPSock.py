from PyQt5.QtNetwork import QUdpSocket,QHostAddress
from PyQt5 import QtCore, QtNetwork
import lzo
import struct

class Receiver(QtCore.QObject):
    def __init__(self,port):
        self.port = port
        super(Receiver, self).__init__()
        self._socket = QtNetwork.QUdpSocket(self)
        self._socket.bind(QHostAddress.AnyIPv4, self.port)
        self._socket.readyRead.connect(self.on_readyRead)


    def join_grp(self):
        self._socket.joinMulticastGroup(QHostAddress('233.1.2.5'))
    def leave_grp(self):
        self._socket.leaveMulticastGroup(QHostAddress('233.1.2.5'))

    @QtCore.pyqtSlot()
    def on_readyRead(self):
        while self._socket.hasPendingDatagrams():
            packet, host, port = self._socket.readDatagram(
                self._socket.pendingDatagramSize()
            )
            self.parsePacket(packet,port)


    def parsePacket(self, packet,port):
        pstp = 4
        iNoOfPsckt= struct.unpack('!h', packet[2:4])[0]
        for i in range(iNoOfPsckt):
            icomplen = struct.unpack('!h', packet[pstp:pstp+2])[0]
            petp = pstp+2+icomplen
            if (icomplen == 0):
                pass
            else:
                compressed_packet = packet[pstp+2: pstp+icomplen+2]
                decoded_packet = lzo.lzo1z.decompress_safe(compressed_packet, 1000)
                a = decoded_packet
                mc = struct.unpack('!h', a[18:20])
                if (mc[0] == 7202 and port == 35099):
                    noOfRec = struct.unpack('!h', a[48:50])
                    stp = 50
                    for ik in range(noOfRec[0]):
                        edp = stp + 26
                        token, mt, fillp, fillVol, oi, dhoi, dloi = struct.unpack('!lhlllll', a[stp:edp])
                        lua = self.contract_fo[token-35000]
                        print(lua,fillp)

                        # prevVol =self.contract_fo[token-35000, 28]
                        # prevAmt =self.contract_fo[token-35000, 29]
                        # newVol = prevVol + fillVol
                        # newAmt = prevAmt + (fillVol*fillp)/100000.0
                        # atp = newAmt/newVol*1000
                        # self.OC1[indxNo, [2,3,4,5]] = [fillp/100.0  ,newVol, newAmt,atp]
                        stp = edp
                elif (mc[0] == 7208 and port == 35099):
                    noOfRec = struct.unpack('!h', decoded_packet[48:50])
                    stp = 50

                    for ik in range(noOfRec[0]):
                        edp = stp + 214
                        token = struct.unpack('!l',decoded_packet[stp:stp+4])[0]
                        vol = struct.unpack('!l',decoded_packet[stp+8:stp+12])[0]
                        ltp = struct.unpack('!l',decoded_packet[stp+12:stp+16])[0]/100.0

                        nc = struct.unpack('!l',decoded_packet[stp+18:stp+22])[0]/100.0
                        ltq = struct.unpack('!l',decoded_packet[stp+22:stp+26])[0]
                        ltt = struct.unpack('!l',decoded_packet[stp+25:stp+29])
                        atp = struct.unpack('!l',decoded_packet[stp+30:stp+34])[0]
                        cls = struct.unpack('!l',decoded_packet[stp+198:stp+202])[0]/100.0
                        opn = struct.unpack('!l',decoded_packet[stp+202:stp+206])[0]/100.0
                        nci = struct.unpack('!c',decoded_packet[stp+16:stp+17])[0].decode('UTF-8')
                        high = struct.unpack('!l',decoded_packet[stp+206:stp+210])[0]/100.0
                        low = struct.unpack('!l',decoded_packet[stp+210:stp+214])[0]/100.0

                        lua = self.contract_fo[token-35000]
                        stp = edp

                elif (mc[0] == 7202 and port ==34077):
                    noOfRec = struct.unpack('!h', a[48:50])
                    stp = 50

                    for ik in range(noOfRec[0]):
                        edp = stp + 16
                        token, mt, fillp, fillVol, miv = struct.unpack('!hhlll', a[stp:edp])
                        lua = self.contract_fo[token-35000]
                        # print(token)

                elif (mc[0] == 7208  and port ==34077):
                    noOfRec = struct.unpack('!h', decoded_packet[48:50])
                    # print(noOfRec)
                    stp = 50

                    for ik in range(noOfRec[0]):
                        edp = stp + 212

                        # print(decoded_packet[stp+14:stp+17])
                        token = struct.unpack('!h',decoded_packet[stp:stp+2])[0]
                        vol = struct.unpack('!l',decoded_packet[stp+6:stp+10])[0]
                        ltp = struct.unpack('!l',decoded_packet[stp+10:stp+14])[0]/100.0
                        nci = struct.unpack('!c',decoded_packet[stp+14:stp+15])[0].decode('UTF-8')

                        nc = struct.unpack('!l',decoded_packet[stp+16:stp+20])[0]/100.0
                        ltq = struct.unpack('!l',decoded_packet[stp+20:stp+24])[0]
                        ltt = struct.unpack('!l',decoded_packet[stp+24:stp+28])
                        atp = struct.unpack('!l',decoded_packet[stp+28:stp+32])[0]
                        cls = struct.unpack('!l',decoded_packet[stp+196:stp+200])[0]/100.0
                        opn = struct.unpack('!l',decoded_packet[stp+200:stp+204])[0]/100.0
                        high = struct.unpack('!l',decoded_packet[stp+204:stp+208])[0]/100.0
                        low = struct.unpack('!l',decoded_packet[stp+208:stp+212])[0]/100.0
                        print(ltt)
                        stp = edp
                elif(mc[0] == 7207  and port ==34077):
                    pass










if __name__ == "__main__":
    import sys
    app = QtCore.QCoreApplication(sys.argv)

    receiver1 = Receiver(34077)
    thread = QtCore.QThread()
    thread.start()
    receiver1.moveToThread(thread)

    receiver2 = Receiver(35099)
    thread2 = QtCore.QThread()
    thread2.start()
    receiver2.moveToThread(thread2)


    sys.exit(app.exec_())


