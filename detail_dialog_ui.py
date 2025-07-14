# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detail_dialog.ui'

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.spinBox_qapi_sayi = QtWidgets.QSpinBox(Dialog)
        self.spinBox_qapi_sayi.setPrefix("Qapı sayı: ")
        self.verticalLayout.addWidget(self.spinBox_qapi_sayi)

        self.doubleSpinBox_qapi_eni = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBox_qapi_eni.setPrefix("Qapı eni (m): ")
        self.verticalLayout.addWidget(self.doubleSpinBox_qapi_eni)

        self.doubleSpinBox_qapi_uzun = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBox_qapi_uzun.setPrefix("Qapı uzunluğu (m): ")
        self.verticalLayout.addWidget(self.doubleSpinBox_qapi_uzun)

        self.spinBox_pencere_sayi = QtWidgets.QSpinBox(Dialog)
        self.spinBox_pencere_sayi.setPrefix("Pəncərə sayı: ")
        self.verticalLayout.addWidget(self.spinBox_pencere_sayi)

        self.doubleSpinBox_pencere_eni = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBox_pencere_eni.setPrefix("Pəncərə eni (m): ")
        self.verticalLayout.addWidget(self.doubleSpinBox_pencere_eni)

        self.doubleSpinBox_pencere_uzun = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBox_pencere_uzun.setPrefix("Pəncərə uzunluğu (m): ")
        self.verticalLayout.addWidget(self.doubleSpinBox_pencere_uzun)

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setText("Təsdiq et")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtCore.QCoreApplication.translate("Dialog", "Otaq Təfərrüatı"))
