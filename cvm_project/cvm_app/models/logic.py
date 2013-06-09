"""
Business logic for models.
"""

from django.contrib.auth.models import User
from django.db import connections
from bson.objectid import ObjectId
from pymongo.errors import InvalidId
from django.shortcuts import render_to_response
from django.template import RequestContext

import csv, re, json, datetime, random, string
from collections import defaultdict

from cvm_app.algorithms.jenkins import hashlittle
from cvm_app.models.helpers import uses_mongo, MongoEncoder

import cvm_app.models as models
from cvm_app.views import helpers

@uses_mongo
def update_batch_progress(mongo, id_):
    #Connect to the DB
    coll = mongo.get_collection("cvm_batch")

    #Retrieve the batch
    batch = coll.find_one({"_id": id_})
    #print json.dumps(batch, indent=2, cls=MongoEncoder)

    #Scaffold the progress object
    progress = {
        "summary": {}
    }

    #Count total and complete document codes
    assigned, complete = 0, 0

    progress["summary"] = {
        "assigned": assigned,
        "complete": complete,
        #"percent": round(float(100 * complete) / assigned, 1),
    }

    #print id_
    #print "!"*80
    #print json.dumps(batch, indent=2, cls=MongoEncoder)
    batch["reports"]["progress"] = progress
#    print json.dumps(progress, indent=2, cls=MongoEncoder)

    coll.update({"_id": ObjectId(id_)}, batch)
#    print result#json.dumps(progress, indent=2, cls=MongoEncoder)

#This is one way new collections are created
def convert_document_csv_to_bson(csv_text):
    C = csv.reader(csv.StringIO(csv_text))

    #Parse the header row
    H = C.next()

    #Capture the url/content column index
    url_index, content_index = None, None
    if 'url' in H:
        url_index = H.index('url')
    if 'content' in H:
        content_index = H.index('content')

    if url_index==None and content_index==None:
        raise Exception('You must specify either a "url" column or a "content" column in the .csv header.')

    #Identify metadata_fields
    meta_fields = {}
    for h in H:
        if re.match('META_', h):
            name = re.sub('^META_', '', h)
            index = H.index(h)
            if name in meta_fields:
                raise Exception('Duplicate META_ name : '+name)
            meta_fields[name] = index

#    print json.dumps(meta_fields, indent=2)

    documents_json = []

    #http://lethain.com/handling-very-large-csv-and-xml-files-in-python/
    #print csv.field_size_limit()
    csv.field_size_limit(1000000)
    
    #For each row in the collection
    for row in C:
        j = {}

        #Grab the content or url
        #If both are present, url gets precedence
        if url_index != None:
            j['url'] = row[url_index]
        elif content_index != None:
            j['content'] = row[content_index]

        #Grab metadata fields
        m = {}
        for f in meta_fields:
            #Don't include missing values
            #! Maybe include other missing values here
            if meta_fields[f] != '':
                m[f] = row[meta_fields[f]]

        #Don't include empty metadata objects
        if m != {}:
            j["metadata"] = m

        documents_json.append(j)

#    print json.dumps(documents_json, indent=2)
    return documents_json

### Batches ###################################################################



def generate_compiled_batch(count, index_compiled_batch, codebook_id, collection_ids, doc_size, docs):
    profile = {
        'name': 'Batch ' + str(count + 1),
        'description': "This is a compiled batch for " + 'Batch ' + str(index_compiled_batch),
        'index': count + 1,
        'codebook_id': codebook_id,
        'collection_ids': collection_ids,
        'parent_batch_id': None,
        'pct_overlap': -1,
        'replication': -1,
        'created_at': datetime.datetime.now(),
        'doc_size': doc_size,
    }

    #Construct batch object
    batch = {
        'profile' : profile,
        'documents': docs,
        'reports': {
            'progress': {},
            'reliability': {},
        },
    }
    
    return batch

@uses_mongo
def gen_game_session(mongo, batch_id, user, replication):
    #Construct object
    #user_name = mongo.get_collection("cvm_user").find_one({"user": ObjectId(batch_id))

    lane = -1

    if user["user_type"] == "anonymous":
        lane_seed = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        lane = helpers.random_lane_number_generator(lane_seed, replication) ### Needs to figure this out!!
        
    elif user["user_type"] == "member":
        #print user["user_info"]["username"]
        user = mongo.get_collection("cvm_user").find_one({"profile.user_name": user["user_info"]["username"]})
        #print user
        user_lane_seed = user["profile"]["lane_seed"]
        lane = helpers.random_lane_number_generator(user_lane_seed, replication)
        
    elif user["user_type"] == "mturk":
        lane = models.helpers.random_lane_number_generator(user["user_info"]["workerId"], replication)

    #print '*'*80
    #print "lane number is ", lane

    # find how many tasks are remaining in the batch 
    responses = list(mongo.get_collection("cvm_response").find({"batch_id": ObjectId(batch_id)}))
    response_size = len(responses)
    tasks_remaining = 0
    
    for index in range(response_size):
        if "any" in responses[index]["lanes"] and not responses[index]["lanes"]["any"]["game_session_id"]:
            tasks_remaining = tasks_remaining + 1
        elif str(lane) in responses[index]["lanes"] and not responses[index]["lanes"][str(lane)]["game_session_id"]:
            tasks_remaining = tasks_remaining + 1

    #print "aaa"*80
    #print "response_size is ", response_size
    #print "tasks_remaining is ", tasks_remaining

    default_game_session_setting = models.gen.game_session(batch_id, user, tasks_remaining, lane)

    return default_game_session_setting        

@uses_mongo
def get_next_document(mongo, lane, batch, gs_id):
    responses = list(mongo.get_collection("cvm_response").find({"batch_id": batch["_id"]}))
    response_size = len(responses)

    # There should be at most one uncompleted response for each game session
    #print "gs_id is ", gs_id
    
    game_session = mongo.get_collection("cvm_game_session").find_one({"_id": ObjectId(gs_id)})
    lane_number = str(game_session["lane"])
    #print "lane is ", lane_number
    uncompleted_responses = []
    uncompleted_response_any = mongo.get_collection("cvm_response").find_one({"lanes.any.game_session_id": gs_id, "lanes.any.finished_at": ""})
    #print uncompleted_response_any
    query1 = "lanes." + lane_number + ".game_session_id"
    query2 = "lanes." + lane_number + ".finished_at"
    #print "query1 is ", query1
    #print "query2 is ", query2
    uncompleted_response_lane = mongo.get_collection("cvm_response").find_one({query1: gs_id, query2: ""})
    #print uncompleted_response_lane

    if uncompleted_response_any:
        uncompleted_responses.append(uncompleted_response_any)
    if uncompleted_response_lane:
        uncompleted_responses.append(uncompleted_response_lane)

    if uncompleted_responses:
        if len(uncompleted_responses) > 1:
            print "sth is wrong!!!"
            return None
        else:
            document_id = uncompleted_responses[0]["document_id"]
            content = mongo.get_collection("cvm_document").find_one({"_id": ObjectId(document_id)})["content"]
            return {
                'document_id': document_id,
#                'collection_index': collection_index,
                'content': content,
                #'index': collection_index,
                #'content': collection_content,
            }

    #print doc_size    

    #Find all empty slots for coding within the user's lane
    batch_indexes = []
    for index in range(response_size):
        if "any" in responses[index]["lanes"] and not responses[index]["lanes"]["any"]["game_session_id"]:
            batch_indexes.append(index)
        elif str(lane) in responses[index]["lanes"] and not responses[index]["lanes"][str(lane)]["game_session_id"]:
            batch_indexes.append(index)

    #batch = mongo.get_collection("cvm_batch").find_one({"_id": ObjectId(batch_id)},{"documents.$0.index":1})
    #print json.dumps(batch, cls=MongoEncoder, indent=2)
    #indexes = range(len(batch["documents"]))
    #print batch_indexes
    #print batch_indexes
    
    #If at least one slot is open in this batch...
    if len(batch_indexes) > 0:
        #Pick an index at random
        random.shuffle(batch_indexes)
        #print batch_indexes
        batch_index = batch_indexes[0]
        if "any" in responses[batch_index]["lanes"]:
            task_remaining_list = []
            for each in batch["reports"]["progress"]["task_remaining_list"]:
                each = each - 1
                task_remaining_list.append(each)

            mongo.get_collection("cvm_batch").update(
                { "_id": batch["_id"] },
                { "$set": { "reports.progress.task_remaining_list": task_remaining_list}}
            )
        else:
            task_remaining_list = batch["reports"]["progress"]["task_remaining_list"]
            task_remaining_list[lane] = task_remaining_list[lane] - 1

            mongo.get_collection("cvm_batch").update(
                { "_id": batch["_id"] },
                { "$set": { "reports.progress.task_remaining_list": task_remaining_list}}
            )

        #Retrieve the content of the document
        document_id = responses[batch_index]["document_id"]
        #collection_index = batch["documents"][batch_index]["collection_index"]
        content = mongo.get_collection("cvm_document").find_one({"_id": ObjectId(document_id)})["content"]

        #print "haha" * 80
        #print "picked_index is ", indexes[0]
        #print "batch_index is ", batch_index
        
        return {
            'document_id': document_id,
#            'collection_index': collection_index,
            'content': content,
            #'index': collection_index,
            #'content': collection_content,
        }

    else:
        print "No next document at all!"
    
        return None
        """
            #'content': -1,
            'batch_index': -1,
            'collection_content': {},
        }
        """

def calc_label_score(batch, labels, doc_index):
    #################! Put in modified kripp.alpha here!##########################
    if random.uniform(0,1) > .5:
        score = int(random.uniform(-50,100))
    else:
        score = None
    ########### we will figure out the markup later#####
    markup = {}
    return (score, markup)

def update_game_stats(tasks_remaining, old_game_stats, game_setup, new_score=None):
    if not new_score is None:
        scored_tasks = old_game_stats["scored_tasks"]+1
        #Update avg score
        avg_score = (new_score + (scored_tasks-1)*old_game_stats["avg_score"])/scored_tasks
    else:
        scored_tasks = old_game_stats["scored_tasks"]
        avg_score = old_game_stats["avg_score"]
        
    tasks_until_next_bonus = game_setup["bonus_frequency"]-(old_game_stats["tasks_completed"]+1) % game_setup["bonus_frequency"]
    tasks_completed = old_game_stats["tasks_completed"]+1
    return {
        'total_score': avg_score * tasks_completed,
        'avg_score': avg_score,
        'tasks_completed': tasks_completed,
        'scored_tasks': scored_tasks,
        'tasks_remaining': tasks_remaining,
        'tasks_until_next_bonus': tasks_until_next_bonus,
        'last_score': new_score,

#        'bonus_credits': game_setup["bonus_amount"] * tasks_completed/3,#game_setup["bonus_frequency"],
#        'bonus_amount': game_setup["bonus_amount"],
    }

###########################################################
#! Here's the stuff that was just moved back

#import cvm_app.models as models

#@models.helpers.uses_mongo
def get_batch_profile_json(new_collection=None, old_batch=None):
    """Create json for a new batch
        Assumes:
            All entries in batch.profile.collection_ids are unique
            A batch that includes a given collection includes *ALL* of the documents in the collection
    """

    #! Need views validation to prevent this case:
    if not old_batch and not new_collection:
        #print 'LKKLN:LKNB:LBL:KBJ:KBJK:L'
        return {
            'docs': [],
            'collection_ids': [],
            'doc_size': 0,
            'parent_batch_id': None,
        }

    #Define (old) collection_ids, parent_batch_id
    if old_batch:
        collection_ids = old_batch["profile"]["collection_ids"]
        parent_batch_id = old_batch["_id"]
    else:
        collection_ids = []
        parent_batch_id = None

    #Add doc_size
    if old_batch:
        if new_collection and not new_collection["_id"] in collection_ids:
            doc_size = old_batch["profile"]["doc_size"] + new_collection["profile"]["size"]
        else:
            doc_size = old_batch["profile"]["doc_size"]
    else:
        doc_size = new_collection["profile"]["size"]            

    #Add docs from new_collection, if applicable
    if new_collection and not new_collection["_id"] in collection_ids:
        collection_ids.append(new_collection["_id"])
        add_new_collection = "yes"
    else:
        add_new_collection = "no"

    return {
        #'docs': docs,
        'collection_ids': collection_ids,
        'doc_size': doc_size,
        'parent_batch_id': parent_batch_id,
        'add_new_collection': add_new_collection,
    }

def get_new_batch_json(count, pct_overlap, replication, codebook, collection, batch):
    #print json.dumps(collection, indent=2, cls=MongoEncoder)
    #print json.dumps(codebook, indent=2, cls=MongoEncoder)

    #Construct profile object
    #print collection
    #print batch
    update_info = get_batch_profile_json(collection, batch)
    profile = {
        'name': 'Batch ' + str(count + 1),
        'priority': random.randint(0, 100),
        'description': "",
        'index': count + 1,
        'codebook_id': codebook['_id'],
        'collection_ids': update_info["collection_ids"],
        'parent_batch_id': update_info["parent_batch_id"],
        'pct_overlap': pct_overlap,
        'replication': replication,
        'created_at': datetime.datetime.now(),
        'doc_size': update_info["doc_size"],
        'game_setup' : {
            'exchange_rate': 2.00,
            'bonus_frequency': 25,
            'bonus_amount': 2,
        }
    }

    task_remaining_list = []
    for index in range(replication):
        task_remaining_list.append(update_info["doc_size"])

    if collection:
        profile["description"] = collection["profile"]["name"][:20] + " * " + codebook["profile"]["name"][:20] + " (" + str(codebook["profile"]["version"]) + ")"

    elif batch:
        profile["description"] = batch["profile"]["name"][:20] + " * " + codebook["profile"]["name"][:20] + " (" + str(codebook["profile"]["version"]) + ")"

    else:
        print "There are no batches and collections at all!"
        assert False

    #Construct batch object
    batch = {
        'profile' : profile,
        #'documents': update_info["docs"],
        'reports': {
            'progress': {"task_remaining_list": task_remaining_list},
            'reliability': {},
        },
        'add_new_collection': update_info["add_new_collection"],
    }
        
    return batch

@models.helpers.uses_mongo
def gen_batch_responses_json(mongo, pct_overlap, replication, batch, new_collection = None):
    old_batch_id = batch["profile"]["parent_batch_id"]
    old_batch = old_batch = mongo.get_collection("cvm_batch").find_one({"_id": ObjectId(old_batch_id)})
    new_batch_id = batch["_id"]

    #print "old_batch is ", old_batch
    
    #Add docs (and old_labels) from old_batch, if applicable
    responses = []
    if old_batch:
        #print responses
        responses = list(mongo.get_collection("cvm_response").find({"batch_id": ObjectId(old_batch_id)}))
        #print responses

        for r in responses:
            r["old_responses"], r["lanes"] = r["_id"], {}
            r["batch_id"] = new_batch_id
            del r["_id"]
            
    #Add docs from new_collection, if applicable
    if new_collection:
        k = len(new_collection["doc_ids"])

        more_responses = [{} for i in range(k)]

        for i in range(k):
            more_responses[i] = {
#                "index": i+len(docs),
                "document_id": new_collection["doc_ids"][i],
                "batch_id": new_batch_id,
                "lanes": {},
#                "old_labels": {},
            }
            
        responses = responses + more_responses

    size = len(responses)
    overlap = int((size * pct_overlap) / 100)
    
    random.shuffle(responses)

    shared = responses[:overlap]
    unique = responses[overlap:]

    #Construct documents object

    for response in shared:
        response['lanes'] = dict( (str(j),{"game_session_id": "", "created_at": "", "finished_at": "", "labels": {}}) for j in range(replication) )

    for response in unique:
        response['lanes'] = { "any":{"game_session_id": "", "created_at": "", "finished_at": "", "labels": {}} }

    #print json.dumps(responses, indent=2, cls=cvm_app.models.helpers.MongoEncoder)
#    random.shuffle(docs)
#    assert False

    for response in responses:
        response_id = mongo.get_collection("cvm_response").insert(response)
        

    return helpers.gen_json_response({"status": "success", "msg": "Successfully generate new responses."})

# task.py helper functions

@uses_mongo
def create_mturk_game_session(mongo, request, assignmentId, workerId, hitId, turkSubmitTo):

    #Get a random sequence over batches
    #! We need to replace this logic with a "priority" sort over batches
    batch_total = mongo.get_collection("cvm_batch").count()
    #indexes = range(batch_total)
    #random.shuffle(indexes)

    #batch_index = 0
    #! Yikes.  "while True" loops scare me.

    batches = list(mongo.get_collection("cvm_batch").find(fields={"profile": 1, "reports": 1}, sort=[('profile.priority', -1)]))
    
    counter = 0
    #############!!!!!! Have not vetted the contents of this loop !!!!!################
    for b in batches:
        print "haha"
        print b["profile"]["priority"]

    for batch in batches:
        #try:        
        #    batch_id = indexes[batch_index] + 1
        #except IndexError:
        #    return render_to_response('tasks/no-tasks-left.html', context_instance=RequestContext(request))
        #batch_name = "Batch " + str(batch_id)
        #batch = mongo.get_collection("cvm_batch").find_one({"profile.name": batch_name})
        lane = models.helpers.random_lane_number_generator(workerId, batch["profile"]["replication"])
        #print batch
        #print batch_name

        responses = list(mongo.get_collection("cvm_response").find({"batch_id": ObjectId(batch["_id"])}))
        response_size = len(responses)
        tasks_remaining = 0
            
        for index in range(response_size):
            if "any" in responses[index]["lanes"] and not responses[index]["lanes"]["any"]["game_session_id"]:
                tasks_remaining = tasks_remaining + 1
            elif str(lane) in responses[index]["lanes"] and not responses[index]["lanes"][str(lane)]["game_session_id"]:
                tasks_remaining = tasks_remaining + 1

        print "bbb"*80
        print tasks_remaining

        if tasks_remaining:
            print "yida" * 80
            print batch["profile"]["priority"]
            break
        else:
            counter = counter + 1

    if counter == batch_total:
        return render_to_response('tasks/no-tasks-left.html', context_instance=RequestContext(request))
    #create game_session
    
    # create assignmentDict the first time
    assignmentIdDict = {}
    key = assignmentId
    assignmentIdDict[key] = datetime.datetime.now()
    user = {
        "user_type" : "mturk",
        "user_info" : {
            "assignmentIdDict" : assignmentIdDict,
            "workerId" : workerId,
            "hitId" : hitId,
            "turkSubmitTo" : turkSubmitTo,
        },
        "screen_info" : {},
    }
    J = models.logic.gen_game_session(batch["_id"], user, batch["profile"]["replication"])

    gs_id = mongo.get_collection("cvm_game_session").insert(J)

    # retrieve the data
    #docs = batch["documents"]
    codebook = mongo.get_collection("cvm_codebook").find_one({"_id": batch["profile"]["codebook_id"]})
    game_session = mongo.get_collection("cvm_game_session").find_one({"_id": ObjectId(gs_id)})
    result = {'batch': batch, 'codebook': codebook, 'game_session': game_session}

    return result

@uses_mongo
def get_first_task(mongo, gs_id):
    #Fetch game_session from database
    game_session = mongo.get_collection("cvm_game_session").find_one({"_id": ObjectId(gs_id)})
    lane = game_session["lane"]
        
    #Fetch batch from database
    batch_id = game_session["batch_id"]
    batch = mongo.get_collection("cvm_batch").find_one({"_id": ObjectId(batch_id)})

    #Get the next document in the batch
    document = models.logic.get_next_document(lane, batch, gs_id)
    document_id = document["document_id"]

    response = mongo.get_collection("cvm_response").find_one({"batch_id": ObjectId(batch_id), "document_id": ObjectId(document_id)})

    print "batch_id is ", batch_id
    print "document_id is ", document_id
    print json.dumps(response, indent=2, cls=helpers.MongoEncoder)
    
    #If the document isn't null (i.e the batch contained at least one uncoded document in the lane)
    if document and response:
        #Store game_session_id and created_at in the correct slots in batch.documents
        #! This logic should live in get_next_document()
        if "any" in response["lanes"]:
            response["lanes"]["any"]["game_session_id"] = gs_id
            response["lanes"]["any"]["created_at"] = datetime.datetime.now()

        else:
            response["lanes"][str(lane)]["game_session_id"] = gs_id
            response["lanes"][str(lane)]["created_at"] = datetime.datetime.now()

        mongo.get_collection("cvm_response").update(
            { "_id": ObjectId(response["_id"]) },
            { "$set": { "lanes": response["lanes"]}}
        )

    return {
        "document": document,
        "game_stats": game_session["game_stats"],
        "game_setup": batch["profile"]["game_setup"],
    }

@uses_mongo
def submit_task(mongo, data):
    #Fetch the game_session
    old_game = mongo.get_collection("cvm_game_session").find_one({"_id": ObjectId(data["game_session_id"])})
    old_game_stats = old_game["game_stats"]
    lane = old_game["lane"]
    
    #Fetch the batch
    batch_id = old_game["batch_id"]
    batch = mongo.get_collection("cvm_batch").find_one({"_id": ObjectId(batch_id)})

    #Update the game_session
    (score, markup) = models.logic.calc_label_score(batch, data["labels"], data["document_id"])
    tasks_remaining = batch["reports"]["progress"]["task_remaining_list"][old_game["lane"]]
    new_game_stats = models.logic.update_game_stats(tasks_remaining, old_game_stats, batch["profile"]["game_setup"], score)

    mongo.get_collection("cvm_game_session").update(
        { "_id": ObjectId(data["game_session_id"]) },
        { "$set": { "game_stats": new_game_stats}}
    )

    #Update the batch document
    document_id = data["document_id"]
    response = mongo.get_collection("cvm_response").find_one({"batch_id": ObjectId(batch_id), "document_id": ObjectId(document_id)})

    if "any" in response["lanes"]:
        response["lanes"]["any"]["labels"] = data["labels"]
        response["lanes"]["any"]["finished_at"] = datetime.datetime.now()
        
    else:
        response["lanes"][str(old_game["lane"])]["labels"] = data["labels"]
        response["lanes"][str(old_game["lane"])]["finished_at"] = datetime.datetime.now()

    mongo.get_collection("cvm_response").update(
        { "_id": ObjectId(response["_id"]) },
        { "$set": { "lanes": response["lanes"]}}
    )
    #! I don't understand this comment:
    # leave it later after changing the database

    #Get the next document
    new_document = models.logic.get_next_document(old_game["lane"], batch, data["game_session_id"])

    #If the document isn't null, add placeholders in the right batch.document.lane
    #! Again, this logic should live in get_next_document()
    new_document_id = new_document["document_id"]

    new_response = mongo.get_collection("cvm_response").find_one({"batch_id": ObjectId(batch_id), "document_id": ObjectId(new_document_id)})

    print "batch_id is ", batch_id
    print "new_document_id is ", new_document_id
    print json.dumps(new_response, indent=2, cls=helpers.MongoEncoder)

    #If the document isn't null (i.e the batch contained at least one uncoded document in the lane)
    if new_document and new_response:
        #Store game_session_id and created_at in the correct slots in batch.documents
        #! This logic should live in get_next_document()
        if "any" in new_response["lanes"]:
            new_response["lanes"]["any"]["game_session_id"] = data["game_session_id"]
            new_response["lanes"]["any"]["created_at"] = datetime.datetime.now()

        else:
            new_response["lanes"][str(lane)]["game_session_id"] = data["game_session_id"]
            new_response["lanes"][str(lane)]["created_at"] = datetime.datetime.now()

        mongo.get_collection("cvm_response").update(
            { "_id": ObjectId(new_response["_id"]) },
            { "$set": { "lanes": new_response["lanes"]}}
        )

        return {
            "next_document": new_document,
            "game_stats": new_game_stats,
        }
    else:
        return None

#! This method needs to be tested more
#! This method could probably be rewritten as a models method
#! In that case, we could remove the AJAX handling
@uses_mongo
def create_game_session(request, mongo):
    #Load the request and remove the CSRF middleware token
    J = json.loads(request.raw_post_data)
    del J["csrfmiddlewaretoken"]

    #Retrieve the appropriate batch
    batch = mongo.get_collection("cvm_batch").find_one({"_id": ObjectId(J["batch_id"])})

    #For members: Check to see if a game session for this user/batch pair already exists
    if J["user"]["user_type"] == "member":
        gs_temp = mongo.get_collection("cvm_game_session").find_one({"batch_id": ObjectId(J["batch_id"]), "user.user_info.username": request.user.username})

    #If so, return the *old* batch session, so the user can continue.
    if gs_temp:
        return helpers.gen_json_response({"status": "success", "msg": "Return old game session.", "gs_id": gs_temp["_id"]})
    
    #If no old session exists...
    else:
        #For members, add username to the user_info field
        if J["user"]["user_type"] == "member":
            J["user"]["user_info"] = {'username': request.user.username}

        #Construct and insert game_session json object
        J = models.logic.gen_game_session(J["batch_id"], J["user"], batch["profile"]["replication"])
        gs_id = mongo.get_collection("cvm_game_session").insert(J)

        #Return success message
        return helpers.gen_json_response({"status": "success", "msg": "Added new game session.", "gs_id": gs_id})


















