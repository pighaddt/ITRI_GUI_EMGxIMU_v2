import sys
from PyQt5 import QtBluetooth as QtBt
from PyQt5 import QtCore


class Application(QtCore.QCoreApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scan_for_devices()
        self.exec()

    def display_status(self):
        print(self.agent.isActive(), self.agent.discoveredDevices())

    def show_info(self, info: QtBt.QBluetoothDeviceInfo):
        print('Device discovered')
        print(info)
        print(f'Name: {info.name()}')
        print(f'UUID: {info.deviceUuid()}')
        print()
        pass

    def agent_finished(self,*args, **kwargs):
        print('Agent finished')
        print(f'args {args}')
        print(f'kwargs {kwargs}')

    def agent_error(self,*args, **kwargs):
        print('Agent error')
        print(f'args {args}')
        print(f'kwargs {kwargs}')

    def scan_for_devices(self):
        self.agent = QtBt.QBluetoothDeviceDiscoveryAgent()
        self.agent.setLowEnergyDiscoveryTimeout(5000)

        self.agent.deviceDiscovered.connect(self.show_info)
        self.agent.finished.connect(self.agent_finished)
        self.agent.error.connect(self.agent_error)

        timer = QtCore.QTimer(self.agent)
        timer.start(1000)
        timer.timeout.connect(self.display_status)

        self.agent.start()


if __name__ == '__main__':
    app = Application(sys.argv)