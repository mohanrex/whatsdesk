__author__ = 'Raj'

from Controller.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.setApplicationName("Whatsdesk")
    app.setApplicationDisplayName("Whatsdesk")
    print("App Started")
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
