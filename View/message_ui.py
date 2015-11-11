# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(610, 504)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.head_table = QtWidgets.QTableWidget(Form)
        self.head_table.setMaximumSize(QtCore.QSize(16777215, 50))
        self.head_table.setObjectName("head_table")
        self.head_table.setColumnCount(0)
        self.head_table.setRowCount(0)
        self.head_table.horizontalHeader().setVisible(False)
        self.head_table.horizontalHeader().setHighlightSections(False)
        self.head_table.verticalHeader().setVisible(False)
        self.head_table.verticalHeader().setHighlightSections(False)
        self.verticalLayout.addWidget(self.head_table)
        self.message_box = QtWebKitWidgets.QWebView(Form)
        self.message_box.setUrl(QtCore.QUrl("about:blank"))
        self.message_box.setObjectName("message_box")
        self.verticalLayout.addWidget(self.message_box)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message_text = QtWidgets.QPlainTextEdit(Form)
        self.message_text.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.message_text.setFont(font)
        self.message_text.setObjectName("message_text")
        self.horizontalLayout.addWidget(self.message_text)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.send_button = QtWidgets.QPushButton(Form)
        self.send_button.setMinimumSize(QtCore.QSize(100, 0))
        self.send_button.setMaximumSize(QtCore.QSize(100, 50))
        self.send_button.setObjectName("send_button")
        self.horizontalLayout.addWidget(self.send_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.message_text.setPlaceholderText(_translate("Form", "Type Your Message Here"))
        self.send_button.setText(_translate("Form", "Send"))

from PyQt5 import QtWebKitWidgets
