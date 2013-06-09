from django.http import HttpResponse, HttpResponseRedirect  # ?
from django.contrib.auth import authenticate, login, logout
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render_to_response, get_object_or_404, redirect  # ?
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import json, re, datetime, csv
from collections import defaultdict

from django.contrib.auth.models import User
from django.conf import settings  # ?
from django.db import connections
from bson.objectid import ObjectId
from pymongo.errors import InvalidId


from django.core.exceptions import PermissionDenied
from cvm_app import models

def jsonifyRecord(obj, fields):
    j = {}
    for f in fields:
        j[f] = obj.__dict__[f]
    return j


def jsonifyRecords(objs, fields):
    j = []
    for o in objs:
        j.append(jsonifyRecord(o, fields))
    return j


class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def gen_json_response(result):
    return HttpResponse(json.dumps(result, indent=2, cls=MongoEncoder), mimetype='application/json')

def sluggify(string):
    ustring = unicode.decode(string).lower()
    return re.sub(r'\W+','-',ustring)

def admin_required(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner

def uses_mongo(function):
    def _inner(request, *args, **kwargs):
        mongo = connections["default"]
        return function(request, mongo, *args, **kwargs)
    return _inner
