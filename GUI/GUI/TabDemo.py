# http://www.tastones.com/zh-tw/tutorial/pyqt5/pyqt5-tabs/
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from BTDemo2 import BTServer

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('GUI of SEMICON Taiwan')
        self.setGeometry(0, 0, 1000, 800)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()

class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.BTServer.startServer(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Setting")
        self.tabs.addTab(self.tab2, "Processing")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton = QPushButton("PyQt5 button")
        self.pushButton.clicked.connect(self.on_click)
        self.tab1.layout.addWidget(self.pushButton)
        self.tab1.setLayout(self.tab1.layout)

        #
        self.pushButton1 = QPushButton("Close window")
        self.pushButton1.clicked.connect(self.on_pushButton_2_clicked)
        self.layout.addWidget(self.pushButton1)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    @pyqtSlot()
    def on_pushButton1_clicked(self):
        self.close()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.showMinimized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.showFullScreen()
    sys.exit(app.exec_())