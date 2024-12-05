from datetime import datetime

from bson import json_util
from django.conf import settings
from elasticsearch import Elasticsearch

from core.celery import APP

from pykolofinance.audtilog.mongo_connector import get_database

database = get_database()
app_name = settings.APP_NAME.lower()
db_name = settings.MONGODB_LOGGER_DATABASE
collection_name = database[db_name]


@APP.task()
def send_logs_to_logger(data):
    inserted_id = collection_name.insert_one(data).inserted_id
    # elastic_search = Elasticsearch(hosts=settings.MONGODB_LOGGER_URL)
    # result = elastic_search.index(index=settings.APP_NAME.lower(), body=data)
    return {
        'entry': str(inserted_id),
        'app_name': app_name,
        'db_name': db_name,
        'timestamp': str(datetime.now()),
    }


@APP.task()
def send_log_to_auditlogger(data):
    pass
