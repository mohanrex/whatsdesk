__author__ = 'Raj'

from PyQt5.Qt import QWidget

from View import contactrow_ui


class ContactRow(QWidget, contactrow_ui.Ui_Form):
    def __init__(self, record):
        QWidget.__init__(self)
        self.setupUi(self)
        self.name_label.setText(record[1])
        self.new_msg_label.setText(str(record[2]))
