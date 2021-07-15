import random

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import time
import numpy as np


app = QtGui.QApplication([])



win = pg.GraphicsWindow()

p1 = win.addPlot()
p2 = win.addPlot()
p3 = win.addPlot()


curve1 = p1.plot()

curve2 = p2.plot()

curve3 = p3.plot()

readData = [0.0, 0.0, 0.0]
y1=[0.0]
y2=[0.0]
y3=[0.0]

temp = [0.0]

start = time.time()

def update():
    global curve1, curve2, curve3
    t = time.time()-start         # measure of time as x-coordinate
    readData= [random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)]    #function that reads data from the sensor it returns a list of 3 elements as the y-coordinates for the updating plots
    y1.append(readData[0])
    y2.append(readData[1])
    y3.append(readData[2])
    temp.append(t)

    curve1.setData(temp,y1)
    curve2.setData(temp,y2)
    curve3.setData(temp,y3)
    app.processEvents()



timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)




if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_'):
        QtGui.QApplication.instance().exec_()