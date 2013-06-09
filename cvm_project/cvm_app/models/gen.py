"""
Generator functions that return json for most DB objects 

    Style guide for cvm_app.models.gen:
    * Object structures only
    * Method names correspond with mongo collections (or subobjects)
    * No logic
    * No DB writes (no @uses_mongo)
    
    This module basically contains the database spec.
"""

from bson.objectid import ObjectId
import datetime

from cvm_app.models import helpers
import cvm_app.models.logic
import cvm_app.models as models


def collection(name, description, doc_ids):
    J = {
        'profile' : {
            'name' : name,
            'description' : description,
            'created_at' : datetime.datetime.now(),
            'size' : len(doc_ids),
        },
        'doc_ids' : doc_ids,
    }
    
    return J

#! This should be accept content and metadata as arguments
def document(document):
    J = {
        "content": document["content"],
        "metadata": document["metadata"],
        'civility_labels' : {
            "codebook_id" : {
                "score": 0,
                "uncertainty": 0.0,
                "last_updated": "",
                "method": "",
            }
        }
    }

    return J

#! Used to be called: get_new_user_json
#! Need to change all refs to cvm_user_profile
# The user_profile collection 
def user_profile(user_name, lane_seed):
    return {
        'profile' : {
            'user_name' : user_name,
            'lane_seed' : lane_seed,
            'created_at' : datetime.datetime.now(),
        },
    }

# Formerly: get_new_game_session_json
#! This shouldn't have uses_mongo.  Needs to be split into two functions.
#from cvm_app.models.helpers import uses_mongo
#@uses_mongo
def game_session(batch_id, user, tasks_remaining, lane):

    return {
        'user': user,
        'batch_id': ObjectId(batch_id),
        'game_stats': {
            'total_score': 0.,
            'avg_score': 0.,
            'tasks_completed': 0,
            'bonus_credits': 0,
            'scored_tasks' : 0,
            'tasks_remaining': tasks_remaining,
        },
        'lane': lane,
    }
