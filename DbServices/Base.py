__author__ = 'Raj'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Base:
    session = scoped_session(sessionmaker())
    base = declarative_base()

    def init(self, dbname='sqlite:///whatsdesk.db', clear=False):
        engine = create_engine(dbname, echo=False)
        self.session.remove()
        if clear:
            self.base.metadata.drop_all(engine)
        self.session.configure(bind=engine, autoflush=False, expire_on_commit=False)
        self.base.metadata.create_all(engine)
        return engine
