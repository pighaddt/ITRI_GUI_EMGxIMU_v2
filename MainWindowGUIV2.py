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
        # self.index1 = 0
        # self.index2 = 0

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
        self.windowWidth_Device1 = 500
        self.windowWidth_Device2 = 100
        #Device1 2EMG signal + 1 IMU Signal
        self.Device1EMG1 = linspace(0, 0, self.windowWidth_Device1)
        self.Device1EMG2= linspace(0, 0, self.windowWidth_Device1)
        self.Device1IMU1 = linspace(0, 0, self.windowWidth_Device1)  # create array that will contain the relevant time series
        #Device2  1 IMU Signal
        self.Device2IMU2 = linspace(0, 0, self.windowWidth_Device2)  # create array that will contain the relevant time series
        self.Device2IMU3 = linspace(0, 0, self.windowWidth_Device2)  # create array that will contain the relevant time series


    def initSet(self):
        for i in range(len(self.bpsArray)):
            self.ui.comboBox_Device1BR.addItem(self.bpsArray[i])
            self.ui.comboBox_Device2BR.addItem(self.bpsArray[i])
        self.ui.comboBox_Device1BR.setCurrentIndex(3) #Device1 init buad rate 115200
        self.ui.comboBox_Device2BR.setCurrentIndex(3) #Device2 init buad rate 115200

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
        self.ui.textEdit_info.append(" Device 1 Connecting to {}...".format(str(self.comPortDevice1)))

    def connectDevice2SP(self):
        self.comPortDevice2 = self.ui.comboBox_Device2CP.currentText()
        self.baudRateDevice2 = self.ui.comboBox_Device2BR.currentText()
        self.serDevice2 = serial.Serial(self.comPortDevice2, int(self.baudRateDevice2), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
        self.ui.textEdit_info.append("Device 2 Connecting to {}...".format(str(self.comPortDevice2)))


    def set_graph2_ui(self):
        global curve1, curve2, curve3
        Y_EMG_range = [-3000, 3000]
        Y_IMU_range = [-180, 180]

        pg.setConfigOptions(antialias=True)  # pg global variable setting function, antialias=True open curve anti-aliasing
        win = pg.GraphicsLayoutWidget()  # Create pg layout for automatic management of data interface layout
        win.setBackground('w')
        # pg The drawing window can be added to the graph_layout in the GUI as a widget, and of course can be added to all other Qt containers.
        # self.verticalLayoutWidget.addWidget(win)
        self.ui.verticalLayout.addWidget(win)
        p1 = win.addPlot(title="Device1 EMG 1 Raw Data")  # Add the first drawing window
        p1.setLabel('left', text='mV', color='#000000')  # y axis setting function
        p1.showGrid(x=False, y=False)  # Grid setting function
        p1.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        p1.setLabel('bottom', text='points', color='#000000', units='s')  # x axis setting function
        p1.setYRange(min=int(Y_EMG_range[0]), max=int(Y_EMG_range[1]))
        p1.addLegend() # Select whether to add legend

        curve1 = p1.plot(pen=pg.mkPen(color='k', width=2.0), name="EMG 1 Raw Data")  ##pitch EMG


        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p2 = win.addPlot(title="Device1 EMG 2 Raw Data")
        p2.setLabel('left', text='mV', color='#000000')
        p2.showGrid(x=False, y=False)
        p2.setLogMode(x=False, y=False)
        p2.setLabel('bottom', text='points',color='#000000' ,  units='s')
        p2.setYRange(min=int(Y_EMG_range[0]), max=int(Y_EMG_range[1]))
        p2.addLegend()
        curve2 = p2.plot(pen=pg.mkPen(color='r', width=2.0), name="EMG 2 Raw Data")  ##pitch EMG


        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p3 = win.addPlot(title="Device1 IMU 1 Raw Data")
        p3.setLabel('left', text='angle', color='#000000')
        p3.showGrid(x=False, y=False)
        p3.setLogMode(x=False, y=False)
        p3.setLabel('bottom', text='points', color='#000000', units='s')
        p3.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        p3.addLegend()
        curve3 = p3.plot(pen=pg.mkPen(color='b', width=2.0), name="IMU 1 Pitch")  ##pitch EMG

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
        p4 = win.addPlot(title="Device2 IMU 2 Raw Data")  # Add the first drawing window
        p4.setLabel('left', text='mV', color='#000000')  # y axis setting function
        p4.showGrid(x=False, y=False)  # Grid setting function
        p4.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        p4.setLabel('bottom', text='points', color='#000000', units='s')  # x axis setting function
        p4.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        # p5.setXRange(0, 1000) # bigger than 1000 will use k units
        p4.addLegend()  # Select whether to add legend

        curve4 = p4.plot(pen=pg.mkPen(color='k', width=2.0), name="IMU 1 Roll")  ##pitch EMG

        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        # Y_IMU_range = [-180, 180]
        p5 = win.addPlot(title="EMG Raw Data")
        p5.setLabel('left', text='mV', color='#000000')
        p5.showGrid(x=False, y=False)
        p5.setLogMode(x=False, y=False)
        p5.setLabel('bottom', text='points', color='#000000', units='s')
        p5.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        p5.addLegend()
        curve5 = p5.plot(pen=pg.mkPen(color='r', width=2.0), name="IMU 1 Yaw")  ##pitch EMG

        return p4, p5

    def threadDevice1Start(self):
        Device1Thread = threading.Thread(target=self.start_Device1plot, name='dataDevice1Thread')
        Device1Thread.start()

    def threadDevice2Start(self):
        Device2Thread = threading.Thread(target=self.start_Device2plot, name='dataDevice2Thread')
        Device2Thread.start()

    def start_Device1plot(self):
        self.portNameDevice1 = self.ui.comboBox_Device1CP.currentText()

        while self.portNameDevice1 is not None:
            self.ui.pushButton_StartDevice1Plot.setEnabled(False)
            dataDevice1 = self.serDevice1.readline().decode("utf-8", errors="ignore").splitlines()
            print(dataDevice1)
            if len(dataDevice1[0]) == 5:
                dataDevice1[0] = int(dataDevice1[0])
                # print(dataEMG[0])
                if int(dataDevice1[0] / 10000) == 1:
                    # self.index1 = self.index1 + 1
                    self.Device1EMG1[:-1] = self.Device1EMG1[1:]
                    # dataEMG[0] = (dataEMG[0] % 10000) - 1500
                    dataDevice1[0] = (dataDevice1[0] % 10000)  #gravity version
                    # print(dataEMG[0])
                    self.Device1EMG1[-1] = dataDevice1[0]             # vector containing the instantaneous values
                    # if self.index1 % 20 == 0:
                    # curve5.setData(self.EMGData1)  # set the curve with these data
                    # QApplication.processEvents()  # process the plot now
                    # self.index1 = 0
                elif int(dataDevice1[0] / 10000) == 2:
                    # self.index2 = self.index2 + 1
                    self.Device1EMG2[:-1] = self.Device1EMG2[1:]
                    # dataEMG[0] = (dataEMG[0] % 10000) - 1500
                    dataDevice1[0] = (dataDevice1[0] % 10000)
                    # print(dataEMG[0])
                    self.Device1EMG2[-1] = dataDevice1[0]  # vector containing the instantaneous values

            # Emitting this signal ensures update_graph() will run in the main thread since the signal was connected in the __init__ function (main thread)
            self.signalComm.request_Device1graph_update.emit()
        print(" successful pause")


    def start_Device2plot(self):
        self.portNameDevice2 = self.ui.comboBox_Device2CP.currentText()

        while self.portNameDevice2 is not None:
            self.ui.pushButton_StartDevice2Plot.setEnabled(False)
            dataDevice2 = self.serDevice2.readline().decode("utf-8", errors="ignore")
            print(len(dataDevice2))
            # print(dataIMU[4:5])
            if dataDevice2[4:5] == 'P':  # verify String Data
                dataDevice2 = str(dataDevice2)
                dataDevice2 = dataDevice2[4:-2]
                # print("dataIMU" + dataIMU)
                splitData = dataDevice2.split(',')
                # print(splitData)
                pitchStr = splitData[0]
                rollStr = splitData[1]
                yawStr = splitData[2]
                self.Device1IMU1[:-1] = self.Device1IMU1[1:]  # shift pitch data in the temporal mean 1 sample left
                self.Device2IMU2[:-1] = self.Device2IMU2[1:]  # shift roll data in the temporal mean 1 sample left
                self.Device2IMU3[:-1] = self.Device2IMU3[1:]  # shift roll data in the temporal mean 1 sample left

                self.Device1IMU1[-1] = float(pitchStr[2:])  # pitchStr : R= pitch
                self.Device2IMU2[-1] = float(rollStr[2:])  # vector containing the instantaneous values
                self.Device2IMU3[-1] = float(yawStr[2:])  # vector containing the instantaneous values
                # print(splitData)

            # Emitting this signal ensures update_graph() will run in the main thread since the signal was connected in the __init__ function (main thread)
            self.signalComm.request_Device2graph_update.emit()
        print(" successful pause")



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
        global curve1, curve2, curve3
        # print('Thread ={} Function = update_graph()'.format(threading.currentThread().getName()))
        curve1.setData(self.Device1EMG1)
        curve2.setData(self.Device1EMG2)
        curve3.setData(self.Device1IMU1)

    def update_Device2graph(self):
        global curve4, curve5
        # print('Thread ={} Function = update_graph()'.format(threading.currentThread().getName()))
        curve4.setData(self.Device2IMU2)
        curve5.setData(self.Device2IMU3)

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
        dataArray = pd.read_csv(filenameDevice1, skiprows=3, usecols=[3, 4])
        data1 = dataArray.iloc[:, 0]
        data2 = dataArray.iloc[:, 1]
        # beforeMedianFrequency = plotTimeFrequencyDomain(data)
        # create an axis
        rms1 = RMSDetect.rms_function(data1, 10)
        rms2 = RMSDetect.rms_function(data2, 10)
        startPointArray1 = RMSDetect.startPoint(rms1, 300, 50)
        startPointArray2 = RMSDetect.startPoint(rms2, 300, 50)
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
                dataArray = pd.read_csv(filenameDevice1, skiprows=3, usecols=[3])
                data = dataArray.iloc[:, 0]
                self.figure1.clear()
                ax = self.figure1.add_subplot()
                ax.plot(data)
                ax.plot(rms1)
                for i in range(len(startPointArray1)):
                    if i%2 == 1:
                        ax.plot(startPointArray1[i], rms1[i], marker="o", color="r")
                    else:
                        ax.plot(startPointArray1[i], rms1[i], marker="o", color="k")
                self.canvas1.draw()

            else:
                dataArray = pd.read_csv(filenameDevice1, skiprows=3, usecols=[3])
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
                dataArray = pd.read_csv(filenameDevice1, skiprows=3, usecols=[4])
                data = dataArray.iloc[:, 0]
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
                dataArray = pd.read_csv(filenameDevice1, skiprows=3, usecols=[4])
                data = dataArray.iloc[:, 0]
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
                    wr.writerow(["EMG Channel 1 ", "EMG Channel 2"])
                wr.writerow([self.Device1EMG1[word], self.Device1EMG2[word]])

    def Device2SaveData(self):
        with open(self.storagePathDevice2, "w", newline="\n") as csvfile:
            wr = csv.writer(csvfile)
            print("Save Device2 Data to .CSV")
            for word in range(1, len(self.Device2IMU2)):
                if word == 1:
                    wr.writerow(["IMU Pitch ", "IMU Roll", "IMU Yaw"])
                # wr.writerow([self.Device2IMU2[word], self.Device2IMU3[word], self.Device2IMU2[word]])
                wr.writerow([self.Device2IMU2[word], self.Device2IMU3[word]])




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.instance().exec_())