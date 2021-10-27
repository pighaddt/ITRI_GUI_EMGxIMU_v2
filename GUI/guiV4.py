import sys
from PyQt5 import QtWidgets, QtGui, QtCore, QtSerialPort

from gui_v5 import Ui_MainWindow
import serialDemo

from queue import Queue
import pyqtgraph as pg
import numpy as np
from scipy import signal
import threading
import serial
import openpyxl
import time
import math
import xlwt


class SignalCommunicate(QtCore.QObject):
    request_graph_update = QtCore.pyqtSignal()
    request_Cgraph_update = QtCore.pyqtSignal()

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
        self.p1, self.p2 = self.set_graph_ui()
        self.pc = self.set_Cgraph_ui()
        self.ui.pushButton_start.clicked.connect(self.threadStart)
        self.ui.pushButton_stop.clicked.connect(self.stopPlot)

        # Signals that can be emitted
        self.signalComm = SignalCommunicate()
        # Update graph whenever the 'request_graph_update' signal is emitted
        self.signalComm.request_graph_update.connect(self.update_graph)
        self.signalComm.request_Cgraph_update.connect(self.update_Cgraph)

    def pushButton_2_miniWin(self):
        self.showMinimized()
    def pushButton_3_closeWin(self):
        global ser
        ser.close()
        self.close()

    def reset(self):
        global comPortName, ser
        self.ui.textEdit_btResult.clear()
        self.ui.comboBox_selectCom.clear()
        self.ui.label_BTConnected_Item.clear()
        self.ui.label_capaci_val.setText(str(0.0))
        self.ui.label_capaci_val_2.setText(str(0.0))
        self.ui.label_capaci_state.setText("(state)")
        self.ui.label_pressure_val.setText(str(0.0))
        self.ui.label_CH1SNR_val.setText(str(0.0))
        self.ui.label_CH2SNR_val.setText(str(0.0))
        self.ui.lineEdit_Cthreshold_noise.clear()
        self.ui.lineEdit_Cthreshold_dryOrSweaty.clear()
        self.ui.label_capaci_dryVal.setText(str(0.0))
        self.ui.label_capaci_sweatyVal1.setText(str(0.0))
        self.ui.label_capaci_sweatyVal2.setText(str(0.0))
        self.ui.label_capaci_noiseVal.setText(str(0.0))
        comPortName = None
        curve1.clear()
        curve2.clear()
        curve3.clear()
        curveC.clear()
        ser.close()

    def searchComPort(self):
        self.ui.textEdit_btResult.setReadOnly(True)
        self.ui.textEdit_btResult.setText("Searching BT Device...")
        self.comPorResult = serialDemo.serial_ports()
        if len(self.comPorResult) == 0:
            self.ui.textEdit_btResult.append("No BT Devices were found!")
        else:
            for i in range(len(self.comPorResult)):
                self.ui.textEdit_btResult.append(self.comPorResult[i])
                self.ui.comboBox_selectCom.addItem(self.comPorResult[i])

    def connectBT(self):
        global comPortName, ser
        comPortName = self.ui.comboBox_selectCom.currentText()
        self.ui.label_BTConnected_Item.setText(str(comPortName))
        if str(comPortName) == '':
            self.ui.textEdit_btResult.append("There is no BT device can be connected.")
        else:
            self.ui.textEdit_btResult.append("Connecting to {}...".format(str(comPortName)))
            self.portName = self.ui.label_BTConnected_Item.text()
            self.baudRate = 115200
            ser = serial.Serial(self.portName, int(self.baudRate), timeout=1, parity=serial.PARITY_NONE, stopbits=1, xonxoff=True)
            ser.set_buffer_size(rx_size=4096, tx_size=None)
            self.ui.textEdit_btResult.append("Connected to {}!".format(str(comPortName)))

    def set_graph_ui(self):
        """
        settings (set 4 sub-windows) for pyqtgraph window (vertical layout)
        """
        global curve1, curve2, curve3
        pg.setConfigOptions(antialias=True)  # pg global variable setting function, antialias=True open curve anti-aliasing
        win = pg.GraphicsLayoutWidget()  # Create pg layout for automatic management of data interface layout
        win.setBackground('w')
        self.ui.verticalLayout.addWidget(win)

        # plot 1
        p1 = win.addPlot(title="Ch1: Target EMG data")  # Add the first drawing window
        p1.setLabel('left', text='V', color='#000000')  # y axis setting function
        p1.showGrid(x=False, y=False)
        p1.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        # p1.setLabel('bottom', text='Time', color='#000000', units='s')  # x axis setting function
        p1.setYRange(min=0.0, max=3.4)
        # p1.addLegend()
        curve1 = p1.plot(pen=pg.mkPen(color='k', width=2.0), name="Ch1: Target EMG data")

        # plot 2
        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p2 = win.addPlot(title="Ch2: Compensated EMG data")
        p2.setLabel('left', text='V', color='#000000')
        p2.showGrid(x=False, y=False)
        p2.setLogMode(x=False, y=False)
        # p2.setLabel('bottom', text='Time', color='#000000', units='s')
        p2.setYRange(min=-1.7, max=1.7)
        # p2.addLegend()
        curve2 = p2.plot(pen=pg.mkPen(color='k', width=2.0), name="Ch2: Compensated EMG data")
        curve3 = p2.plot(pen=pg.mkPen(color='b', width=2.0), name="Onset and offset")

        return p1, p2

    def set_Cgraph_ui(self):
        """
        settings (set 4 sub-windows) for pyqtgraph window (vertical layout)
        """
        global curveC
        pg.setConfigOptions(antialias=True)  # pg global variable setting function, antialias=True open curve anti-aliasing
        winC = pg.GraphicsLayoutWidget()  # Create pg layout for automatic management of data interface layout
        winC.setBackground('w')
        self.ui.verticalLayout_2.addWidget(winC)

        # plot 1
        pc = winC.addPlot(title="Tau curve to calculate C")  # Add the first drawing window
        pc.setLabel('left', text='V', color='#000000')  # y axis setting function
        pc.showGrid(x=False, y=False)
        pc.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        pc.setYRange(min=0.0, max=3.3)
        curveC = pc.plot(pen=pg.mkPen(color='k', width=2.0), name="Tau curve to calculate C")

        return pc

    def calcuC(self, Value, q):
        """
        The function of calculating capacitance by processing V_ADC raw data.
        """
        # for i in range(len(Value)):
        #     Value[i] = int(str(Value[i]).lstrip("C"))/1000
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
            if filterValue[MaxIndx[p] + tauIndex + 1] - filterValue[MaxIndx[p] + tauIndex] != 0:
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
            if filterValue[MinIndx[p] + tauIndex] - filterValue[MinIndx[p] + tauIndex + 1] != 0:
                t_tau = float((filterValue[MinIndx[p] + tauIndex] - V_tau) / (
                        filterValue[MinIndx[p] + tauIndex] - filterValue[
                    MinIndx[p] + tauIndex + 1])) * self.sampleRate + tauIndex * self.sampleRate
                C_down.append(abs(t_tau) / self.R)
                C_rise.append(abs(t_tau) / self.R)
        dic = {'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'Length of C': len(C_rise),
               'Average capacitance value(F)': np.average(C_rise)}
        # print(dic)
        q.put(dic)
        # print()
        return dic


    def threadStart(self):
        if self.ui.lineEdit_Cthreshold_dryOrSweaty.text() == '':
            self.ui.lineEdit_Cthreshold_dryOrSweaty.setText("250")
        if self.ui.lineEdit_Cthreshold_noise.text() == '':
            self.ui.lineEdit_Cthreshold_noise.setText("110")
        self.ui.label_capaci_dryVal.setText(self.ui.lineEdit_Cthreshold_dryOrSweaty.text())
        self.ui.label_capaci_sweatyVal2.setText(self.ui.lineEdit_Cthreshold_dryOrSweaty.text())
        self.ui.label_capaci_sweatyVal1.setText(self.ui.lineEdit_Cthreshold_noise.text())
        self.ui.label_capaci_noiseVal.setText(self.ui.lineEdit_Cthreshold_noise.text())
        thread = threading.Thread(target=self.start_plot, name='thread')
        thread.start()

    def start_plot(self):
        global Cvalue, portName, ser

        ### function
        def update(sample):
            """
            Load V_ADC raw data
            """
            Data, Cdata, Pdata = [], [], []
            for i in range(sample):
                value = str(ser.readline(), 'utf-8')
                print("buffer: ", ser.in_waiting)
                print(value)
                if 'C' in value:
                    Cvalue = value.replace('C', '')
                    if Cvalue != '\n' and 'E' not in Cvalue and 'P' not in Cvalue:
                        Cdata.append(int(Cvalue) / 1000)
                elif 'P' in value:
                    # Pvalue = value.replace('P', '')
                    Pvalue = value.replace('mmHg', '')
                    Pvalue = Pvalue.replace('P', '')
                    if Pvalue != '\n' and 'E' not in Pvalue and 'C' not in Pvalue:
                        Pdata.append(int(Pvalue))
                elif 'E' in value and len(value)>5 and len(value)<7:
                    EMGvalue = value.replace('E', '')
                    if EMGvalue != '\n':
                        if 'C' not in EMGvalue and 'P' not in EMGvalue:
                            Data.append(int(EMGvalue)/1000)
            print("C({}): ".format(len(Cdata)), Cdata)
            print("EMG({}): ".format(len(Data)), "C({}): ".format(len(Cdata)), "P({}): ".format(len(Pdata)))
            return Data, Cdata, Pdata

        def bandStopFilter(x, low, high):
            """
            Remove the Working Frequency Noise about 50(Hz) * n.
            :param x: the data that need to be filtered.
            :param low/high: below/ above the low/hjgh ferquency
            :return y: the band-stop filtered data of ECG
            """
            b, a = signal.butter(1, [float(low), float(high)], 'bandstop')
            y = signal.filtfilt(b, a, x)
            return y

        def medianFilter(x, R):
            """
            Median Filter to solve the problem of Baseline Wandering.
            :param x: the array of ECG raw signal data.
            :param R: (median filter window length = 2*R+1)
            :return y: the median filtered data of ECG
            """
            y = []
            for i in range(len(x)):
                if (i + R) <= len(x) and (i - R) >= 1:
                    med = np.median(x[(i - R):(i + R)])
                elif (i + R) <= len(x) and (i - R) < 1:
                    med = np.median(x[:(i + R)])
                elif (i + R) > len(x) and (i - R) >= 1:
                    med = np.median(x[(i - R):])
                else:
                    med = np.median(x[:])
                y.append(x[i] - med)
            y = np.array(y)
            return y

        def smoothCurve(data, winsize):
            window = np.ones(winsize) / winsize
            return np.convolve(data, window, mode='same')

        ###
        # parameter settings for reading data
        self.portName = self.ui.label_BTConnected_Item.text()
        self.samplePoint = 500  # after how many points -> starting cal C
        self.thrd = 10  # how many periods would be cal
        self.winSize = 5000

        # FW and HW Parameter settings
        self.R = 1 * 10 ** 6  # Ohm
        self.pwmPeriod = 2 * 10 ** (-3)  # sec
        self.sampleHZ = 6 * 10 ** 3  # Hz
        self.sampleRate = 1 / self.sampleHZ  # sec
        self.point = self.pwmPeriod // self.sampleRate
        self.tauPercent = 0.632
        self.sample_rate = 1500  # EMG sample rate

        # Start updating the value of pygraph window
        self.CdataWin = np.linspace(0, 0, 500)
        self.EMGdataWin = np.linspace(0, 0, self.winSize)
        self.compenEMGdataWin = np.linspace(0, 0, self.winSize)
        self.crossEmgdataWin = np.linspace(0, 0, self.winSize)
        self.gainLen, noise, noiseCom, maxAmp = [], [], [], []
        self.gainLen.append(0)
        noise.append(0)
        noiseCom.append(0)
        maxAmp.append(0)

        # while True:
        while self.portName is not None:
            # load signal
            self.Data, self.Cdata, self.Pdata = update(self.samplePoint)

            # calculate C and show C result in GUI
            if len(self.Cdata) > 20:
                for i in range(len(self.Cdata)):
                    self.CdataWin[-1] = self.Cdata[i]
                    self.CdataWin[:-1] = self.CdataWin[1:]
                # thread for calculating C
                q = Queue()
                thread_C = threading.Thread(target=self.calcuC, args=(self.Cdata, q))
                thread_C.start()
                self.Cmessage = q.get()
                # Transform C data into value for importing to pygraph and C value label
                self.lenC = int(str(self.Cmessage['Length of C']))
                self.Cvalue = float(round(float(self.Cmessage['Average capacitance value(F)'])/(10**(-12)), 3))
                if self.ui.lineEdit_Cthreshold_dryOrSweaty.text() == '':
                    self.ui.lineEdit_Cthreshold_dryOrSweaty.setText("250")
                if self.ui.lineEdit_Cthreshold_noise.text() == '':
                    self.ui.lineEdit_Cthreshold_noise.setText("110")
                CThd_noise = float(self.ui.lineEdit_Cthreshold_noise.text())
                CThd_drySweaty = float(self.ui.lineEdit_Cthreshold_dryOrSweaty.text())
                if self.lenC != 0:
                    self.ui.label_capaci_val.setText(str(self.Cvalue))
                    self.ui.label_capaci_val.setAlignment(QtCore.Qt.AlignCenter)
                    self.ui.label_capaci_val_2.setText(str(self.Cvalue))
                    self.ui.label_capaci_val_2.setAlignment(QtCore.Qt.AlignCenter)
                    if self.Cvalue > CThd_drySweaty:
                        self.ui.label_capaci_state.setText("(Dry skin)")
                    elif CThd_drySweaty > self.Cvalue and self.Cvalue > CThd_noise: 
                        self.ui.label_capaci_state.setText("(Sweaty skin)")
                    elif self.Cvalue < CThd_noise:
                        self.ui.label_capaci_state.setText("(Noise)")

            # show P result in GUI
            if len(self.Pdata) != 0:
                self.ui.label_pressure_val.setText(str(self.Pdata[-1]))
                self.ui.label_pressure_val.setAlignment(QtCore.Qt.AlignCenter)

            # Process EMG data
            if len(self.Data) > 9:
                FilterData = medianFilter(self.Data, 30)
                # The length of the input vector self.Data must be greater than padlen, which is 9.
                bandStopFilterData = bandStopFilter(FilterData, (60 - 2) / self.sample_rate, (60 + 2) / self.sample_rate)

            # zeroIndex = [index for (index, value) in enumerate(self.compenEMGdataWin[1:500]) if -0.001 < value < 0.001]
            for i in range(len(self.Data)):
                # Raw data
                self.EMGdataWin[-1] = self.Data[i]
                self.EMGdataWin[:-1] = self.EMGdataWin[1:]
                # Compensate data
                self.compenEMGdataWin[-1] = bandStopFilterData[i]
                self.crossEmgdataWin[-1] = bandStopFilterData[i]
                # update window
                self.compenEMGdataWin[:-1] = self.compenEMGdataWin[1:]
                self.crossEmgdataWin[:-1] = self.crossEmgdataWin[1:]

            # QtGui.QApplication.processEvents()
            QtCore.QCoreApplication.processEvents()
            print()

            # the detection of muscular activation
            emgIndex = [index for (index, value) in enumerate(self.crossEmgdataWin[:]) if value > 0.02]
            if len(emgIndex) > 100:
                rectSignal = np.absolute(self.crossEmgdataWin)
                smoothSignal = smoothCurve(rectSignal, 100)
                threshold = np.average(smoothSignal)
                index_on_off = []
                flag_onset = False
                temp_onset = None
                self.binary = np.zeros(len(smoothSignal))
                for index, sample_value in enumerate(smoothSignal):
                    if sample_value > threshold and flag_onset is False:
                        temp_onset = index
                        flag_onset = True
                    elif sample_value < threshold and flag_onset is True:
                        index_on_off.append((temp_onset, index))
                        flag_onset = False

                # indicate EMG feature and calculate the SNR
                for i in range(len(index_on_off)):
                    if (index_on_off[i][1] - index_on_off[i][0]) > 500 and index_on_off[i][0] > 30:
                        # indicating EMG feature
                        self.binary[index_on_off[i][0]:index_on_off[i][1]] = 1
                        # computing SNR (dB): Raw signal
                        emgLength = index_on_off[i][1] - index_on_off[i][0]
                        print("emg length: ", emgLength, "\n")
                        emgFeature = self.EMGdataWin[index_on_off[i][0]:index_on_off[i][1]]
                        vpp_signal = max(emgFeature) - min(emgFeature)
                        noiseFeature = self.EMGdataWin[(index_on_off[i][0] - 300 - emgLength // 3):(index_on_off[i][0] - 300)]
                        if len(noiseFeature) != 0:
                            noise.append(noiseFeature)
                        elif len(noiseFeature) == 0:
                            noiseFeature = noise[-1]
                        vpp_noise = max(noiseFeature) - min(noiseFeature)
                        self.SNR = round((10 * math.log10(vpp_signal / vpp_noise)), 3)
                        self.ui.label_CH1SNR_val.setText(str(self.SNR))

                        # checking C and compensating
                        C_currentVal = float(self.ui.label_capaci_val.text())
                        if self.ui.lineEdit_Cthreshold_dryOrSweaty.text() == '':
                            self.ui.lineEdit_Cthreshold_dryOrSweaty.setText("250")
                        if self.ui.lineEdit_Cthreshold_noise.text() == '':
                            self.ui.lineEdit_Cthreshold_noise.setText("110")
                        CThd_noise = float(self.ui.lineEdit_Cthreshold_noise.text())
                        CThd_drySweaty = float(self.ui.lineEdit_Cthreshold_dryOrSweaty.text())
                        if C_currentVal > CThd_noise and emgLength != self.gainLen[-1]:
                            if max(self.compenEMGdataWin[index_on_off[i][0]:index_on_off[i][1]]) != maxAmp[-1] and min(
                                    self.compenEMGdataWin[index_on_off[i][0]:index_on_off[i][1]]) > -1.2 and max(
                                    self.compenEMGdataWin[index_on_off[i][0]:index_on_off[i][1]]) < 1.2:
                                self.gainLen.append(emgLength)
                                # compensate v2
                                if C_currentVal > CThd_drySweaty:
                                    gain = 3.5  # dry
                                elif C_currentVal < CThd_drySweaty:
                                    gain = 2.5  # wet
                                self.compenEMGdataWin[index_on_off[i][0]:index_on_off[i][1]] = self.crossEmgdataWin[
                                                                             index_on_off[i][0]:index_on_off[i][1]] * gain
                                maxAmp.append(max(self.compenEMGdataWin[index_on_off[i][0]:index_on_off[i][1]]))
                                print("Gain {}!".format(gain), "\n")
                                # computing SNR (dB): compensated signal
                                emgFeatureCom = self.compenEMGdataWin[index_on_off[i][0]:index_on_off[i][1]]
                                vpp_signal_com = max(emgFeatureCom) - min(emgFeatureCom)
                                noiseFeatureCom = self.compenEMGdataWin[
                                                  (index_on_off[i][0] - 300 - emgLength // 3):(index_on_off[i][0] - 300)]
                                if len(noiseFeatureCom) != 0:
                                    noiseCom.append(noiseFeatureCom)
                                elif len(noiseFeatureCom) == 0:
                                    noiseFeatureCom = noiseCom[-1]
                                vpp_noise_com = max(noiseFeatureCom) - min(noiseFeatureCom)
                                self.SNR_com = round((10 * math.log10(vpp_signal_com / vpp_noise_com)), 3)
                                self.ui.label_CH2SNR_val.setText(str(self.SNR_com))

            else:
                self.binary = np.zeros(len(self.compenEMGdataWin))

            # Emitting this signal ensures update_graph() will run in the main thread
            # since the signal was connected in the __init__ function (main thread)
            self.signalComm.request_graph_update.emit()
            self.signalComm.request_Cgraph_update.emit()


    def update_graph(self):
        global curve1, curve2, curve3
        curve1.setData(self.EMGdataWin)
        curve2.setData(self.compenEMGdataWin)
        curve3.setData(self.binary)

    def update_Cgraph(self):
        global curveC
        curveC.setData(self.CdataWin)

    def stopPlot(self):
        self.portName = None
        # save data
        C_currentVal = float(self.ui.label_capaci_val.text())
        t_current = str(time.strftime("%Y%m%d_%H-%M-%S", time.localtime()))
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet("Saved data")
        sheet1.write(0, 0, "Raw")
        sheet1.write(0, 1, "Compensated")
        sheet1.write(0, 2, "EMG feature")
        sheet1.write(0, 3, "Capacitance")
        sheet1.write(1, 3, C_currentVal)
        sheet1.write(0, 4, "ch1/ch2 SNR")
        sheet1.write(1, 4, "{} / {}".format(self.SNR, self.SNR_com))
        for i in range(len(self.EMGdataWin)):
            sheet1.write(i + 1, 0, self.EMGdataWin[i])
            sheet1.write(i + 1, 1, self.compenEMGdataWin[i])
            sheet1.write(i + 1, 2, self.binary[i])
        workbook.save(r'C:\Users\K100\PycharmProjects\GUI\Save data\{}.csv'.format(t_current))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    # window.showFullScreen()
    sys.exit(app.exec_())



