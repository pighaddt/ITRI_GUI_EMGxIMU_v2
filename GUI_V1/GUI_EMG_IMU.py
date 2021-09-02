# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_EMG_IMU.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 0, 1231, 721))
        font = QtGui.QFont()
        font.setItalic(False)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_connection = QtWidgets.QWidget()
        self.tab_connection.setObjectName("tab_connection")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_connection)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 210, 385, 471))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_6.setTextFormat(QtCore.Qt.RichText)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.comboBox_Device1CP = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_Device1CP.setObjectName("comboBox_Device1CP")
        self.gridLayout.addWidget(self.comboBox_Device1CP, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.comboBox_Device1BR = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_Device1BR.setObjectName("comboBox_Device1BR")
        self.gridLayout.addWidget(self.comboBox_Device1BR, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.comboBox_Device2CP = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_Device2CP.setObjectName("comboBox_Device2CP")
        self.gridLayout.addWidget(self.comboBox_Device2CP, 2, 1, 1, 1)
        self.pushButton_EMG = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_EMG.setObjectName("pushButton_EMG")
        self.gridLayout.addWidget(self.pushButton_EMG, 5, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_5.setTextFormat(QtCore.Qt.RichText)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.pushButton_IMU = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_IMU.setObjectName("pushButton_IMU")
        self.gridLayout.addWidget(self.pushButton_IMU, 6, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.comboBox_Device2BR = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_Device2BR.setObjectName("comboBox_Device2BR")
        self.gridLayout.addWidget(self.comboBox_Device2BR, 4, 1, 1, 1)
        self.pushButton_searchSP = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_searchSP.setObjectName("pushButton_searchSP")
        self.gridLayout.addWidget(self.pushButton_searchSP, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab_connection)
        self.label_7.setGeometry(QtCore.QRect(410, 370, 181, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_7.setTextFormat(QtCore.Qt.RichText)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.textEdit_info = QtWidgets.QTextEdit(self.tab_connection)
        self.textEdit_info.setGeometry(QtCore.QRect(410, 410, 791, 271))
        self.textEdit_info.setObjectName("textEdit_info")
        self.label_8 = QtWidgets.QLabel(self.tab_connection)
        self.label_8.setGeometry(QtCore.QRect(10, 20, 481, 161))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("../icons/ITRI_logo.png"))
        self.label_8.setScaledContents(True)
        self.label_8.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.tab_connection)
        self.label_9.setGeometry(QtCore.QRect(500, 20, 701, 161))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(40)
        self.label_9.setFont(font)
        self.label_9.setTextFormat(QtCore.Qt.AutoText)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.tabWidget.addTab(self.tab_connection, "")
        self.tab_plot = QtWidgets.QWidget()
        self.tab_plot.setObjectName("tab_plot")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_plot)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 1161, 641))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_SaveIMUData = QtWidgets.QPushButton(self.tab_plot)
        self.pushButton_SaveIMUData.setGeometry(QtCore.QRect(996, 660, 131, 28))
        self.pushButton_SaveIMUData.setObjectName("pushButton_SaveIMUData")
        self.pushButton_StartIMUPlot = QtWidgets.QPushButton(self.tab_plot)
        self.pushButton_StartIMUPlot.setGeometry(QtCore.QRect(10, 660, 91, 28))
        self.pushButton_StartIMUPlot.setObjectName("pushButton_StartIMUPlot")
        self.pushButton_CloseIMUPlot = QtWidgets.QPushButton(self.tab_plot)
        self.pushButton_CloseIMUPlot.setGeometry(QtCore.QRect(110, 660, 93, 28))
        self.pushButton_CloseIMUPlot.setObjectName("pushButton_CloseIMUPlot")
        self.tabWidget.addTab(self.tab_plot, "")
        self.tab_algorithm = QtWidgets.QWidget()
        self.tab_algorithm.setObjectName("tab_algorithm")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_algorithm)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(30, 10, 1161, 641))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_SaveEMGData = QtWidgets.QPushButton(self.tab_algorithm)
        self.pushButton_SaveEMGData.setGeometry(QtCore.QRect(996, 660, 131, 28))
        self.pushButton_SaveEMGData.setObjectName("pushButton_SaveEMGData")
        self.pushButton_CloseEMGPlot = QtWidgets.QPushButton(self.tab_algorithm)
        self.pushButton_CloseEMGPlot.setGeometry(QtCore.QRect(110, 660, 93, 28))
        self.pushButton_CloseEMGPlot.setObjectName("pushButton_CloseEMGPlot")
        self.pushButton_StartEMGPlot = QtWidgets.QPushButton(self.tab_algorithm)
        self.pushButton_StartEMGPlot.setGeometry(QtCore.QRect(10, 660, 91, 28))
        self.pushButton_StartEMGPlot.setObjectName("pushButton_StartEMGPlot")
        self.tabWidget.addTab(self.tab_algorithm, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(450, 15, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(450, 230, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(450, 270, 761, 161))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(450, 450, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(450, 490, 761, 161))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(20, 250, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(40, 290, 321, 311))
        self.label_14.setText("")
        self.label_14.setPixmap(QtGui.QPixmap("../icons/angle_draw.jpg"))
        self.label_14.setScaledContents(True)
        self.label_14.setObjectName("label_14")
        self.label_angle = QtWidgets.QLabel(self.tab)
        self.label_angle.setGeometry(QtCore.QRect(10, 610, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_angle.setFont(font)
        self.label_angle.setObjectName("label_angle")
        self.pushButton_LoadEMG = QtWidgets.QPushButton(self.tab)
        self.pushButton_LoadEMG.setGeometry(QtCore.QRect(20, 50, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_LoadEMG.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Desktop/EMG.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_LoadEMG.setIcon(icon)
        self.pushButton_LoadEMG.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_LoadEMG.setObjectName("pushButton_LoadEMG")
        self.pushButton_LoadIMU = QtWidgets.QPushButton(self.tab)
        self.pushButton_LoadIMU.setGeometry(QtCore.QRect(200, 50, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_LoadIMU.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../Desktop/IMU.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_LoadIMU.setIcon(icon1)
        self.pushButton_LoadIMU.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_LoadIMU.setShortcut("")
        self.pushButton_LoadIMU.setCheckable(False)
        self.pushButton_LoadIMU.setObjectName("pushButton_LoadIMU")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(450, 50, 759, 159))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_EMGDevice1 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_EMGDevice1.setGeometry(QtCore.QRect(610, 20, 151, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_EMGDevice1.setFont(font)
        self.checkBox_EMGDevice1.setObjectName("checkBox_EMGDevice1")
        self.checkBox_EMGDevice2 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_EMGDevice2.setGeometry(QtCore.QRect(610, 230, 151, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_EMGDevice2.setFont(font)
        self.checkBox_EMGDevice2.setObjectName("checkBox_EMGDevice2")
        self.tabWidget.addTab(self.tab, "")
        self.pushButton_Reset = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Reset.setGeometry(QtCore.QRect(1070, 720, 93, 28))
        self.pushButton_Reset.setObjectName("pushButton_Reset")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_6.setText(_translate("MainWindow", "IMU Device"))
        self.label.setText(_translate("MainWindow", "Device 1 Com Port"))
        self.label_3.setText(_translate("MainWindow", "Device 2 Com Port"))
        self.label_4.setText(_translate("MainWindow", "Device 2 Baud Rate"))
        self.pushButton_EMG.setText(_translate("MainWindow", "Connect Device 1"))
        self.label_5.setText(_translate("MainWindow", "EMG Device"))
        self.pushButton_IMU.setText(_translate("MainWindow", "Connect Device 2"))
        self.label_2.setText(_translate("MainWindow", "Device 1 Baud Rate"))
        self.pushButton_searchSP.setText(_translate("MainWindow", "Search Serial Port"))
        self.label_7.setText(_translate("MainWindow", "Command Window"))
        self.label_9.setText(_translate("MainWindow", "EMG IMU 多通道介面"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_connection), _translate("MainWindow", "Connection"))
        self.pushButton_SaveIMUData.setText(_translate("MainWindow", "Save IMU Data"))
        self.pushButton_StartIMUPlot.setText(_translate("MainWindow", "Start Ploting"))
        self.pushButton_CloseIMUPlot.setText(_translate("MainWindow", "Close Ploting"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_plot), _translate("MainWindow", "IMU Real Time Plot"))
        self.pushButton_SaveEMGData.setText(_translate("MainWindow", "Save EMG Data"))
        self.pushButton_CloseEMGPlot.setText(_translate("MainWindow", "Close Ploting"))
        self.pushButton_StartEMGPlot.setText(_translate("MainWindow", "Start Ploting"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_algorithm), _translate("MainWindow", "EMG Real Time Plot"))
        self.label_10.setText(_translate("MainWindow", "EMG Device 1"))
        self.label_11.setText(_translate("MainWindow", "EMG Device 2"))
        self.label_12.setText(_translate("MainWindow", "IMU Device Angle"))
        self.label_13.setText(_translate("MainWindow", "IMU Angle "))
        self.label_angle.setText(_translate("MainWindow", "Current Angle : 90"))
        self.pushButton_LoadEMG.setText(_translate("MainWindow", "Load EMG"))
        self.pushButton_LoadIMU.setText(_translate("MainWindow", "Load IMU"))
        self.checkBox_EMGDevice1.setText(_translate("MainWindow", "Start Point Detect"))
        self.checkBox_EMGDevice2.setText(_translate("MainWindow", "Start Point Detect"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Algorithm"))
        self.pushButton_Reset.setText(_translate("MainWindow", "Reset"))