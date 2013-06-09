#! Need to remove unused headers
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

import cvm_app.models.gen
import cvm_app.models as models

from cvm_app.views import helpers
import random, string

@helpers.uses_mongo
def choose_task(request, mongo):
    #print "=== GET Parameters ==="
    #print '\n'.join([ "\t"+k+"\t"+request.GET[k] for k in request.GET])

    #Identify user type
    if request.user.is_anonymous():
        user_type = "anonymous"
    else:
        user_type = "member"

    #Retrieve batches and construct result object
    result = {
        'user_type': user_type,
        'batches': list(mongo.get_collection("cvm_batch").find(fields={"profile": 1, "reports": 1}, sort=[('created_at', 1)])),
    }

    #Render template
    return render_to_response('tasks/choose-task.html', result, context_instance=RequestContext(request))

@helpers.uses_mongo
def task(request, mongo, game_session_id):
    #Retrieve game session based on id
    #! Need error handling for bad ids
    game_session = mongo.get_collection("cvm_game_session").find_one({"_id": ObjectId(game_session_id)})

    #! If the user is logged in, we should make sure the game session belongs to the same user

    #Retrieve the batch from game_session
    batch_id = game_session["batch_id"]
    batch = mongo.get_collection("cvm_batch").find_one(
        {"_id": ObjectId(batch_id)},
        {"profile": 1, "documents": 1}
    )
    #docs = batch["documents"]

    #Retrieve the codebook from the batch
    codebook = mongo.get_collection("cvm_codebook").find_one({"_id": batch["profile"]["codebook_id"]})

    #Construct result object
    result = {'batch': batch, 'codebook': codebook, 'game_session': game_session}

    #!!! This is a temporary hack to edit the mturk task page
    return render_to_response('tasks/mturk-user-task.html', result, context_instance=RequestContext(request))

    #Render the appropriate template
#    if game_session["user"]["user_type"] == "mturk":
#        return render_to_response('tasks/mturk-user-task.html', result, context_instance=RequestContext(request))
        
#    elif game_session["user"]["user_type"] == "member":
    if game_session["user"]["user_type"] == "member":
        return render_to_response('tasks/cvm-user-task.html', result, context_instance=RequestContext(request))
        
    elif game_session["user"]["user_type"] == "anonymous":
        #! Eventually, anonymous users will probably get their own template
        return render_to_response('tasks/cvm-user-task.html', result, context_instance=RequestContext(request))

@helpers.uses_mongo
def mturk(request, mongo):
    """
        This method handles requests from an mturk ExternalQuestion.
        
        There are two main cases:
          1. assignmentId == None :
            Indicates a HIT that hasn't been accepted yet.
            ==> Render static-template.html
            
          2. assignmentId == "string" :
            Indicates an accepted (active) HIT
            ==> Create a game_session,
                Render mturk-user-task.html
    """
    
    #Retrieve assignmentId
    assignmentId = request.GET.get("assignmentId", None)

    if assignmentId:

        #Retrieve other mturk variables
        #! This should throw an error if any of these are missing.
        workerId = request.GET.get("workerId", None)
        hitId = request.GET.get("hitId", None)
        turkSubmitTo = request.GET.get("turkSubmitTo", None)

        old_game_session = mongo.get_collection("cvm_game_session").find_one({"user.user_info.workerId": workerId})
        if old_game_session:
            print "There exists an old_game_session for the mturker!"
            old_batch = mongo.get_collection("cvm_batch").find_one({"_id": old_game_session["batch_id"]})
            old_codebook = mongo.get_collection("cvm_codebook").find_one({"_id": old_batch["profile"]["codebook_id"]})

            # assignmentDict will be refreshed (datetime is overwritten) each time user refreshes the page
            # or re-enter the old game session he left last time.
            assignmentIdDict = old_game_session["user"]["user_info"]["assignmentIdDict"]
            key = assignmentId

            # looks redundent but easy to understand :)
            if not key in assignmentIdDict: # old user uses new assignmentId to pick up old task
                assignmentIdDict[key] = datetime.datetime.now()
            else: # old user refreshes the page
                assignmentIdDict[key] = datetime.datetime.now()
            
            mongo.get_collection("cvm_game_session").update(
                    { "_id": ObjectId(old_game_session["_id"]) },
                    { "$set": { "user.user_info.assignmentIdDict": assignmentIdDict}}
            )            

            result = {'batch': old_batch, 'codebook': old_codebook, 'game_session': old_game_session}

            return render_to_response('tasks/mturk-user-task.html', result, context_instance=RequestContext(request))
        else:
            result = models.logic.create_mturk_game_session(request, assignmentId, workerId, hitId, turkSubmitTo)

            return render_to_response('tasks/mturk-user-task.html', result, context_instance=RequestContext(request))
        
        #redirect to /tasks/game-session/[gs_id]
        # actual mturk task taker
    else:
        codebooks = list(mongo.get_collection("cvm_codebook").find())
        documents = list(mongo.get_collection("cvm_document").find().limit(10))
        result = {
            'codebook' : random.choice( codebooks ),
            'document' : random.choice( documents ),
        }
        
        return render_to_response('tasks/mturk-preview.html', result, context_instance=RequestContext(request))
    

#!! Do we need this method any more...?
#@helpers.uses_mongo
#def task_all_done(request, mongo, game_session_id):
#    game_session = mongo.get_collection("cvm_game_session").find_one({"_id": ObjectId(game_session_id)})
#    return render_to_response('tasks/all-done.html', {'game_session':game_session}, context_instance=RequestContext(request))
  
@helpers.uses_mongo
def get_first_task(request, mongo):
    #Retrieve game_session_id
    #! Need to add validation
    gs_id = request.POST['gs_id']

    result = models.logic.get_first_task(gs_id)

    # Return the document, game_stats, and game_setup
    #! Are we returning document old_labels, or just content?  It should only content.
    #! Game setup does not need to be returned here.
    return helpers.gen_json_response({
        "status": "success",
        "msg": "Here's the first task",
        "document": result["document"],
        "game_stats": result["game_stats"],
        "game_setup": result["game_setup"],
    })

@helpers.uses_mongo
def submit_task(request, mongo):
    #Retrieve reponse object
    data = json.loads(request.raw_post_data)
    
    #! Need object validation
    
    #Remove CSRF token
    del data["csrfmiddlewaretoken"]

    result = models.logic.submit_task(data)
    
    if result:    
        #Return next document, game stats, and markup
        return helpers.gen_json_response({
            "status": "success",
            "msg": "Successfully submit the task",
            "next_document": result["next_document"],
            "game_stats": result["game_stats"],
            "codebook_markup": {}
        })

    #If no documents are left in the batch
    else:
        #print "Congratulations! You have finished all the tasks!"
        #Return a success message and game stats
        return helpers.gen_json_response({"status": "failed", "msg": "No next document in batch!", "game_stats": new_game_stats})

