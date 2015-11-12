__author__ = 'Raj'


from PyQt5.QtCore import QThread
import time
import logging

from yowsup.stacks import YowStackBuilder
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import AuthError
from yowsup.layers.network import YowNetworkLayer

from YowsupHelper.Interfacer import Interfacer


class YowsupThread(QThread):
    def __init__(self, phone, password, parent=None, debug=False):
        QThread.__init__(self, parent)
        self.exiting = False
        self.interface = Interfacer()
        if debug:
            logging.basicConfig(level=logging.DEBUG)

        stack_builder = YowStackBuilder()

        self.stack = stack_builder\
            .pushDefaultLayers(True)\
            .push(self.interface)\
            .build()
        self.stack.setCredentials([phone, password])

    def __del__(self):
        print("Thread Deleted")
        self.exiting = True
        self.wait()

    def render(self):
        print("Thread Initiated")
        self.start()

    def run(self):
        time.sleep(5)
        print("Thread Started")
        count = 0
        while count < 100:
            self.run_loop()
            count += 1

    def run_loop(self):
        time.sleep(5)
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e)
        print("Thread Restarting")
