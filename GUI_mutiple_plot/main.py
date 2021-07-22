#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:dell
import sys
import numpy as np
from PyQt5 import QtWidgets
import pyqtgraph as pg

from main_ui import Ui_MainWindow


class MyGraphWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):

        super(MyGraphWindow, self).__init__()
        self.setupUi(self) # Initialize the window
        self.p1, self.p2 = self.set_graph_ui() # set the drawing window
        self.btn.clicked.connect(self.plot_sin_cos) # Click the button to start drawing

    def set_graph_ui(self):
        pg.setConfigOptions(antialias=True) # pg global variable setting function, antialias=True open curve anti-aliasing
        win = pg.GraphicsLayoutWidget() # Create pg layout for automatic management of data interface layout
        # pg The drawing window can be added to the graph_layout in the GUI as a widget, and of course can be added to all other Qt containers.
        self.graph_layout.addWidget(win)
        p1 = win.addPlot(title="sin function") # Add the first drawing window
        p1.setLabel('left', text='meg', color='#ffffff') # y axis setting function
        p1.showGrid(x=True, y=True) # Grid setting function
        p1.setLogMode(x=False, y=False) # False stands for linear axis, True stands for logarithmic axis
        p1.setLabel('bottom', text='time', units='s') # x axis setting function
        # p1.addLegend() # Select whether to add legend

        win.nextRow() #layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p2 = win.addPlot(title="cos function")
        p2.setLabel('left', text='meg', color='#ffffff')
        p2.showGrid(x=True, y=True)
        p2.setLogMode(x=False, y=False)
        p2.setLabel('bottom', text='time', units='s')
        # p2.addLegend()
        return p1, p2

    def plot_sin_cos(self):
        t = np.linspace(0, 20, 200)
        y_sin = np.sin(t)
        y_cos = np.cos(t)
        self.p1.plot(t, y_sin, pen='g', name='sin(x)', clear=True)
        self.p2.plot(t, y_cos, pen='g', name='con(x)', clear=True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWin = MyGraphWindow()
    myWin.show()
    sys.exit(app.exec_())

