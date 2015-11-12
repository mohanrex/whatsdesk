__author__ = 'Raj'

from sqlalchemy import or_, select, and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from DbServices.Tables import *
from DbServices.Base import Base


class Helper:
    def __init__(self):
        """
        Initialization
        """
        self._db_base = Base()
        self.engine = self._db_base.init(clear=False)

    # -------------------------- Message db operation -------------------------------------------- #
    def add_message(self, values):
        field_name = [
            'message_id',
            'body',
            'from_id',
            'to_id',
            'notify',
            'participant_id',
            'is_out',
            'is_group',
            'is_media',
            'timestamp',
            'status'
        ]
        fields = dict(zip(field_name, values))
        self.add_query('Message', fields)

    def get_all_messages(self, current_id):
        sql = "select * from message left join contact on contact.id = message.participant_id where message.from_id = "+current_id
        count_sql = "select count(id) from message where from_id = "+current_id
        records = self.engine.execute(sql)
        count = self.engine.execute(count_sql).scalar()
        return {'records': records, 'count': count}

    def set_read(self, current_id):
        sql = "update message set status = 20 where from_id = "+current_id
        self.engine.execute(sql)

    # -------------------------- Profile db operation -------------------------------------------- #
    def get_credentials(self):
        sess = self._db_base.session()
        record = sess.query(Profile).first()
        sess.close()
        if record:
            return {'phone_number': str(record.country_code)+str(record.phone_number), 'password': record.password}
        else:
            return None

    # -------------------------- Contact db operation -------------------------------------------- #
    def get_jid_of_id(self, idx):
        sess = self._db_base.session()
        try:
            record = sess.query(Contact).filter_by(id=idx).one()
            sess.close()
            return record.jid
        except NoResultFound:
            return
        except MultipleResultsFound:
            record = sess.query(Contact).filter_by(id=idx).first()
            sess.close()
            return record.jid

    def updatePresence(self, jid, available=None, last=None):
        sess = self._db_base.session()
        try:
            record = sess.query(Contact).filter_by(jid=jid).one()
            record.is_online = "20" if available is None else "10"
            record.last_seen = record.last_seen if last is None else last
            sess.commit()
            sess.close()
        except NoResultFound:
            return
        except MultipleResultsFound:
            record = sess.query(Contact).filter_by(jid=jid).first()
            record.is_online = "20" if available is None else "10"
            record.last_seen = record.last_seen if last is None else last
            sess.commit()
            sess.close()
            return

    def get_contact_id(self, jid, notify, is_group=0):
        sess = self._db_base.session()
        if jid:
            try:
                record = sess.query(Contact).filter_by(jid=jid).one()
                sess.close()
                return record.id
            except NoResultFound:
                sess.close()
                self.add_contact([
                    jid,
                    notify,
                    "",
                    "",
                    "",
                    is_group,
                    10,
                    ""
                ])
                return self.get_contact_id(jid, notify)
            except MultipleResultsFound:
                record = sess.query(Contact).filter_by(jid=jid).first()
                sess.close()
                return record.id
        else:
            return jid

    def update_contact_id(self, jid, name):
        sess = self._db_base.session()
        if jid:
            try:
                record = sess.query(Contact).filter_by(jid=jid).one()
                record.name = name
                sess.commit()
                sess.close()
                return
            except NoResultFound:
                self.add_contact([
                    jid,
                    name,
                    "",
                    "",
                    "",
                    1,
                    10,
                    ""
                ])
                return
            except MultipleResultsFound:
                return
        else:
            return

    def check_contact_id(self, jid):
        sess = self._db_base.session()
        if jid:
            try:
                record = sess.query(Contact).filter_by(jid=jid).one()
                sess.close()
                return True
            except NoResultFound:
                sess.close()
                return False
            except MultipleResultsFound:
                record = sess.query(Contact).filter_by(jid=jid).first()
                sess.close()
                return True
        else:
            return False

    def get_contact_group(self, group=False):
        sql = "select id, jid from contact where is_group = 0"
        records = self.engine.execute(sql)
        return records

    def get_all_contact(self):
        sql = "select contact.id, contact.name, " \
              "(select count(message.id) from message " \
              "where message.from_id = contact.id and message.status = 10), " \
              "contact.status_message, contact.is_group, contact.is_online from contact " \
              "left join message as msg on msg.from_id = contact.id " \
              "group by contact.id order by msg.timestamp desc"
        count_sql = "select count(id) from contact"
        records = self.engine.execute(sql)
        count = self.engine.execute(count_sql).scalar()
        return {'records': records, 'count': count}

    def add_contact(self, values):
        field_name = [
            'jid',
            'name',
            'contact_image',
            'status_message',
            'status',
            'is_group',
            'is_online',
            'lastSeen'
        ]
        fields = dict(zip(field_name, values))
        self.add_query('Contact', fields)

    # -------------------------- Base db operation -------------------------------------------- #
    def add_query(self, model, values):
        sess = self._db_base.session()
        model = globals()[model]
        model = model()
        for name, value in values.items():
            setattr(model, name, value)
        sess.add(model)
        sess.commit()
        sess.close()
