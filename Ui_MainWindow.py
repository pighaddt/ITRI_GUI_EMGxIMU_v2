# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        #若未設置centralWidget 則元件大小不會隨視窗縮放而改變
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        #設置幾何 QtCore.QRect(left, top, width, height)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 40, 1400, 800))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 900, 1401, 28))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.menubar.show()
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        # self.statusbar.showMessage("HI  Statusbar ")
        MainWindow.setStatusBar(self.statusbar)
        ## add menubar setting
        # exitAction = QAction("&Exit", MainWindow)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        # exitAction.triggered.connect(qApp.quit)
        #
        # # self.statusbar()
        #
        # # menubar = self.menuBar()
        # fileMenu = self.menubar.addMenu('&File')
        # fileMenu.addAction(exitAction)
        #
        # # self.setWindowTitle('PyQt5 Basic Menubar')
        # # self.show()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start Data Ploting(Open Serial ComPort)"))
