from pymongo import MongoClient
from pymongo.database import Database
import os

_client: MongoClient = None
_db: Database = None


def get_database() -> Database:
    global _client, _db
    if _db is None:
        mongo_uri = os.getenv("MONGODB_URI")
        _client = MongoClient(mongo_uri)
        _db = _client.get_default_database()
    return _db