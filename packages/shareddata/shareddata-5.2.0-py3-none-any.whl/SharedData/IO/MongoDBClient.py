import os

from pymongo import MongoClient, errors
from pymongo import ASCENDING, DESCENDING

class MongoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            mongodb_conn_str = (f'mongodb://{os.environ["MONGODB_USER"]}:'
                                f'{os.environ["MONGODB_PWD"]}@'
                                f'{os.environ["MONGODB_HOST"]}:'
                                f'{os.environ["MONGODB_PORT"]}/')
            cls._instance.client = MongoClient(mongodb_conn_str)
        return cls._instance

    def __getitem__(self, collection_name):
        return self._client['SharedData'][collection_name]

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value    