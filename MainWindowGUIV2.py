import csv
import os
import threading

import PyQt5
import numpy
import serial
from PyQt5 import QtWidgets, QtCore
import sys

from PyQt5.QtWidgets import QFileDialog
from numpy import linspace

import RMSDetect
from GUI.GUI import serialDemo
import pyqtgraph as pg

import matplotlib

from datetime import date
from datetime import datetime

from GUI_EMG_IMU_v2 import Ui_MainWindow

matplotlib.use("Qt5Agg")  # 声明使用QT5
import pandas as pd

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class SignalCommunicate(PyQt5.QtCore.QObject):
    request_Device1graph_update = PyQt5.QtCore.pyqtSignal()
    request_Device2graph_update = PyQt5.QtCore.pyqtSignal()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__() #inherit Mainwindow super function
        self.ui = Ui_MainWindow() # your mainwindow from pyuic5
        self.ui.setupUi(self) # your init setupUI function
        # self.p1, self.p2, self.p3, self.p4 = self.set_graph2_ui()  # set the drawing window
        self.p1, self.p2, self.p3 = self.set_graph2_ui()  # set the drawing window
        self.p4, self.p5 = self.set_graph3_ui()  # set the drawing window
        # self.ui.pushButton_StartPlot.clicked.connect(self.threadStart)
        self.ui.pushButton_ConnectDevice1.clicked.connect(self.connectDevice1SP)
        self.ui.pushButton_ConnectDevice2.clicked.connect(self.connectDevice2SP)
        self.ui.pushButton_StartDevice1Plot.clicked.connect(self.threadDevice1Start)
        self.ui.pushButton_CloseDevice1Plot.clicked.connect(self.stop_Device1plot)
        self.ui.pushButton_StartDevice2Plot.clicked.connect(self.threadDevice2Start)
        self.ui.pushButton_CloseDevice2Plot.clicked.connect(self.stop_Device2plot)
        self.ui.pushButton_searchSP.clicked.connect(self.searchComPort)
        self.ui.pushButton_LoadDevice1.clicked.connect(self.loadDevice1)
        self.ui.pushButton_LoadDevice2.clicked.connect(self.loadDevice2)
        self.ui.checkBox_EMGDevice1.clicked.connect(self.EMGDevice1Click)
        self.ui.checkBox_EMGDevice2.clicked.connect(self.EMGDevice2Click)
        self.ui.pushButton_SaveDevice1Data.clicked.connect(self.Device1SaveData)
        self.ui.pushButton_SaveDevice2Data.clicked.connect(self.Device2SaveData)
        self.ui.pushButton_Reset.clicked.connect(self.reset)
        # self.comPortSetting()
        self.EMGIMUDataSetting()
        self.bpsArray = ['4800', '9600', '115200']
        self.initSet()
        self.IMUindex = 0

        # Signals that can be emitted
        self.signalComm = SignalCommunicate()
        # Update graph whenever the 'request_graph_update' signal is emitted
        self.signalComm.request_Device1graph_update.connect(self.update_Device1graph)
        self.signalComm.request_Device2graph_update.connect(self.update_Device2graph)

        # matplotlib  figure instance to plot on
        self.figure1 = plt.figure()
        self.figure2 = plt.figure()
        self.figure3 = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas3 = FigureCanvas(self.figure3)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        # self.toolbar = NavigationToolbar(self.canvas, self)
        # set the layout
        # layout.addWidget(self.toolbar)
        self.ui.verticalLayout_3.addWidget(self.canvas1)
        self.ui.verticalLayout_4.addWidget(self.canvas2)
        self.ui.verticalLayout_5.addWidget(self.canvas3)
        today = date.today()
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        d1 = today.strftime("%b-%d-%Y")
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        self.storagePathDevice1 = f"{desktop}\\{d1}{current_time}Device1.csv"
        self.storagePathDevice2 = f"{desktop}\\{d1}{current_time}Device2.csv"

        matplotlib.rcParams.update({'font.size': 8})

    def EMGIMUDataSetting(self):
        self.DefaultAngle = 60
        self.DataList = []
        self.Index = 0
        self.windowWidth_Device1 = 1000
        self.windowWidth_Device2 = 100
        #Device1 2 EMG signal + 1 IMU Signal
        self.Device1EMG1 = linspace(0, 0, self.windowWidth_Device1)
        self.Device1EMG2= linspace(0, 0, self.windowWidth_Device1)

        self.Device1IMUPitch = linspace(0, 0, int(self.windowWidth_Device1 / 5))  # create array that will contain the relevant time series
        self.Device1IMURoll = linspace(0, 0, self.windowWidth_Device1)  # create array that will contain the relevant time series
        self.DeviceAnle = linspace(0,0, int(self.windowWidth_Device1 / 5))
        #Device2  1 IMU Signal
        
        self.Device2IMUPitch = linspace(0, 0, self.windowWidth_Device2)  # create array that will contain the relevant time series
        self.Device2IMURoll = linspace(0, 0, self.windowWidth_Device2)  # create array that will contain the relevant time series


    def initSet(self):
        for i in range(len(self.bpsArray)):
            self.ui.comboBox_Device1BR.addItem(self.bpsArray[i])
            self.ui.comboBox_Device2BR.addItem(self.bpsArray[i])
        self.ui.comboBox_Device1BR.setCurrentIndex(2) #Device1 init buad rate 115200
        self.ui.comboBox_Device2BR.setCurrentIndex(2) #Device2 init buad rate 115200

    def searchComPort(self):
        self.ui.textEdit_info.setReadOnly(True)
        self.ui.textEdit_info.setText("Searching BT Device...")
        self.comPorResult = serialDemo.serial_ports()
        for i in range(len(self.comPorResult)):
            self.ui.textEdit_info.append(self.comPorResult[i])
            self.ui.comboBox_Device1CP.addItem(self.comPorResult[i])
            self.ui.comboBox_Device2CP.addItem(self.comPorResult[i])

    def reset(self):
        global curve1, curve2, curve3, curve4, curve5
        self.ui.comboBox_Device1CP.clear()
        self.ui.comboBox_Device2CP.clear()
        self.ui.textEdit_info.clear()
        self.comPortDevice1 = None
        self.comPortDevice2 = None
        self.ui.comboBox_Device1CP.clear()
        self.ui.comboBox_Device2CP.clear()
        curve1.clear()
        curve2.clear()
        curve3.clear()
        curve4.clear()
        curve5.clear()

    def connectDevice1SP(self):
        self.comPortDevice1 = self.ui.comboBox_Device1CP.currentText()
        self.baudRateDevice1 = self.ui.comboBox_Device1BR.currentText()
        self.serDevice1 = serial.Serial(self.comPortDevice1, int(self.baudRateDevice1), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
        # self.serDevice1.flushInput()
        self.ui.textEdit_info.append(" Device 1 Connecting to {}...".format(str(self.comPortDevice1)))

    def connectDevice2SP(self):
        self.comPortDevice2 = self.ui.comboBox_Device2CP.currentText()
        self.baudRateDevice2 = self.ui.comboBox_Device2BR.currentText()
        self.serDevice2 = serial.Serial(self.comPortDevice2, int(self.baudRateDevice2), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
        self.ui.textEdit_info.append("Device 2 Connecting to {}...".format(str(self.comPortDevice2)))


    def set_graph2_ui(self):
        global curve1, curve2, curve3, curve_roll, curve_angle
        Y_EMG_range = [-2000, 2000]
        Y_IMU_range = [-180, 180]

        pg.setConfigOptions(antialias=True)  # pg global variable setting function, antialias=True open curve anti-aliasing
        win = pg.GraphicsLayoutWidget()  # Create pg layout for automatic management of data interface layout
        win.setBackground('w')
        # pg The drawing window can be added to the graph_layout in the GUI as a widget, and of course can be added to all other Qt containers.
        # self.verticalLayoutWidget.addWidget(win)
        self.ui.verticalLayout.addWidget(win)
        p1 = win.addPlot(title="Device 1 EMG 1 Raw Data")  # Add the first drawing window
        p1.setLabel('left', text='mV', color='#000000')  # y axis setting function
        p1.showGrid(x=False, y=False)  # Grid setting function
        p1.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        p1.setLabel('bottom', text='points', color='#000000', units='s')  # x axis setting function
        p1.setYRange(min=int(Y_EMG_range[0]), max=int(Y_EMG_range[1]))
        p1.addLegend() # Select whether to add legend

        curve1 = p1.plot(pen=pg.mkPen(color='k', width=2.0), name="EMG 1 Raw Data")  ##pitch EMG


        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p2 = win.addPlot(title="Device 1 EMG 2 Raw Data")
        p2.setLabel('left', text='mV', color='#000000')
        p2.showGrid(x=False, y=False)
        p2.setLogMode(x=False, y=False)
        p2.setLabel('bottom', text='points',color='#000000' ,  units='s')
        p2.setYRange(min=int(Y_EMG_range[0]), max=int(Y_EMG_range[1]))
        p2.addLegend()
        curve2 = p2.plot(pen=pg.mkPen(color='r', width=2.0), name="EMG 2 Raw Data")  ##pitch EMG


        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p3 = win.addPlot(title="Device 2 IMU 2 Raw Data")
        p3.setLabel('left', text='angle', color='#000000')
        p3.showGrid(x=False, y=False)
        p3.setLogMode(x=False, y=False)
        p3.setLabel('bottom', text='points', color='#000000', units='s')
        #pitch and roll
        # p3.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        #angle Device1 and Device2
        p3.setYRange(min=int(0), max=int(150))
        p3.addLegend()
        curve3 = p3.plot(pen=pg.mkPen(color='b', width=2.0), name="IMU 1 Pitch")  ##pitch EMG
        curve_roll = p3.plot(pen=pg.mkPen(color='r', width=2.0), name="IMU 1 Roll")  ##roll curve
        curve_angle = p3.plot(pen=pg.mkPen(color='g', width=3.0), name="IMU Angle")  ##angle curve

        return p1, p2, p3

    def set_graph3_ui(self):
        global curve4, curve5
        Y_IMU_range = [-180, 180]
        pg.setConfigOptions(
            antialias=True)  # pg global variable setting function, antialias=True open curve anti-aliasing
        win = pg.GraphicsLayoutWidget()  # Create pg layout for automatic management of data interface layout
        win.setBackground('w')
        # pg The drawing window can be added to the graph_layout in the GUI as a widget, and of course can be added to all other Qt containers.
        # self.verticalLayoutWidget.addWidget(win)
        self.ui.verticalLayout_2.addWidget(win)
        p4 = win.addPlot(title="Device 2 IMU 2 Raw Data")  # Add the first drawing window
        p4.setLabel('left', text='mV', color='#000000')  # y axis setting function
        p4.showGrid(x=False, y=False)  # Grid setting function
        p4.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        p4.setLabel('bottom', text='points', color='#000000', units='s')  # x axis setting function
        p4.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        # p5.setXRange(0, 1000) # bigger than 1000 will use k units
        p4.addLegend()  # Select whether to add legend

        curve4 = p4.plot(pen=pg.mkPen(color='k', width=2.0), name="IMU 1 Pitch")  ##pitch EMG

        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        # Y_IMU_range = [-180, 180]
        p5 = win.addPlot(title="Device 2 IMU 3 Raw Data")
        p5.setLabel('left', text='mV', color='#000000')
        p5.showGrid(x=False, y=False)
        p5.setLogMode(x=False, y=False)
        p5.setLabel('bottom', text='points', color='#000000', units='s')
        p5.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        p5.addLegend()
        curve5 = p5.plot(pen=pg.mkPen(color='r', width=2.0), name="IMU 1 Roll")  ##pitch EMG

        return p4, p5

    def threadDevice1Start(self):
        Device1Thread = threading.Thread(target=self.start_Device1plot, name='dataDevice1Thread')
        Device1Thread.start()

    def threadDevice2Start(self):
        Device2Thread = threading.Thread(target=self.start_Device2plot, name='dataDevice2Thread')
        Device2Thread.start()

    def start_Device1plot(self):
        self.portNameDevice1 = self.ui.comboBox_Device1CP.currentText()
        def update(sample):
            """
            Load V_ADC raw data
            """
            EMG1, EMG2, IMU1 = [], [], []
            for i in range(sample):
                value = str(self.serDevice1.readline().decode("utf-8", errors="ignore"))
                # value = str(self.serDevice1.readline(), 'utf-8')
                # print("buffer: ", ser.in_waiting)
                # print(value)
                if len(value) == 6:  # data + \n
                    if value[0] == '1':
                        data = int(value[1:5])-1500
                        EMG1.append(int(data))
                    elif value[0] == '2':
                        data = int(value[1:5]) - 1500
                        EMG2.append(int(data))
                    elif value[0] == '3':
                        data = int(value[1:5])
                        IMU1.append(int(data))
            return EMG1, EMG2, IMU1

        while self.portNameDevice1 is not None:
            self.ui.pushButton_StartDevice1Plot.setEnabled(False)
            dataDevice1 = self.serDevice1.readline().decode("utf-8", errors="ignore")
            # load signal
            # self.update_orva(update)

            if len(dataDevice1) == 6: #data + \n
                # print(dataDevice1)
                self.Index = self.Index + 1
                if dataDevice1[0] == '1':
                    self.Device1EMG1[:-1] = self.Device1EMG1[1:]
                    self.Device1EMG1[-1] = int(dataDevice1[1:5])-1500

                if dataDevice1[0] == '2':
                    self.Device1EMG2[:-1] = self.Device1EMG2[1:]
                    self.Device1EMG2[-1] = int(dataDevice1[1:5]) - 1500

                if dataDevice1[0] == '3':
                    self.Device1IMUPitch[:-1] = self.Device1IMUPitch[1:]
                    self.Device1IMUPitch[-1] = int(dataDevice1[1:5])
                    print(dataDevice1)
                    self.DeviceAnle[:-1] = self.DeviceAnle[1:]
                    # single mode
                    self.DeviceAnle[-1] = int(180 - self.DefaultAngle - int(dataDevice1[2:5]))
                    # self.DeviceAnle[-1] = int(180 - self.DefaultAngle - abs(self.Device2IMUPitch[-1]))
                    # dual mode
                    # self.DeviceAnle[-1] = int(int(dataStr[1:5]) - self.Device2IMUPitch[-1])
                    # Emitting this signal ensures update_graph() will run in the main thread since the signal was connected in the __init__ function (main thread)
                    # QtCore.QCoreApplication.processEvents()
                if (self.Index % 500 == 0):
                    self.signalComm.request_Device1graph_update.emit()

            # print(" successful pause")

    def update_orva(self, update):
        EMG1, EMG2, IMU1 = update(150)
        for i in range(len(EMG1)):
            # Raw data
            self.Device1EMG1[:-1] = self.Device1EMG1[1:]
            self.Device1EMG1[-1] = EMG1[i]
        #
        for i in range(len(EMG2)):
            #     Raw data
            self.Device1EMG2[:-1] = self.Device1EMG2[1:]
            self.Device1EMG2[-1] = EMG2[i]
        for i in range(len(IMU1)):
            # Raw data
            self.Device1IMUPitch[:-1] = self.Device1IMUPitch[1:]
            self.Device1IMUPitch[-1] = IMU1[i]
        self.signalComm.request_Device1graph_update.emit()

    def start_Device2plot(self):
        self.portNameDevice2 = self.ui.comboBox_Device2CP.currentText()

        while self.portNameDevice2 is not None:
            self.ui.pushButton_StartDevice2Plot.setEnabled(False)
            dataDevice2 = self.serDevice2.readline().decode("utf-8", errors="ignore").splitlines()
            # print(dataDevice2)
            if len(dataDevice2) != 0:
                if len(dataDevice2[0]) == 5:
                    dataStr = dataDevice2[0]
                    dataStr = str(dataStr)
                    # print(dataStr)
                    if dataStr[0] == '5':
                        self.Device2IMUPitch[:-1] = self.Device2IMUPitch[1:]
                        #Data
                        # self.Device2IMUPitch[-1] = abs(int(dataStr[1:5]))

                        # single mode
                        self.Device2IMUPitch[-1] = int(180 - self.DefaultAngle - abs(int(dataStr[1:5])))
                        # print(abs(self.Device2IMUPitch[-1]))
                    elif dataStr[0] == '6':
                        self.Device2IMURoll[:-1] = self.Device2IMURoll[1:]
                        self.Device2IMURoll[-1] = int(dataStr[1:5])

            # Emitting this signal ensures update_graph() will run in the main thread since the signal was connected in the __init__ function (main thread)
            self.signalComm.request_Device2graph_update.emit()
        # print(" successful pause")



    def stop_Device1plot(self):
        self.portNameDevice1 = None
        self.ui.pushButton_StartDevice1Plot.setEnabled(True)
        self.ui.textEdit_info.setText("Function Not Yet.......")
        print("ploting stop")

    def stop_Device2plot(self):
        self.portNameDevice2 = None
        self.ui.pushButton_StartDevice2Plot.setEnabled(True)
        self.ui.textEdit_info.setText("Function Not Yet.......")
        print("ploting stop")

    def update_Device1graph(self):
        global curve1, curve2, curve3, curve_roll, curve_angle
        # print('Thread ={} Function = update_graph()'.format(threading.currentThread().getName()))
        curve1.setData(self.Device1EMG1)
        curve2.setData(self.Device1EMG2)
        curve3.setData(self.Device1IMUPitch)
        # curve_roll.setData(self.Device1IMURoll)
        curve_angle.setData(self.DeviceAnle)

    def update_Device2graph(self):
        global curve4, curve5
        # print('Thread ={} Function = update_graph()'.format(threading.currentThread().getName()))
        curve4.setData(self.Device2IMUPitch)
        curve5.setData(self.Device2IMUPitch)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;csv Files (*.csv)", options=options)
        if fileName:
            # print(fileName)
            return fileName

    def loadDevice1(self):
        global filenameDevice1, startPointArray1, startPointArray2, rms1, rms2
        filenameDevice1 = self.openFileNameDialog()
        print("EMG Filename" + filenameDevice1)
        dataArray = pd.read_csv(filenameDevice1, skiprows=3, usecols=[0,1,2,3])
        data1 = dataArray.iloc[:, 0]
        data2 = dataArray.iloc[:, 1]
        data3 = dataArray.iloc[:, 2]
        # beforeMedianFrequency = plotTimeFrequencyDomain(data)
        # create an axis
        rms1 = RMSDetect.rms_function(data1, 10)
        rms2 = RMSDetect.rms_function(data2, 10)
        startPointArray1 = RMSDetect.startPoint(rms1, 600, 400) #gravity EMG
        # print(rms1)
        # print(startPointArray1)
        startPointArray2 = RMSDetect.startPoint(rms2, 600, 400)
        self.figure1.clear()
        ax = self.figure1.add_subplot()

        # plot data
        ax.plot(data1)
        self.canvas1.draw()

        self.figure2.clear()
        ax = self.figure2.add_subplot()

        # plot data
        ax.plot(data2)
        self.canvas2.draw()

        self.figure3.clear()
        ax = self.figure3.add_subplot()

        # plot data
        ax.plot(data3)
        self.canvas3.draw()
        maxAngle = numpy.max(data3)
        self.ui.label_angle.setText("Current Angle : " + str(maxAngle))

    def loadDevice2(self):
        filename = self.openFileNameDialog()
        print("IMU Filename" + filename)
        dataArray = pd.read_csv(filename, skiprows=0)
        data = dataArray.iloc[:, 0]
        # create an axis
        ax = self.figure3.add_subplot(111)
        # plot data
        ax.plot(data)
        self.canvas3.draw()
        maxAngle  = numpy.max(data)
        self.ui.label_angle.setText("Current Angle : " + str(maxAngle))
        # print("Max Angle" + str(maxAngle))

    def EMGDevice1Click(self):
        global filenameDevice1, rms1, startPointArray1
        if filenameDevice1 is not None:
            #RMS Detect Function start
            if self.ui.checkBox_EMGDevice1.isChecked():
                dataArray = pd.read_csv(filenameDevice1, skiprows=3, usecols=[0, 1, 2, 3])
                data = dataArray.iloc[:, 0]
                self.figure1.clear()
                ax = self.figure1.add_subplot()
                ax.plot(data)
                # ax.plot(rms1)
                for i in range(len(startPointArray1)):
                    if i%2 == 1:
                        ax.plot(startPointArray1[i], rms1[i], marker="o", color="r")
                    else:
                        ax.plot(startPointArray1[i], rms1[i], marker="o", color="k")
                self.canvas1.draw()

            else:
                dataArray = pd.read_csv(filenameDevice1, skiprows=3, usecols=[0, 1, 2, 3])
                data = dataArray.iloc[:, 0]
                self.figure1.clear()
                ax = self.figure1.add_subplot()
                ax.plot(data)
                self.canvas1.draw()

    def EMGDevice2Click(self):
        global filenameDevice1, rms2, startPointArray2
        if filenameDevice1 is not None:
            # RMS Detect Function start
            if self.ui.checkBox_EMGDevice2.isChecked():
                dataArray = pd.read_csv(filenameDevice1, skiprows=3, usecols=[0, 1, 2, 3])
                data = dataArray.iloc[:, 1]
                self.figure2.clear()
                ax = self.figure2.add_subplot()
                ax.plot(data)
                ax.plot(rms2)
                print(startPointArray1)
                for i in range(len(startPointArray2)):
                    if i % 2 == 1:
                        ax.plot(startPointArray2[i], rms1[i], marker="o", color="r")
                    else:
                        ax.plot(startPointArray2[i], rms1[i], marker="o", color="k")
                self.canvas2.draw()

            else:
                dataArray = pd.read_csv(filenameDevice1, skiprows=3, usecols=[0, 1, 2, 3])
                data = dataArray.iloc[:, 1]
                self.figure2.clear()
                ax = self.figure2.add_subplot()
                ax.plot(data)
                self.canvas2.draw()

    def Device1SaveData(self):
        with open(self.storagePathDevice1, "w", newline="\n") as csvfile:
            wr = csv.writer(csvfile)
            print("Save Device1 Data to .CSV")
            for word in range(1, len(self.Device1EMG1)):
                if word == 1:
                    wr.writerow(["EMG Channel 1 ", "EMG Channel 2", "IMU 1 Pitch", "IMU 1 Roll"])
                wr.writerow([self.Device1EMG1[word], self.Device1EMG2[word], self.Device1IMUPitch[word], self.Device1IMURoll[word]])

    def Device2SaveData(self):
        with open(self.storagePathDevice2, "w", newline="\n") as csvfile:
            wr = csv.writer(csvfile)
            print("Save Device2 Data to .CSV")
            for word in range(1, len(self.Device2IMUPitch)):
                if word == 1:
                    wr.writerow(["IMU Pitch ", "IMU Roll"])
                # wr.writerow([self.Device1IMURoll[word], self.Device2IMUPitch[word], self.Device1IMURoll[word]])
                wr.writerow([self.Device2IMUPitch[word], self.Device2IMURoll[word]])




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.instance().exec_())