from decouple import config
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

from . import Singleton, classproperty


def db_connect():
    return create_engine(config('DATABASE_URI', 'sqlite:///:memory:'))


class Model:
    @classmethod
    def create_all(cls):
        cls.metadata.create_all(cls.session.bind)

    def flush(self):
        self.save().flush()

    @classmethod
    def get(cls, *args, **kwargs) -> 'Model':
        return cls.session.get(cls, *args, **kwargs)

    @classmethod
    def query(cls, *entities, **kwargs) -> Query:
        return cls.session.query(cls, *entities, **kwargs)

    def save(self):
        self.session.add(self)
        return self.session

    @classproperty
    def session(cls):
        return SessionManager().session

    @classmethod
    def where(cls, *criterion) -> Query:
        return cls.query().where(*criterion)


Model = declarative_base(cls=Model)


class SessionManager(metaclass=Singleton):
    def __init__(self):
        self._session = None

    @property
    def session(self):
        session: Session = self._session
        if session:
            if session.is_active:
                return session
            session.close()
        self._engine = db_connect()
        session = sessionmaker(bind=self._engine)()
        self._session = session
        return session

    def __del__(self):
        if self._engine:
            self._engine.dispose()
        if self._session:
            self._session.close()
            self._session = None
