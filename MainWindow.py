import serial
from PyQt5 import QtWidgets, QtGui, QtCore
import sys

from PyQt5.QtWidgets import QApplication
from numpy import linspace

from Ui_MainWindow import Ui_MainWindow
import pyqtgraph as pg
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        global isSerialPort
        isSerialPort = False
        super(MainWindow, self).__init__() #inherit Mainwindow super function
        self.ui = Ui_MainWindow() # your mainwindow from pyuic5
        self.ui.setupUi(self) # your init setupUI function
        self.p1, self.p2, self.p3, self.p4 = self.set_graph_ui()  # set the drawing window
        self.ui.pushButton.clicked.connect(self.plot_EMG_IMU_Data)
        self.comPortSetting()
        self.EMGIMUDataSetting()

        # while True:
        #     self.plot_EMG_IMU_Data()

    def comPortSetting(self):
        global ser1, portName1, baudRate1
        # Create object serial port
        portName1 = "COM9"
        baudRate1 = 9600  # FW1.0 115200 FW2.0 9600
        ser1 = serial.Serial(portName1, int(baudRate1), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
        data = ser1.readline().decode("utf-8", errors='ignore')
        print(data)
    def EMGIMUDataSetting(self):
        global EMGData, IMU1Data, IMU2Data, IMU3Data, ZeroData
        windowWidth_EMG = 1000
        EMGData = linspace(0, 0, windowWidth_EMG)  # create array that will contain the relevant time series
        windowWidth_IMU = 100
        IMU1Data = linspace(0, 0, windowWidth_IMU)  # create array that will contain the relevant time series
        IMU2Data = linspace(0, 0, windowWidth_IMU)  # create array that will contain the relevant time series
        IMU3Data = linspace(0, 0, windowWidth_IMU)  # create array that will contain the relevant time series
        ZeroData = linspace(0, 0, windowWidth_IMU)

    def set_graph_ui(self):
        global curve1, curve2, curve3, curve4
        Y_EMG_range = [-3000, 3000]
        pg.setConfigOptions(antialias=True)  # pg global variable setting function, antialias=True open curve anti-aliasing
        win = pg.GraphicsLayoutWidget()  # Create pg layout for automatic management of data interface layout
        win.setBackground('w')
        # pg The drawing window can be added to the graph_layout in the GUI as a widget, and of course can be added to all other Qt containers.
        # self.verticalLayoutWidget.addWidget(win)
        self.ui.verticalLayout.addWidget(win)
        p1 = win.addPlot(title="EMG Raw Data")  # Add the first drawing window
        p1.setLabel('left', text='mV', color='#000000')  # y axis setting function
        p1.showGrid(x=False, y=False)  # Grid setting function
        p1.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        p1.setLabel('bottom', text='points', color='#000000', units='s')  # x axis setting function
        p1.setYRange(min=int(Y_EMG_range[0]), max=int(Y_EMG_range[1]))
        p1.addLegend() # Select whether to add legend

        curve1 = p1.plot(pen=pg.mkPen(color='k', width=2.0), name="EMG Raw Data")  ##pitch EMG


        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        Y_IMU_range = [-180, 180]
        p2 = win.addPlot(title="IMU 1 Raw Data")
        p2.setLabel('left', text='angle', color='#000000')
        p2.showGrid(x=False, y=False)
        p2.setLogMode(x=False, y=False)
        p2.setLabel('bottom', text='points',color='#000000' ,  units='s')
        p2.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        p2.addLegend()
        curve2 = p2.plot(pen=pg.mkPen(color='k', width=2.0), name="IMU 1 Pitch")  ##pitch EMG


        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p3 = win.addPlot(title="IMU 2 Raw Data")
        p3.setLabel('left', text='angle', color='#000000')
        p3.showGrid(x=False, y=False)
        p3.setLogMode(x=False, y=False)
        p3.setLabel('bottom', text='points', color='#000000', units='s')
        p3.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        p3.addLegend()
        curve3 = p3.plot(pen=pg.mkPen(color='k', width=2.0), name="IMU 2 Pitch")  ##pitch EMG


        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p4 = win.addPlot(title="IMU 3 Raw Data")
        p4.setLabel('left', text='angle', color='#000000')
        p4.showGrid(x=False, y=False)
        p4.setLogMode(x=False, y=False)
        p4.setLabel('bottom', text='points', color='#000000', units='s')
        p4.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        p4.addLegend()
        curve4 = p4.plot(pen=pg.mkPen(color='k', width=2.0), name="IMU 3 Pitch")  ##pitch EMG


        return p1, p2, p3, p4

    # def update(self):
    #     global curve, curve2, ptr, pitch, roll
    #     data = ser.readline().decode("utf-8", errors="ignore")
    #     if len(data) > 1:
    #         data = str(data)
    #         data = data[4:-2]
    #         splitData = data.split(',')
    #         pitchStr = splitData[0]
    #         rollStr = splitData[1]
    #         pitch[:-1] = pitch[1:]  # shift pitch data in the temporal mean 1 sample left
    #         roll[:-1] = roll[1:]  # shift roll data in the temporal mean 1 sample left
    #
    #         pitch[-1] = float(pitchStr[2:])  # pitchStr : R= pitch
    #         roll[-1] = float(rollStr[2:])  # vector containing the instantaneous values
    #         ptr += 1  # update x position for displaying the curve
    #         curve.setData(pitch)  # set the curve with these data
    #         curve2.setData(roll)  # set the curve with these data
    #         # curve.setPos(ptr, 0)  # set x posiYtion in the graph to 0
    #         QtGui.QApplication.processEvents()  # process the plot now

    def plot_EMG_IMU_Data(self):
        global curve1, curve2, curve3, curve4 , EMGData, IMU1Data, IMU2Data, IMU3Data, ser1, isSerialPort, portName1, baudRate1, ZeroData

        if isSerialPort==False:
            self.ui.pushButton.setText("Close Serial Port")
            isSerialPort = True
            while True:
                # if ser1.isOpen() == False:
                #     ser1.open()
                # print(portName1, baudRate1)
                # ser1 = serial.Serial(portName1, int(baudRate1), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
                data = ser1.readline().decode("utf-8", errors='ignore')
                # ser1.
                print(data)
                if len(data) > 1:
                    data = str(data)
                    data = data[4:-2]
                    splitData = data.split(',')
                    pitchStr = splitData[0]
                    rollStr = splitData[1]
                    IMU1Data[:-1] = IMU1Data[1:]  # shift pitch data in the temporal mean 1 sample left
                    IMU2Data[:-1] = IMU2Data[1:]  # shift roll data in the temporal mean 1 sample left

                    IMU1Data[-1] = float(pitchStr[2:])  # pitchStr : R= pitch
                    IMU2Data[-1] = float(rollStr[2:])  # vector containing the instantaneous values
                    curve2.setData(IMU1Data)  # set the curve with these data
                    curve3.setData(IMU2Data)  # set the curve with these data
                    # curve.setPos(ptr, 0)  # set x posiYtion in the graph to 0
                    QApplication.processEvents()  # process the plot now

        # else:
        #     self.ui.pushButton.setText('Open Serial Port')
        #     # ser1.close()
        #     # ser1.open()
        #     curve2.setData(ZeroData)  # set the curve with these data
        #     curve3.setData(ZeroData)  # set the curve with these data
        #     # curve.setPos(ptr, 0)  # set x posiYtion in the graph to 0
        #     QApplication.processEvents()  # process the plot now
        #     isSerialPort = False
        #     print()



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.instance().exec_())