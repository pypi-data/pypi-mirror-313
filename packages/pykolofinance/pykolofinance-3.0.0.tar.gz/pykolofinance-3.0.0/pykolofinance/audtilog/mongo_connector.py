from django.conf import settings
from pymongo import MongoClient


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # db_url = "mongodb://phlox:6GlbaXu0sJWUG@143.110.171.18:27017/PhloxLogDatabase?authSource=admin"
    db_url = settings.MONGODB_LOGGER_URL

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(db_url)
    database = settings.MONGODB_LOGGER_DATABASE
    # database = settings.APP_NAME.lower()

    return client[database]
