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

# p2 = win.addPlot(title="RMS plot")  # create empty space for the plot in the window
# p2.setYRange(min=int(Y_range[0]), max=int(Y_range[1]))
curve = p.plot(pen=pg.mkPen(color='k', width=0.2))
curve2 = p.plot(pen=pg.mkPen(color='b', width=0.5))
# create an empty "plot" (a curve to plot)
# pg.setConfigOption('background', 'w')

windowWidth = 1500
Xm = linspace(0, 0, 1500)
# windowWidth = 100                       # width of the window displaying the curve
# Xm = linspace(0, 0, 250)         # create array that will contain the relevant time series
ptr = -windowWidth                       # set first x position
Value = deque(maxlen=len(Xm))
saveData = []
index = 0
today = date.today()
d1 = today.strftime("%b-%d-%Y")
now = datetime.now()
current_time = now.strftime("%H-%M-%S")
storagePath = f"{desktop}\\{d1}{current_time}.csv"
# storagePath = f"C:\\Users\\{d1}{current_time}.csv"

# Realtime data plot.
# Each time this function is called, the data display is updated
def update():
    global curve, curve2, ptr, Xm, saveData, index
    value = ser.readline().decode("utf-8", errors = 'ignore')
    # print(value)
    saveData.append(value)
    if len(value) > 2:
        value = float(value)
        if int(value / 10000) == 2:
            Xm[:-1] = Xm[1:]
            # shift data in the temporal mean 1 sample left
    # value = str(ser.readline(), 'utf-8')
    # print("my value" + value)


    # Raw signal
    # if value != '\r\n':
    # if value != '\n':
            if value != '\n':
                if int(value / 10000) == 2:
                    # print(value % 10000)
                    value = (value % 10000) -1500
                    Xm[-1] = value             # vector containing the instantaneous values
                    # index = index + 1
                    # saveData.append(value) # saveData all data not only specific channel
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
                    if index % 500 == 0:
                        with open(storagePath, "w", newline="\n") as csvfile:
                            wr = csv.writer(csvfile)
                            print("Save Data to .CSV")
                            # wr.writerow(saveData[1: index])
                            for word in range(1, len(saveData)):
                                wr.writerow([saveData[word]])

    # # Filtered signal: Median Filter to solve Baseline Wandering.
    # if value != '\r\n':
    #     print(value)
    #     Value.append(float(value))
    # if Value[-1] != 0:
    #     for i in range(len(Value)):
    #         med = np.median(Value)
    #     Xm[-1] = Value[-1] - med




### MAIN PROGRAM ###
# this is a brutal infinite loop calling the realtime data plot
while True:
    update()

### END QtApp ###
pg.QtGui.QApplication.exec_() # you MUST put this at the end

##################

