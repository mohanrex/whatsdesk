__author__ = 'Raj'

from DbServices.Helper import Helper
import threading, os
from PyQt5.QtCore import QThread, pyqtSignal

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_groups.protocolentities import *
from yowsup.layers.protocol_messages.protocolentities import *
from yowsup.layers.protocol_profiles.protocolentities import *
from yowsup.layers.protocol_presence.protocolentities import *
from yowsup.layers.protocol_contacts.protocolentities import *


class Interfacer(QThread, YowInterfaceLayer):

    # -------------------------- PY QT Signals -------------------------------------------- #
    message_received_signal = pyqtSignal()
    success_connection_signal = pyqtSignal()
    presence_update_signal = pyqtSignal()

    # -------------------------- Class Constructor -------------------------------------------- #
    def __init__(self):
        super(Interfacer, self).__init__()
        self.ackQueue = []
        self.send_receipts = True
        self.lock = threading.Condition()
        self.services = Helper()

    # -------------------------- Forward operations functions -------------------------------------------- #
    def send_message(self, phone, message):
        self.lock.acquire()
        if '@' in phone:
            entity = TextMessageProtocolEntity(message, to=phone)
        elif '-' in phone:
            entity = TextMessageProtocolEntity(message, to="%s@g.us" % phone)
        else:
            entity = TextMessageProtocolEntity(message, to="%s@s.whatsapp.net" % phone)
        self.ackQueue.append(entity.getId())
        self.toLower(entity)
        self.services.add_message([
            entity.getId(),
            entity.getBody(),
            self.services.get_contact_id(entity.getTo(), "Unknown", entity.isGroupMessage()),
            entity.getTo(),
            entity.getNotify(),
            self.services.get_contact_id(entity.getParticipant(), "Unknown"),
            entity.isOutgoing(),
            entity.isGroupMessage(),
            '0',
            entity.getTimestamp(),
            '20'
        ])
        self.message_received_signal.emit()
        self.lock.release()
        print(entity)

    def on_text_message(self, entity):
        if entity.isGroupMessage() == 0 and self.services.check_contact_id(entity.getFrom()):
            self.presence_subscribe(entity.getFrom())
        elif entity.isGroupMessage() == 1 and self.services.check_contact_id(entity.getParticipant()):
            self.presence_subscribe(entity.getParticipant())

        self.services.add_message([
            entity.getId(),
            entity.getBody(),
            self.services.get_contact_id(entity.getFrom(), entity.getNotify(), entity.isGroupMessage()),
            entity.getTo(),
            entity.getNotify(),
            self.services.get_contact_id(entity.getParticipant(), entity.getNotify()),
            entity.isOutgoing(),
            entity.isGroupMessage(),
            '0',
            entity.getTimestamp(),
            '10'
        ])
        self.message_received_signal.emit()
        print("Message from %s" % (entity.getFrom(False)))

    def get_group_info(self, group_jid):
        def on_success(success_entity, original_entity):
            print(success_entity)

        def on_error(error_entity, original_entity):
            print(error_entity)
            print(original_entity)
        entity = InfoGroupsIqProtocolEntity(group_jid)
        success = lambda success_entity, original_entity: on_success(success_entity, original_entity)
        error = lambda error_entity, original_entity: on_error(error_entity, original_entity)
        self._sendIq(entity, success, error)

    def contact_picture(self, jid):
        entity = GetPictureIqProtocolEntity(jid, preview=True)
        self._sendIq(entity, self.contact_image_result)

    @staticmethod
    def contact_image_result(success_entity, original_entity):
        success_entity.writeToFile("../tmp/images/%s_%s.jpg" % (
            original_entity.getTo(),
            "preview" if success_entity.isPreview() else "full")
        )

    def groups_list(self):
        def on_success(success_entity, original_entity):
            for group in success_entity.getGroups():
                self.services.update_contact_id(group.getId()+"@g.us", group.getSubject())
                # self.contact_picture(group.getId+"@g.us")
            self.success_connection_signal.emit()

        def on_error(error_entity, original_entity):
            print(error_entity)
            print(original_entity)

        entity = ListGroupsIqProtocolEntity()
        success = lambda success_entity, original_entity: on_success(success_entity, original_entity)
        error = lambda error_entity, original_entity: on_error(error_entity, original_entity)
        self._sendIq(entity, success, error)

    def on_media_message(self, entity):
        """ if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" %
        ssageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" %
        (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
        """
        print(entity)

    def set_presence_available(self):
        entity = AvailablePresenceProtocolEntity()
        self.toLower(entity)

    def presence_name(self, name):
        entity = PresenceProtocolEntity(name=name)
        self.toLower(entity)

    def presence_unavailable(self):
        entity = UnavailablePresenceProtocolEntity()
        self.toLower(entity)

    def presence_subscribe(self, jid):
        entity = SubscribePresenceProtocolEntity(jid)
        self.toLower(entity)

    def contact_lastseen(self, jid):
        def onSuccess(resultIqEntity, originalIqEntity):
            print("%s lastseen %s seconds ago" % (resultIqEntity.getFrom(), resultIqEntity.getSeconds()))

        def onError(errorIqEntity, originalIqEntity):
            print("Error getting lastseen information for %s" % originalIqEntity.getTo())

        entity = LastseenIqProtocolEntity(jid)
        self._sendIq(entity, onSuccess, onError)

    def contacts_sync(self, contacts):
        entity = GetSyncIqProtocolEntity(contacts.split(','))
        self.toLower(entity)

    # -------------------------- Callback functions for each functions -------------------------------------------- #
    @ProtocolEntityCallback("success")
    def on_success(self, entity):
        print("Success Connected")
        self.set_presence_available()
        self.groups_list()

    @ProtocolEntityCallback("ack")
    def on_ack(self, entity):
        self.lock.acquire()
        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))
        self.lock.release()

    @ProtocolEntityCallback("chatstate")
    def on_chatstate(self, entity):
        print(entity)

    @ProtocolEntityCallback("iq")
    def on_iq(self, entity):
        print(entity)

    @ProtocolEntityCallback("message")
    def on_message(self, entity):
        print(entity)
        if entity.getType() == 'text':
            self.on_text_message(entity)
        elif entity.getType() == 'media':
            self.on_media_message(entity)
        self.toLower(entity.ack())
        self.toLower(entity.ack(True))

    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        self.toLower(entity.ack())

    @ProtocolEntityCallback("notification")
    def on_notification(self, notification):
        notification_data = notification.__str__()
        if notification_data:
            print(notification_data)
        else:
            print("From :%s, Type: %s" % (self.jidToAlias(notification.getFrom()), notification.getType()))
        self.toLower(notification.ack())

    @ProtocolEntityCallback("presence")
    def on_presence_update(self, entity):
        self.services.updatePresence(entity.getFrom(), entity.getType(), entity.getLast())
        self.presence_update_signal.emit()
