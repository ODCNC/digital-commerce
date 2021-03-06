import hashlib
from typing import Dict

from bson.objectid import ObjectId
from decouple import config
from pymongo import MongoClient

from . import *

MongoClient.HOST = config('MONGO_URI', 'localhost')


def str2oid(text: str):
    assert text
    oid = hashlib.md5(text.encode('utf-8')).hexdigest()[:24]
    return ObjectId(oid)


class Document(Dict):
    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.get(name)


class MongoManager(metaclass=Singleton):
    def __init__(self, **kwargs):
        self._client = None
        self.kwargs = kwargs
        kwargs.setdefault('document_class', Document)

    @property
    def client(self):
        client: MongoClient = self._client
        try:
            if client and client.is_mongos:
                return client
        except:
            client.close()
        client = MongoClient(**self.kwargs)
        self._client = client
        return client

    def __del__(self):
        if self._client:
            self._client.close()
            self._client = None
