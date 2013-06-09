from django.http import HttpResponse, HttpResponseRedirect  # ?
from django.contrib.auth import authenticate, login, logout
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render_to_response, get_object_or_404, redirect  # ?
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import json, re, datetime, csv, random
from collections import defaultdict

from django.contrib.auth.models import User
from django.conf import settings  # ?
from django.db import connections
from bson.objectid import ObjectId
from bson.code import Code
from pymongo.errors import InvalidId

from cvm_app.views import helpers

@helpers.uses_mongo
def query_count(request, mongo):
    start_time = datetime.datetime.utcnow()

    batch_id = request.POST["batch_id"]
    query_word = request.POST["query_word"]
    batch = mongo.get_collection("cvm_batch").find_one({"_id": ObjectId(batch_id)})

    if not batch:
        return helpers.gen_json_response({"status": "failed", "msg": "Invalid batch_id."})
    if not query_word:
        return helpers.gen_json_response({"status": "failed", "msg": "No query_word found."})
        
    yes_count = 0
    no_count = 0

    for doc in batch["documents"]:
        collection_id = doc["collection_id"]
        collection_index = doc["collection_index"]

        collection = mongo.get_collection("cvm_collection").find_one({"_id": ObjectId(collection_id)})
        collection_content = collection["documents"][collection_index]["content"]

        if re.search( query_word, collection_content ):
            yes_count = yes_count + 1
        else:
            no_count = no_count + 1
 
#    end_time = datetime.datetime.utcnow()

    print "yes_count is ", yes_count
    print "no_count is ", no_count

    return helpers.gen_json_response({
        'status': "success",
        'msg': "Successfully finished the query-count",
        'query': {
            'query_type': "query-count",
            'batch_id': batch_id,
            'query_word': query_word,
            'query_started_at': start_time,
            'query_finished_at' : datetime.datetime.utcnow(),
        },
        'result': {
            'yes_count' : yes_count,
            'no_count': no_count,
        }
    })


@helpers.uses_mongo
def mapreduce_query(request, mongo):
    #Unpack request parameters
    #Authenticate user
    #Construct mongo query
    map_func = Code("""
function() {
    date = ISODate(this.metadata.timestamp)

//    group = date; //by day
//    group = new Date( date.getFullYear(), date.getMonth(), 1, 0, 0, 0, 0) }; //by month
    group = new Date( date.getFullYear(), 0, 1, 0, 0, 0, 0) }; //by year
    emit( group, {avg : this.civility_labels.divisiveness.score, count: 1} )
};
    """)

    reduce_func = Code("""
function(key, values) {
   var sum = 0;
   var count = 0;
   values.forEach(function(doc) {
     sum += doc.avg * doc.count;
     count += doc.count;
   });
   return {avg: sum/count, n: count};
};
    """)

    #Execute mongo query
    mr_result = mongo.get_collection("cvm_document").inline_map_reduce(map_func, reduce_func)
    
    result = {
        "status" : "success",
        "results" : mr_result,
    }

    #Unpack result
    return helpers.gen_json_response(result)


