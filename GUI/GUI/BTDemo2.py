import sys
from PyQt5.QtBluetooth import *
from PyQt5.QtCore import *
# http://python.6.x6.nabble.com/QBluetooth-support-for-a-PyQT-Bluetooth-Server-td5254657.html

class BTServer(QCoreApplication):
    '''
        Class based on: https://doc.qt.io/qt-5/qtbluetooth-btchat-example.html
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.startServer()

    def startServer(self, localAdapter=QBluetoothAddress()):
        self.rfcommServer = QBluetoothServer(QBluetoothServiceInfo.RfcommProtocol)
        self.rfcommServer.newConnection.connect(self.clientConnected)
        self.result = self.rfcommServer.listen(localAdapter)
        self.clientSockets = []
        if not self.result:
            print("Cannot bind chat server to: " + localAdapter.toString())
        self.serviceInfo = QBluetoothServiceInfo()
        self.serviceInfo.setAttribute(QBluetoothServiceInfo.ServiceName, "iphone")
        self.serviceInfo.setAttribute(QBluetoothServiceInfo.ServiceDescription,
                         "Example bluetooth chat server")
        self.serviceInfo.setAttribute(QBluetoothServiceInfo.ServiceProvider, "qt-project.org")
        self.serviceUuid = QBluetoothUuid("e0cbf06c-cd8b-4647-bb8a-263b43f0f974")
        self.serviceInfo.setServiceUuid(QBluetoothUuid(self.serviceUuid))
        self.PublicBrowseGroup = [QVariant(QBluetoothUuid(QBluetoothUuid.PublicBrowseGroup))]
        self.serviceInfo.setAttribute(QBluetoothServiceInfo.BrowseGroupList, self.PublicBrowseGroup)
        self.protocolDescriptorList = [QBluetoothUuid(QBluetoothUuid.L2cap),
                                       QBluetoothUuid(QBluetoothUuid.Rfcomm),
                                       int(self.rfcommServer.serverPort())]
        print(self.protocolDescriptorList)
        self.serviceInfo.setAttribute(QBluetoothServiceInfo.ProtocolDescriptorList,
                         self.protocolDescriptorList);
        self.serviceInfo.registerService(localAdapter)

    def clientConnected(self,*args, **kwargs):
        self.socket = self.rfcommServer.nextPendingConnection()
        if not self.socket:
            return
        self.rfcommServer.readyRead.connect(self.readSocket)
        self.rfcommServer.disconnected.connect(self.clientDisconnected)
        self.clientSockets.append(self.socketBT)
        print(self.socketBT.peerName())
    def readSocket(self,*args, **kwargs):
        print("Socket data")
    def clientDisconnected(self,*args, **kwargs):
        print("Client Disconected")

if __name__ == '__main__':
    app = BTServer(sys.argv)