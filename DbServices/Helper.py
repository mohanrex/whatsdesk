__author__ = 'Raj'

from sqlalchemy import or_, select, and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from DbServices.Tables import *
from DbServices.Base import Base


class Helper:
    def __init__(self):
        self._db_base = Base()
        self.engine = self._db_base.init(clear=False)

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
                    ""
                ])
                return
            except MultipleResultsFound:
                return
        else:
            return

    def get_all_contact(self):
        sql = "select contact.id, contact.name, " \
              "(select count(message.id) from message " \
              "where message.from_id = contact.id) from contact " \
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
            'lastSeen'
        ]
        fields = dict(zip(field_name, values))
        self.add_query('Contact', fields)

    def add_query(self, model, values):
        sess = self._db_base.session()
        model = globals()[model]
        model = model()
        for name, value in values.items():
            setattr(model, name, value)
        sess.add(model)
        sess.commit()
        sess.close()
