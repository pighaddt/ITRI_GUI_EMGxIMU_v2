# Import libraries
import numpy as np
import os
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
# from PhysioNetData import medianFilter, bandStopFilter
from collections import deque
import csv
from datetime import date
from datetime import datetime
# Create object serial port

portName = "COM4"
baudRate = 115200
R = 30
Y_range = [-2500, 2500]
# ser = serial.Serial(portName, baudRate)
ser = serial.Serial(portName, int(baudRate), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
print(desktop)
### START QtApp #####
app = QtGui.QApplication([])            # initialize things
####################
win = pg.GraphicsWindow(title="Signal from Bluetooth")  # create a window
win.setBackground('w')
p = win.addPlot(title="Realtime plot")  # create empty space for the plot in the window
p.setYRange(min=int(Y_range[0]), max=int(Y_range[1]))
curve = p.plot(pen=pg.mkPen(color='k', width=0.2))
curve2 = p.plot(pen=pg.mkPen(color='b', width=0.5))

windowWidth = 1500
Xm = linspace(0, 0, 1500)
# windowWidth = 100                       # width of the window displaying the curve
# Xm = linspace(0, 0, 250)         # create array that will contain the relevant time series
ptr = -windowWidth                       # set first x position
Value = deque(maxlen=len(Xm))
saveData1 = []
saveData2 = []
index = 0
today = date.today()
d1 = today.strftime("%b-%d-%Y")
now = datetime.now()
current_time = now.strftime("%H-%M-%S")
storagePath = f"{desktop}\\{d1}{current_time}.csv"
def update():
    global curve, curve2, ptr, Xm, saveData, index
    value = ser.readline().decode("utf-8", errors = 'ignore')
    print(value)
    if len(value) > 2:
        value = float(value)
        if int(value / 10000) == 1:
            Xm[:-1] = Xm[1:]
            if value != '\n':
                if int(value / 10000) == 1:
                    # print(value % 10000)
                    value = (value % 10000)
                    Xm[-1] = value             # vector containing the instantaneous values
                    # index = index + 1
                    saveData1.append(value)
                    saveData2.append('123')
                    index += 1
                    # print(saveData)
                    ptr += 1  # update x position for displaying the curve
                    curve.setData(Xm)  # set the curve with these data
                    # rms = rms_function(Xm, 50)
                    # print( int(rms[-1]))
                    # myRMS = int(rms[-1])
                    # curve2.setData(rms)  # set the curve with these data
                    # curve.setPos(ptr, 0)  # set x posiYtion in the graph to 0
                    QtGui.QApplication.processEvents()  # process the plot now
                    # if index % 500 == 0:
                    #     # print(saveData)
                    #     with open(storagePath, "w", newline="\n") as csvfile:
                    #         wr = csv.writer(csvfile)
                    #         print("Save Data to .CSV")
                    #         # wr.writerow(saveData[1: index])
                    #         for word in range(1, len(saveData1)):
                    #             wr.writerow([saveData1[word], saveData2[word]])




### MAIN PROGRAM ###
# this is a brutal infinite loop calling the realtime data plot
while True:
    update()

### END QtApp ###
pg.QtGui.QApplication.exec_() # you MUST put this at the end

##################

