__author__ = 'Raj'

from View import message_ui
from PyQt5.Qt import QWidget
from DbServices.Helper import Helper


class Messager(QWidget, message_ui.Ui_Form):
    def __init__(self, current_id, thread):
        QWidget.__init__(self)
        self.setupUi(self)
        self.thread = thread
        self.db = Helper()
        self.toJid = self.db.get_jid_of_id(current_id)
        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        message = self.message_text.toPlainText()
        if self.validate_message(message):
            self.thread.interface.send_message()

    def validate_message(self, message=''):
        if message != '':
            return True
        else:
            return False
