import csv
import os
import threading

import PyQt5
import numpy
import serial
from PyQt5 import QtWidgets, QtGui, QtCore
import sys

from PyQt5.QtWidgets import QApplication, QFileDialog
from numpy import linspace

import RMSDetect
from GUI.GUI import serialDemo
from GUI_EMG_IMU import Ui_MainWindow
import pyqtgraph as pg
import numpy as np

import matplotlib

from datetime import date
from datetime import datetime

from plotTimeFrequencyDomain import plotTimeFrequencyDomain

matplotlib.use("Qt5Agg")  # 声明使用QT5
import pandas as pd

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random



class SignalCommunicate(PyQt5.QtCore.QObject):
    request_IMUgraph_update = PyQt5.QtCore.pyqtSignal()
    request_EMGgraph_update = PyQt5.QtCore.pyqtSignal()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__() #inherit Mainwindow super function
        self.ui = Ui_MainWindow() # your mainwindow from pyuic5
        self.ui.setupUi(self) # your init setupUI function
        # self.p1, self.p2, self.p3, self.p4 = self.set_graph2_ui()  # set the drawing window
        self.p2, self.p3, self.p4 = self.set_graph2_ui()  # set the drawing window
        self.p5, self.p6 = self.set_graph3_ui()  # set the drawing window
        # self.ui.pushButton_StartPlot.clicked.connect(self.threadStart)
        self.ui.pushButton_EMG.clicked.connect(self.connectEMGSP)
        self.ui.pushButton_IMU.clicked.connect(self.connectIMUSP)
        self.ui.pushButton_StartIMUPlot.clicked.connect(self.threadIMUStart)
        self.ui.pushButton_CloseIMUPlot.clicked.connect(self.stop_IMUplot)
        self.ui.pushButton_StartEMGPlot.clicked.connect(self.threadEMGStart)
        self.ui.pushButton_CloseEMGPlot.clicked.connect(self.stop_EMGplot)
        self.ui.pushButton_searchSP.clicked.connect(self.searchComPort)
        self.ui.pushButton_LoadEMG.clicked.connect(self.loadEMG)
        self.ui.pushButton_LoadIMU.clicked.connect(self.loadIMU)
        self.ui.checkBox_EMGDevice1.clicked.connect(self.EMGDevice1Click)
        self.ui.checkBox_EMGDevice2.clicked.connect(self.EMGDevice2Click)
        self.ui.pushButton_SaveIMUData.clicked.connect(self.IMUSaveData)
        self.ui.pushButton_SaveEMGData.clicked.connect(self.EMGSaveData)
        # self.comPortSetting()
        self.EMGIMUDataSetting()
        self.bpsArray = ['4800', '9600', '115200']
        self.initSet()
        # self.index1 = 0
        # self.index2 = 0

        # Signals that can be emitted
        self.signalComm = SignalCommunicate()
        # Update graph whenever the 'request_graph_update' signal is emitted
        self.signalComm.request_IMUgraph_update.connect(self.update_IMUgraph)
        self.signalComm.request_EMGgraph_update.connect(self.update_EMGgraph)

        # a figure instance to plot on
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
        self.storagePathIMU = f"{desktop}\\{d1}{current_time}IMU.csv"
        self.storagePathEMG = f"{desktop}\\{d1}{current_time}EMG.csv"

        matplotlib.rcParams.update({'font.size': 8})

    def EMGIMUDataSetting(self):
        self.windowWidth_EMG = 500
        self.windowWidth_IMU = 100
        self.IMU1Data = linspace(0, 0, self.windowWidth_IMU)  # create array that will contain the relevant time series
        self.IMU2Data = linspace(0, 0, self.windowWidth_IMU)  # create array that will contain the relevant time series
        self.IMU3Data = linspace(0, 0, self.windowWidth_IMU)  # create array that will contain the relevant time series
        self.EMGData1 = linspace(0, 0, self.windowWidth_EMG)
        self.EMGData2 = linspace(0, 0, self.windowWidth_EMG)

    def initSet(self):
        for i in range(len(self.bpsArray)):
            self.ui.comboBox_Device1BR.addItem(self.bpsArray[i])
            self.ui.comboBox_Device2BR.addItem(self.bpsArray[i])
        self.ui.comboBox_Device1BR.setCurrentIndex(2)
        self.ui.comboBox_Device2BR.setCurrentIndex(1)

    def searchComPort(self):
        self.ui.textEdit_info.setReadOnly(True)
        self.ui.textEdit_info.setText("Searching BT Device...")
        self.comPorResult = serialDemo.serial_ports()
        for i in range(len(self.comPorResult)):
            self.ui.textEdit_info.append(self.comPorResult[i])
            self.ui.comboBox_Device1CP.addItem(self.comPorResult[i])
            self.ui.comboBox_Device2CP.addItem(self.comPorResult[i])

    def reset(self):
        global curve2, curve3, curve4, curve5, curve6
        self.ui.comboBox_Device1CP.clear()
        self.ui.comboBox_Device2CP.clear()
        self.ui.label_BTConnected_Item.clear()
        self.comPortEMGName = None
        self.comPortIMUName = None
        curve2.clear()
        curve3.clear()
        curve4.clear()
        curve5.clear()
        curve6.clear()

    def connectEMGSP(self):
        self.comPortEMG = self.ui.comboBox_Device1CP.currentText()
        self.baudRateEMG = self.ui.comboBox_Device1BR.currentText()
        self.serEMG = serial.Serial(self.comPortEMG, int(self.baudRateEMG), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
        self.ui.textEdit_info.append("EMG Device Connecting to {}...".format(str(self.comPortEMG)))

    def connectIMUSP(self):
        self.comPortIMU = self.ui.comboBox_Device2CP.currentText()
        self.baudRateIMU = self.ui.comboBox_Device2BR.currentText()
        print(self.comPortIMU + self.baudRateIMU)
        self.serIMU = serial.Serial(self.comPortIMU, int(self.baudRateIMU), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
        self.ui.textEdit_info.append("IMU Device Connecting to {}...".format(str(self.comPortIMU)))


    def set_graph2_ui(self):
        global curve1, curve2, curve3, curve4, p2
        Y_EMG_range = [-3000, 3000]
        pg.setConfigOptions(antialias=True)  # pg global variable setting function, antialias=True open curve anti-aliasing
        win = pg.GraphicsLayoutWidget()  # Create pg layout for automatic management of data interface layout
        win.setBackground('w')
        # pg The drawing window can be added to the graph_layout in the GUI as a widget, and of course can be added to all other Qt containers.
        # self.verticalLayoutWidget.addWidget(win)
        self.ui.verticalLayout.addWidget(win)
        # p1 = win.addPlot(title="EMG Raw Data")  # Add the first drawing window
        # p1.setLabel('left', text='mV', color='#000000')  # y axis setting function
        # p1.showGrid(x=False, y=False)  # Grid setting function
        # p1.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        # p1.setLabel('bottom', text='points', color='#000000', units='s')  # x axis setting function
        # p1.setYRange(min=int(Y_EMG_range[0]), max=int(Y_EMG_range[1]))
        # p1.addLegend() # Select whether to add legend
        #
        # curve1 = p1.plot(pen=pg.mkPen(color='k', width=2.0), name="EMG Raw Data")  ##pitch EMG


        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        Y_IMU_range = [-180, 180]
        p2 = win.addPlot(title="IMU Pitch Data")
        p2.setLabel('left', text='angle', color='#000000')
        p2.showGrid(x=False, y=False)
        p2.setLogMode(x=False, y=False)
        p2.setLabel('bottom', text='points',color='#000000' ,  units='s')
        p2.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        p2.addLegend()
        curve2 = p2.plot(pen=pg.mkPen(color='r', width=2.0), name="IMU 1 Pitch")  ##pitch EMG


        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p3 = win.addPlot(title="IMU ROll Data")
        p3.setLabel('left', text='angle', color='#000000')
        p3.showGrid(x=False, y=False)
        p3.setLogMode(x=False, y=False)
        p3.setLabel('bottom', text='points', color='#000000', units='s')
        p3.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        p3.addLegend()
        curve3 = p3.plot(pen=pg.mkPen(color='b', width=2.0), name="IMU 1 Roll")  ##pitch EMG


        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p4 = win.addPlot(title="IMU Yaw Data")
        p4.setLabel('left', text='angle', color='#000000')
        p4.showGrid(x=False, y=False)
        p4.setLogMode(x=False, y=False)
        p4.setLabel('bottom', text='points', color='#000000', units='s')
        p4.setYRange(min=int(Y_IMU_range[0]), max=int(Y_IMU_range[1]))
        p4.addLegend()
        curve4 = p4.plot(pen=pg.mkPen(color='k', width=2.0), name="IMU 1 Yaw")  ##pitch EMG

        # return p1, p2, p3, p4
        return p2, p3, p4
    def set_graph3_ui(self):
        global curve5, curve6
        Y_EMG_range = [-3000, 3000]
        pg.setConfigOptions(
            antialias=True)  # pg global variable setting function, antialias=True open curve anti-aliasing
        win = pg.GraphicsLayoutWidget()  # Create pg layout for automatic management of data interface layout
        win.setBackground('w')
        # pg The drawing window can be added to the graph_layout in the GUI as a widget, and of course can be added to all other Qt containers.
        # self.verticalLayoutWidget.addWidget(win)
        self.ui.verticalLayout_2.addWidget(win)
        p5 = win.addPlot(title="EMG Raw Data")  # Add the first drawing window
        p5.setLabel('left', text='mV', color='#000000')  # y axis setting function
        p5.showGrid(x=False, y=False)  # Grid setting function
        p5.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        p5.setLabel('bottom', text='points', color='#000000', units='s')  # x axis setting function
        p5.setYRange(min=int(Y_EMG_range[0]), max=int(Y_EMG_range[1]))
        # p5.setXRange(0, 1000) # bigger than 1000 will use k units
        p5.addLegend()  # Select whether to add legend

        curve5 = p5.plot(pen=pg.mkPen(color='k', width=2.0), name="EMG Raw Data Channel 1")  ##pitch EMG

        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        # Y_IMU_range = [-180, 180]
        p6 = win.addPlot(title="EMG Raw Data")
        p6.setLabel('left', text='mV', color='#000000')
        p6.showGrid(x=False, y=False)
        p6.setLogMode(x=False, y=False)
        p6.setLabel('bottom', text='points', color='#000000', units='s')
        p6.setYRange(min=int(Y_EMG_range[0]), max=int(Y_EMG_range[1]))
        p6.addLegend()
        curve6 = p6.plot(pen=pg.mkPen(color='r', width=2.0), name="EMG Raw Data Channel 2")  ##pitch EMG

        return p5, p6

    def threadEMGStart(self):
        dataEMGThread = threading.Thread(target=self.start_EMGplot, name='dataEMGThread')
        dataEMGThread.start()

    def threadIMUStart(self):
        dataIMUThread = threading.Thread(target=self.start_IMUplot, name='dataIMUThread')
        dataIMUThread.start()

    def start_EMGplot(self):
        self.portNameEMG = self.ui.comboBox_Device1CP.currentText()

        while self.portNameEMG is not None:
            self.ui.pushButton_StartEMGPlot.setEnabled(False)
            dataEMG = self.serEMG.readline().decode("utf-8", errors="ignore").splitlines()
            print(dataEMG)
            if len(dataEMG[0]) == 5:
                dataEMG[0] = int(dataEMG[0])
                # print(dataEMG[0])
                # print(threading.currentThread().getName())
                if int(dataEMG[0] / 10000) == 1:
                    # self.index1 = self.index1 + 1
                    self.EMGData1[:-1] = self.EMGData1[1:]
                    # dataEMG[0] = (dataEMG[0] % 10000) - 1500
                    dataEMG[0] = (dataEMG[0] % 10000)  #gravity version
                    # print(dataEMG[0])
                    self.EMGData1[-1] = dataEMG[0]             # vector containing the instantaneous values
                    # if self.index1 % 20 == 0:
                    # curve5.setData(self.EMGData1)  # set the curve with these data
                    # QApplication.processEvents()  # process the plot now
                    # self.index1 = 0
                elif int(dataEMG[0] / 10000) == 2:
                    # self.index2 = self.index2 + 1
                    self.EMGData2[:-1] = self.EMGData2[1:]
                    # dataEMG[0] = (dataEMG[0] % 10000) - 1500
                    dataEMG[0] = (dataEMG[0] % 10000)
                    # print(dataEMG[0])
                    self.EMGData2[-1] = dataEMG[0]  # vector containing the instantaneous values

            # Emitting this signal ensures update_graph() will run in the main thread since the signal was connected in the __init__ function (main thread)
            self.signalComm.request_EMGgraph_update.emit()



        print(" successful pause")


    def start_IMUplot(self):
        self.portNameIMU = self.ui.comboBox_Device2CP.currentText()

        while self.portNameIMU is not None:
            self.ui.pushButton_StartIMUPlot.setEnabled(False)
            dataIMU = self.serIMU.readline().decode("utf-8", errors="ignore")
            print(len(dataIMU))
            # print(dataIMU[4:5])
            if dataIMU[4:5] == 'P':  # verify String Data
                dataIMU = str(dataIMU)
                dataIMU = dataIMU[4:-2]
                # print("dataIMU" + dataIMU)
                splitData = dataIMU.split(',')
                # print(splitData)
                pitchStr = splitData[0]
                rollStr = splitData[1]
                yawStr = splitData[2]
                self.IMU1Data[:-1] = self.IMU1Data[1:]  # shift pitch data in the temporal mean 1 sample left
                self.IMU2Data[:-1] = self.IMU2Data[1:]  # shift roll data in the temporal mean 1 sample left
                self.IMU3Data[:-1] = self.IMU3Data[1:]  # shift roll data in the temporal mean 1 sample left

                self.IMU1Data[-1] = float(pitchStr[2:])  # pitchStr : R= pitch
                self.IMU2Data[-1] = float(rollStr[2:])  # vector containing the instantaneous values
                self.IMU3Data[-1] = float(yawStr[2:])  # vector containing the instantaneous values
                # print(splitData)

            # Emitting this signal ensures update_graph() will run in the main thread since the signal was connected in the __init__ function (main thread)
            self.signalComm.request_IMUgraph_update.emit()



        print(" successful pause")



    def stop_EMGplot(self):
        self.portNameEMG = None
        self.ui.pushButton_StartEMGPlot.setEnabled(True)
        # self.portNameIMU = None
        self.ui.textEdit_info.setText("Function Not Yet.......")
        print("ploting stop")

    def stop_IMUplot(self):
        self.portNameIMU = None
        self.ui.pushButton_StartIMUPlot.setEnabled(True)
        self.ui.textEdit_info.setText("Function Not Yet.......")
        print("ploting stop")

    def update_EMGgraph(self):
        global curve5, curve6
        # print('Thread ={} Function = update_graph()'.format(threading.currentThread().getName()))
        curve5.setData(self.EMGData1)
        curve6.setData(self.EMGData2)

    def update_IMUgraph(self):
        global curve2, curve3, curve4
        # print('Thread ={} Function = update_graph()'.format(threading.currentThread().getName()))
        curve2.setData(self.IMU1Data)
        curve3.setData(self.IMU2Data)
        curve4.setData(self.IMU3Data)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;csv Files (*.csv)", options=options)
        if fileName:
            # print(fileName)
            return fileName

    def loadEMG(self):
        global filenameEMG, rms1, startPointArray1, startPointArray2, rms2
        filenameEMG = self.openFileNameDialog()
        print("EMG Filename" + filenameEMG)
        dataArray = pd.read_csv(filenameEMG, skiprows=3, usecols=[3, 4])
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

    def loadIMU(self):
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
        global filenameEMG, rms1, startPointArray1
        if filenameEMG is not None:
            #RMS Detect Function start
            if self.ui.checkBox_EMGDevice1.isChecked():
                dataArray = pd.read_csv(filenameEMG, skiprows=3, usecols=[3])
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
                dataArray = pd.read_csv(filenameEMG, skiprows=3, usecols=[3])
                data = dataArray.iloc[:, 0]
                self.figure1.clear()
                ax = self.figure1.add_subplot()
                ax.plot(data)
                self.canvas1.draw()

    def EMGDevice2Click(self):
        global filenameEMG, rms2, startPointArray2
        if filenameEMG is not None:
            # RMS Detect Function start
            if self.ui.checkBox_EMGDevice2.isChecked():
                dataArray = pd.read_csv(filenameEMG, skiprows=3, usecols=[4])
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
                dataArray = pd.read_csv(filenameEMG, skiprows=3, usecols=[4])
                data = dataArray.iloc[:, 0]
                self.figure2.clear()
                ax = self.figure2.add_subplot()
                ax.plot(data)
                self.canvas2.draw()
    def IMUSaveData(self):
            # print(saveData)
        with open(self.storagePathIMU, "w", newline="\n") as csvfile:
            wr = csv.writer(csvfile)
            print("Save Data to .CSV")
            # wr.writerow(saveData[1: index])
            for word in range(1, len(self.IMU1Data)):
                if word == 1:
                    wr.writerow(["IMU Pitch ", "IMU Roll", "IMU Yaw"])
                wr.writerow([self.IMU1Data[word], self.IMU2Data[word], self.IMU3Data[word]])

    def EMGSaveData(self):
        with open(self.storagePathEMG, "w", newline="\n") as csvfile:
            wr = csv.writer(csvfile)
            print("Save Data to .CSV")
            # wr.writerow(saveData[1: index])
            for word in range(1, len(self.EMGData1)):
                if word == 1:
                    wr.writerow(["EMG Channel 1 ", "EMG Channel 2"])
                wr.writerow([self.EMGData1[word], self.EMGData2[word]])


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.instance().exec_())