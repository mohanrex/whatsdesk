__author__ = 'Raj'

from View import message_ui
from PyQt5.Qt import QWidget
from PyQt5.QtCore import pyqtSignal
from DbServices.Helper import Helper


class Messager(QWidget, message_ui.Ui_Form):
    message_received_signal = pyqtSignal()

    def __init__(self, current_id, thread):
        QWidget.__init__(self)
        self.setupUi(self)
        self.thread = thread
        self.db = Helper()
        self.current_id = current_id
        self.toJid = self.db.get_jid_of_id(self.current_id)
        self.send_button.clicked.connect(self.send_message)
        self.message_box.page().mainFrame().contentsSizeChanged.connect(self.scroll_to_bottom)
        self.thread.interface.message_received_signal.connect(self.on_success)
        self.message_text.setFocus()
        self.update_message_table()
        self.message_received_signal.emit()

    def scroll_to_bottom(self):
        self.message_box.page().mainFrame().scroll(
            self.message_box.page().mainFrame().contentsSize().width(),
            self.message_box.page().mainFrame().contentsSize().height()
        )

    def send_message(self):
        message = self.message_text.toPlainText()
        if self.validate_message(message):
            self.thread.interface.send_message(self.toJid, message)
            self.message_text.setPlainText("")
            self.message_text.setFocus()

    def on_success(self):
        self.update_message_table()

    @staticmethod
    def validate_message(message=''):
        if len(message) > 0:
            return True
        else:
            return False

    def update_message_table(self):
        result = self.db.get_all_messages(self.current_id)
        html_string = '<style type="text/css">' \
                      'p {margin:0px;} p.head-left {color:#990100;text-align: left;margin-bottom: 5px;}' \
                      'p.message {clear:both;padding:5px 20px} p.footer-right {text-align: right;color:#390504;margin-top:10px;font-size: 12px;}' \
                      'div.left, div.right {background-color:#FFFFFF;color:#333333;border:1px solid #E8E8E8;padding:5px;' \
                      'border-radius: 10px;margin-bottom:10px;display:inline-block;}' \
                      'div.right {clear:both;border-top-right-radius: 0px;margin-left:100px;float:right;}' \
                      'div.left {clear:both;margin-right:100px;border-top-left-radius: 0px;float:left;}' \
                      '</style><div style="background-color:#F6F6F6">'
        for idx, record in enumerate(result['records']):
            html_string = html_string + self.generate_message_row(record)
        self.message_box.setHtml(html_string+'</div>')
        self.db.set_read(self.current_id)
        self.message_received_signal.emit()

    @staticmethod
    def generate_message_row(record):
        message_string = '<div class="{}"><p class="head-left">{}</p>' \
                         '<p class="message">{}</p><p class="footer-right">{}</p></div><br />'
        if int(record[7]) == 0:
            orientation = "left"
            name = ""
            status = ""
            if int(record[8]) == 1:
                name = str(record[14])
        else:
            orientation = "right"
            name = ""
            status = "R"
        message = str(record[2]).replace('\n', '<br />')
        return message_string.format(orientation, name, message, status)
