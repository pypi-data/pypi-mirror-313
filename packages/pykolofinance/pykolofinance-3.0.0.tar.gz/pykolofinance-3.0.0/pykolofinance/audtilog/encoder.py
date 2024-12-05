import json
from datetime import datetime

from bson import ObjectId


# class JSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, ObjectId):
#             return str(obj)  # Convert ObjectId to string
#         return super(JSONEncoder, self).default(obj)

class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO format string
        # Use the default method for other types
        return super().default(obj)
