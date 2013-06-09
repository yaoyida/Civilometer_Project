"""
Small helper functions to make working with models easier
"""

from django.db import connections
from bson.objectid import ObjectId
from pymongo.errors import InvalidId
import json

from cvm_app.algorithms.jenkins import hashlittle

def uses_mongo(function):
    def _inner(*args, **kwargs):
        mongo = connections["default"]
        return function(mongo, *args, **kwargs)
    return _inner

class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def random_lane_number_generator(seed_id, replication):
    seed = 0xdeadbeef
    h = hashlittle(seed_id, seed)

    lane = h % replication
    return lane
