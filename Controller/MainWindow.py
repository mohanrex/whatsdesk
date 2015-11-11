__author__ = 'Raj'

from PyQt5.Qt import QMainWindow, QHeaderView, QAbstractItemView, QTableView, QTableWidgetItem
from PyQt5 import QtWidgets
from DbServices.Helper import Helper
from View import mainapp_ui
from Controller.ContactRow import ContactRow
from Controller.Messager import Messager
from YowsupHelper.YowsupThread import YowsupThread


class MainWindow(QMainWindow, mainapp_ui.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.db = Helper()
        self.credentials = self.db.get_credentials()
        self.setupUi(self)
        if self.credentials:
            self.form_widget = None
            self.frame_layout = QtWidgets.QVBoxLayout(self.message_frame)
            self.message_frame.setContentsMargins(0, 0, 0, 0)
            self.thread = YowsupThread(self.credentials['phone_number'], self.credentials['password'], debug=False)
            self.thread.interface.success_connection_signal.connect(self.on_success)
            self.thread.interface.message_received_signal.connect(self.on_success)
            self.contact_table.clicked.connect(self.render_page)
            self.thread.render()
        else:
            print("You need to provide authentication credentials")

    def render_page(self, index):
        row = index.row()
        self.form_widget = Messager(index.sibling(row, 1).data(), self.thread)
        self.form_widget.message_received_signal.connect(self.on_success)
        for i in reversed(range(self.frame_layout.count())):
            self.frame_layout.itemAt(i).widget().setParent(None)
        self.frame_layout.addWidget(self.form_widget)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.message_frame.setLayout(self.frame_layout)
        self.update_contact_table()

    def on_success(self):
        self.update_contact_table(True)
        pass

    def update_contact_table(self, init=False):
        if init:
            self.initialize()
        result = self.db.get_all_contact()
        self.contact_table.setRowCount(result['count'])
        for idx, record in enumerate(result['records']):
            form_widget = ContactRow(record)
            self.contact_table.setItem(idx, 1, QTableWidgetItem(str(record[0])))
            self.contact_table.setCellWidget(idx, 0, form_widget)
        return

    def initialize(self):
        self.contact_table.setColumnCount(2)
        self.contact_table.setColumnHidden(1, True)
        self.contact_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contact_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.contact_table.setSelectionBehavior(QTableView.SelectRows)
        self.contact_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.contact_table.verticalHeader().setVisible(False)
        self.contact_table.horizontalHeader().setVisible(False)
        self.contact_table.verticalHeader().setDefaultSectionSize(68)
