import ctypes
from math import *
import sys
import webbrowser
import subprocess
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QApplication, QTableWidgetItem, QHBoxLayout)
from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QSize, Qt
pr = 'page_2.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        

   
   

        


if __name__ == '__main__':
    appl = QApplication(sys.argv)
win = mywindow()
win.show()
sys.exit(appl.exec())
