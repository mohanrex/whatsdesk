__author__ = 'Raj'

from PyQt5.Qt import QWidget, QPixmap
from resources import resource_rc
from View import contactrow_ui


class ContactRow(QWidget, contactrow_ui.Ui_Form):
    def __init__(self, record):
        QWidget.__init__(self)
        self.setupUi(self)
        self.name_label.setText(record[1])
        self.new_msg_label.setText(str(record[2]))
        self.status__msg_label.setText(record[3])
        if int(record[5]) == 10:
            self.available_label.setPixmap(QPixmap(':/status_icon/user_offline.png'))
        else:
            self.available_label.setPixmap(QPixmap(':/status_icon/user_online.png'))
