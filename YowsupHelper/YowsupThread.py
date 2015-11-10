__author__ = 'Raj'


from PyQt5.QtCore import QThread
import time
import logging

from yowsup.stacks import YowStack
from yowsup.layers import YowLayerEvent
from yowsup.layers.protocol_groups import YowGroupsProtocolLayer
from yowsup.layers.auth import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_media import YowMediaProtocolLayer
from yowsup.layers.stanzaregulator import YowStanzaRegulator
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.logger import YowLoggerLayer
from yowsup.layers.protocol_iq import YowIqProtocolLayer
from yowsup.layers.protocol_calls import YowCallsProtocolLayer
from yowsup.layers.axolotl import YowAxolotlLayer

from YowsupHelper.Interfacer import Interfacer


class YowsupThread(QThread):
    def __init__(self, parent=None, debug=False):
        QThread.__init__(self, parent)
        self.exiting = False
        self.interface = Interfacer()
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        layers = (
            self.interface,
            (
                YowAuthenticationProtocolLayer,
                YowMessagesProtocolLayer,
                YowReceiptProtocolLayer,
                YowAckProtocolLayer,
                YowMediaProtocolLayer,
                YowIqProtocolLayer,
                YowCallsProtocolLayer,
                YowGroupsProtocolLayer
            ),
            YowAxolotlLayer,
            YowLoggerLayer,
            YowCoderLayer,
            YowCryptLayer,
            YowStanzaRegulator,
            YowNetworkLayer
        )
        self.stack = YowStack(layers)

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
