# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainapp.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(895, 716)
        MainWindow.setStyleSheet("background:#F6F6F6")
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.contact_frame = QtWidgets.QFrame(self.central_widget)
        self.contact_frame.setMinimumSize(QtCore.QSize(200, 0))
        self.contact_frame.setMaximumSize(QtCore.QSize(250, 16777215))
        self.contact_frame.setAutoFillBackground(False)
        self.contact_frame.setStyleSheet("QFrame#menuFrame {\n"
"    background : qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(174, 174, 174, 255))\n"
"}")
        self.contact_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.contact_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.contact_frame.setObjectName("contact_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.contact_frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.contact_table = QtWidgets.QTableWidget(self.contact_frame)
        self.contact_table.setAutoFillBackground(False)
        self.contact_table.setStyleSheet("QTableWidget#contactTable {background :#E8E8E8}")
        self.contact_table.setLineWidth(0)
        self.contact_table.setAutoScrollMargin(16)
        self.contact_table.setShowGrid(True)
        self.contact_table.setGridStyle(QtCore.Qt.DashLine)
        self.contact_table.setObjectName("contact_table")
        self.contact_table.setColumnCount(0)
        self.contact_table.setRowCount(0)
        self.contact_table.horizontalHeader().setVisible(False)
        self.contact_table.horizontalHeader().setHighlightSections(False)
        self.contact_table.verticalHeader().setVisible(False)
        self.contact_table.verticalHeader().setHighlightSections(False)
        self.verticalLayout.addWidget(self.contact_table)
        self.horizontalLayout.addWidget(self.contact_frame)
        self.message_frame = QtWidgets.QFrame(self.central_widget)
        self.message_frame.setStyleSheet("QFrame#contentFrame {\n"
"    background : qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(174, 174, 174, 255), stop:1 rgba(255, 255, 255, 255))\n"
"}")
        self.message_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.message_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.message_frame.setObjectName("message_frame")
        self.horizontalLayout.addWidget(self.message_frame)
        MainWindow.setCentralWidget(self.central_widget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet("QStatusBar {\n"
"    border-top : 1px solid #AEAEAE;\n"
"}")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionText = QtWidgets.QAction(MainWindow)
        self.actionText.setObjectName("actionText")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Whatsdesk"))
        self.actionText.setText(_translate("MainWindow", "Text"))

