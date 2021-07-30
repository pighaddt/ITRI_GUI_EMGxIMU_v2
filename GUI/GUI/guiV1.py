import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from gui_v1 import Ui_MainWindow

import pyqtgraph as pg
import numpy as np
import threading
import serial
import openpyxl
import time

import serialDemo


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_miniWin)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_closeWin)
        self.ui.pushButton_btConnect.clicked.connect(self.searchComPort)
        self.ui.pushButton_connectBT.clicked.connect(self.connectBT)
        self.ui.pushButton_reset.clicked.connect(self.reset)
        self.p1, self.p2, self.p3, self.p4 = self.set_graph_ui()
        self.ui.pushButton_start.clicked.connect(self.threadStart)
        self.ui.pushButton_stop.clicked.connect(self.stopPlot)


    def pushButton_2_miniWin(self):
        self.showMinimized()
    def pushButton_3_closeWin(self):
        self.close()
    def reset(self):
        global comPortName, curve3
        self.ui.textEdit_btResult.clear()
        self.ui.comboBox_selectCom.clear()
        self.ui.label_BTConnected_Item.clear()
        comPortName = None
        curve3.clear()

    def searchComPort(self):
        self.ui.textEdit_btResult.setReadOnly(True)
        self.ui.textEdit_btResult.setText("Searching BT Device...")
        self.comPorResult = serialDemo.serial_ports()
        for i in range(len(self.comPorResult)):
            self.ui.textEdit_btResult.append(self.comPorResult[i])
            self.ui.comboBox_selectCom.addItem(self.comPorResult[i])

    def connectBT(self):
        global comPortName
        comPortName = self.ui.comboBox_selectCom.currentText()
        self.ui.label_BTConnected_Item.setText(str(comPortName))
        self.ui.textEdit_btResult.append("Connecting to {}...".format(str(comPortName)))


    def set_graph_ui(self):
        """
        settings (set 4 sub-windows) for pyqtgraph window (vertical layout)
        """
        global curve1, curve2, curve3, curve4
        pg.setConfigOptions(antialias=True)  # pg global variable setting function, antialias=True open curve anti-aliasing
        win = pg.GraphicsLayoutWidget()  # Create pg layout for automatic management of data interface layout
        win.setBackground('w')
        self.ui.verticalLayout.addWidget(win)

        # plot 1
        p1 = win.addPlot(title="Ch1: Target EMG data")  # Add the first drawing window
        p1.setLabel('left', text='mV', color='#000000')  # y axis setting function
        p1.showGrid(x=False, y=False)
        p1.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        # p1.setLabel('bottom', text='Time', color='#000000', units='s')  # x axis setting function
        # p1.setYRange(min=int(Y_EMG_range[0]), max=int(Y_EMG_range[1]))
        # p1.addLegend()
        curve1 = p1.plot(pen=pg.mkPen(color='k', width=2.0), name="Ch1: Target EMG data")

        # plot 2
        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p2 = win.addPlot(title="Ch2: Compensated EMG data")
        p2.setLabel('left', text='mV', color='#000000')
        p2.showGrid(x=False, y=False)
        p2.setLogMode(x=False, y=False)
        # p2.setLabel('bottom', text='Time', color='#000000', units='s')
        # p2.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        # p2.addLegend()
        curve2 = p2.plot(pen=pg.mkPen(color='k', width=2.0), name="Ch2: Compensated EMG data")

        # plot 3
        win.nextRow()
        c_range = [10, 600]
        p3 = win.addPlot(title="Capacitance")
        p3.setLabel('left', text='pF', color='#000000')
        p3.showGrid(x=False, y=False)
        p3.setLogMode(x=False, y=False)
        # p3.setLabel('bottom', text='Time', color='#000000', units='s')
        p3.setYRange(min=int(c_range[0]), max=int(c_range[1]))
        # p3.addLegend()
        curve3 = p3.plot(pen=pg.mkPen(color=(0, 0, 255), width=2.0), name="Capacitance")

        # plot 4
        win.nextRow()
        p4 = win.addPlot(title="Pressure")
        p4.setLabel('left', text='mmHg', color='#000000')
        p4.showGrid(x=False, y=False)
        p4.setLogMode(x=False, y=False)
        p4.setLabel('bottom', text='Time', color='#000000', units='s')
        # p4.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        # p4.addLegend()
        curve4 = p4.plot(pen=pg.mkPen(color='k', width=2.0), name="Pressure")

        return p1, p2, p3, p4



    def threadStart(self):
        thread = threading.Thread(target=self.start_plotC, name='thread')
        thread.start()



    def start_plotC(self):
        """
        Calculate capacitance and plot C curve on GUI
        """
        global curve3, Cvalue, portName
        # parameter settings for reading data
        self.ui.label_BTConnected_Item.text()
        self.portName = self.ui.label_BTConnected_Item.text()
        self.baudRate = 115200
        ser = serial.Serial(self.portName, int(self.baudRate), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
        self.samplePoint = 1000  # after how many points -> starting cal C
        self.thrd = 10  # how many periods would be cal
        # FW and HW Parameter settings
        self.R = 1 * 10 ** 6  # Ohm
        self.pwmPeriod = 2 * 10 ** (-3)  # sec
        self.sampleHZ = 6 * 10 ** 3  # Hz
        self.sampleRate = 1 / self.sampleHZ  # sec
        self.point = self.pwmPeriod // self.sampleRate
        self.tauPercent = 0.632
        # function
        def update(sample):
            """
            Load V_ADC raw data
            """
            Data = []
            print(time.ctime())
            for i in range(sample):
                value = str(ser.readline(), 'utf-8')
                if value != '\n':
                    # print(value)
                    Data.append(int(value) / 1000)
            print(Data)
            return Data
        def calcuC(Value):
            """
            The function of calculating capacitance by processing V_ADC raw data.
            """
            filterValue = Value
            # Find the minimum/maximun value of the curve by calculating the larger/smaller difference.
            diff, MaxIndx, MaxIndxValue, MinIndx, MinIndxValue = [], [], [], [], []
            for i in range(len(filterValue) - 1):
                diff.append(filterValue[i + 1] - filterValue[i])
            for i in range(self.thrd):
                maxIndx = np.argmax(diff)
                minIndx = np.argmin(diff)
                if maxIndx + int(self.point // 2) < len(filterValue):
                    if filterValue[maxIndx + int(self.point // 2)] > filterValue[maxIndx + int((self.point // 2) // 2)]:
                        if filterValue[maxIndx + 1] > filterValue[maxIndx] and filterValue[maxIndx - 1] > filterValue[
                            maxIndx]:
                            MaxIndx.append(maxIndx)
                            MaxIndxValue.append(filterValue[maxIndx])
                if minIndx + int(self.point // 2) < len(filterValue):
                    if filterValue[minIndx + int(self.point // 2)] < filterValue[minIndx + int((self.point // 2) // 2)]:
                        if filterValue[minIndx + 1] < filterValue[minIndx] and filterValue[minIndx - 1] < filterValue[
                            minIndx]:
                            MinIndx.append(minIndx)
                            MinIndxValue.append(filterValue[minIndx])
                diff[maxIndx] = 0
                diff[minIndx] = 0
            # Delete the error items of maximum/minimum value
            for i in range(len(MaxIndx)):
                for j in range(1, int(self.point // 2) - 1):
                    if filterValue[MaxIndx[i] + j] < filterValue[(MaxIndx[i] + 1)]:
                        MaxIndx[i] = 0
                        MaxIndxValue[i] = 0
            if MaxIndx.count(0):
                if 0 in MaxIndx:
                    MaxIndx.remove(0)
                    # MaxIndxValue.remove(0)
            for i in range(len(MinIndx)):
                for j in range(1, int(self.point // 2) - 1):
                    if filterValue[MinIndx[i] + j] > filterValue[(MinIndx[i] + 1)]:
                        MinIndx[i] = 0
                        MinIndxValue[i] = 0
            if MinIndx.count(0):
                if 0 in MinIndx:
                    MinIndx.remove(0)
                    # MinIndxValue.remove(0)
            ###
            # case 1: rise
            C_rise = []
            for p in range(len(MaxIndx)):
                V_tau = (filterValue[MaxIndx[p] + int(self.point // 2)] - filterValue[MaxIndx[p]]) * self.tauPercent + \
                        filterValue[
                            MaxIndx[p]]
                for i in range(int(self.point // 2) + 1):
                    if V_tau < filterValue[MaxIndx[p] + i]:
                        tauIndex = i - 1
                        break
                t_tau = float((V_tau - filterValue[MaxIndx[p] + tauIndex]) / (
                        filterValue[MaxIndx[p] + tauIndex + 1] - filterValue[
                    MaxIndx[p] + tauIndex])) * self.sampleRate + tauIndex * self.sampleRate
                C_rise.append(abs(t_tau) / self.R)
            # case 2: down
            C_down = []
            for p in range(len(MinIndx)):
                V_tau = (filterValue[MinIndx[p]] - (
                            filterValue[MinIndx[p]] - filterValue[MinIndx[p] + int(self.point // 2)]) * self.tauPercent)
                for i in range(int(self.point // 2) + 1):
                    if V_tau > filterValue[MinIndx[p] + i]:
                        tauIndex = i - 1
                        break
                t_tau = float((filterValue[MinIndx[p] + tauIndex] - V_tau) / (
                            filterValue[MinIndx[p] + tauIndex] - filterValue[
                        MinIndx[p] + tauIndex + 1])) * self.sampleRate + tauIndex * self.sampleRate
                C_down.append(abs(t_tau) / self.R)
                C_rise.append(abs(t_tau) / self.R)
            dic = {'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'Length of C': len(C_rise), 'Average capacitance value(F)': np.average(C_rise)}
            print(dic)
            print()
            return dic

        # Start calculating capacitance and update the value of pygraph window
        self.CdataWin = np.linspace(0, 0, 10)
        # while True:
        while self.portName is not None:
            self.CdataWin[:-1] = self.CdataWin[1:]
            # load signal
            self.Data = update(self.samplePoint)

            # calculate C
            self.Cmessage = calcuC(self.Data)

            # Transform C data into value for importing to pygraph and C value label
            self.secVal = int(str(self.Cmessage['time'])[-2:])
            self.Cvalue = float(round(float(self.Cmessage['Average capacitance value(F)'])/(10**(-12)), 3))
            print("#################", self.secVal, self.Cvalue)
            self.CdataWin[-1] = self.Cvalue
            curve3.setData(self.CdataWin)
            QtGui.QApplication.processEvents()

            self.ui.label_capaci_val.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.label_capaci_val.setText(str(self.Cvalue))




    def stopPlot(self):
        self.portName = None




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    # window.showFullScreen()
    sys.exit(app.exec_())



