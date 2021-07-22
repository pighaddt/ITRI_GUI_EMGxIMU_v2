from PyQt5 import QtWidgets, QtGui, QtCore
import sys

from Ui_MainWindow import Ui_MainWindow
import pyqtgraph as pg
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__() #inherit Mainwindow super function
        self.ui = Ui_MainWindow() # your mainwindow from pyuic5
        self.ui.setupUi(self) # your init setupUI function
        self.p1, self.p2, self.p3 = self.set_graph_ui()  # set the drawing window
        # self.pushButton.clicked.connect(self.plot_sin_cos)  # Click the button to start drawing and change button text
        self.ui.pushButton.clicked.connect(self.plot_sin_cos)

    def set_graph_ui(self):
        pg.setConfigOptions(antialias=True)  # pg global variable setting function, antialias=True open curve anti-aliasing
        win = pg.GraphicsLayoutWidget()  # Create pg layout for automatic management of data interface layout
        win.setBackground('w')
        # pg The drawing window can be added to the graph_layout in the GUI as a widget, and of course can be added to all other Qt containers.
        # self.verticalLayoutWidget.addWidget(win)
        self.ui.verticalLayout.addWidget(win)
        p1 = win.addPlot(title="EMG Raw Data")  # Add the first drawing window
        p1.setLabel('left', text='mV', color='#ffffff')  # y axis setting function
        p1.showGrid(x=True, y=True)  # Grid setting function
        p1.setLogMode(x=False, y=False)  # False stands for linear axis, True stands for logarithmic axis
        p1.setLabel('bottom', text='time', units='s')  # x axis setting function
        # p1.addLegend() # Select whether to add legend

        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p2 = win.addPlot(title="IMU 1 Raw Data")
        p2.setLabel('left', text='angle', color='#ffffff')
        p2.showGrid(x=True, y=True)
        p2.setLogMode(x=False, y=False)
        p2.setLabel('bottom', text='time', units='s')
        # p2.addLegend()

        win.nextRow()  # layouts, arranged vertically, without adding this line, the default horizontal arrangement
        p3 = win.addPlot(title="IMU 2 Raw Data")
        p3.setLabel('left', text='angle', color='#ffffff')
        p3.showGrid(x=True, y=True)
        p3.setLogMode(x=False, y=False)
        p3.setLabel('bottom', text='time', units='s')
        return p1, p2, p3

    def plot_sin_cos(self):
        t = np.linspace(0, 20, 200)
        y_sin = np.sin(t)
        y_cos = np.cos(t)
        self.p1.plot(t, y_sin, pen='g', name='sin(x)', clear=True)
        self.p2.plot(t, y_cos, pen='g', name='con(x)', clear=True)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.instance().exec_())