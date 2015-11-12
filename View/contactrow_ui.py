# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contactrow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(459, 68)
        Form.setMaximumSize(QtCore.QSize(16777215, 68))
        Form.setStyleSheet("QLabel {background-color: rgba(255, 255, 255, 0);color:#333333;}\n"
"QGraphicsView {background-color: rgba(255, 255, 255, 0);border:0px;}")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.name_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.gridLayout.addWidget(self.name_label, 0, 1, 1, 1)
        self.status__msg_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(9)
        self.status__msg_label.setFont(font)
        self.status__msg_label.setStyleSheet("")
        self.status__msg_label.setObjectName("status__msg_label")
        self.gridLayout.addWidget(self.status__msg_label, 1, 1, 1, 1)
        self.new_msg_label = QtWidgets.QLabel(Form)
        self.new_msg_label.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(10)
        self.new_msg_label.setFont(font)
        self.new_msg_label.setAlignment(QtCore.Qt.AlignCenter)
        self.new_msg_label.setObjectName("new_msg_label")
        self.gridLayout.addWidget(self.new_msg_label, 1, 2, 1, 1)
        self.available_label = QtWidgets.QLabel(Form)
        self.available_label.setMaximumSize(QtCore.QSize(25, 25))
        self.available_label.setText("")
        self.available_label.setObjectName("available_label")
        self.gridLayout.addWidget(self.available_label, 0, 2, 1, 1)
        self.image_label = QtWidgets.QLabel(Form)
        self.image_label.setMaximumSize(QtCore.QSize(50, 50))
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.gridLayout.addWidget(self.image_label, 0, 0, 2, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.name_label.setText(_translate("Form", "Name"))
        self.status__msg_label.setText(_translate("Form", "status"))
        self.new_msg_label.setText(_translate("Form", "1"))

