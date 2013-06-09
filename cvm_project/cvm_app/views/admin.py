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
import cvm_app.models.logic
import cvm_app.models as models

#import cvm_app.models.gen as models.gen
#import cvm_app.models.gen as gen
from cvm_app.views import helpers

import bson
from bson import json_util
import random, string

### Admin: Object list pages ###################################################

@helpers.admin_required
def admin(request):
   return render_to_response('admin/home.html', context_instance=RequestContext(request))
       
@helpers.admin_required
def users(request):
    result = {
        'users': helpers.jsonifyRecords(
            User.objects.all(),
            ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'last_login']
        )
    }
    return render_to_response('admin/users.html', result, context_instance=RequestContext(request))

@helpers.admin_required
@helpers.uses_mongo
def codebooks(request, mongo):
    result = {
        'codebooks': list(mongo.get_collection("cvm_codebook").find(sort=[('profile.created_at', 1)])),
    }
    return render_to_response('admin/codebooks.html', result, context_instance=RequestContext(request))

@helpers.admin_required
@helpers.uses_mongo
def collections(request, mongo):
    result = {
        'collection': list(mongo.get_collection("cvm_collection").find(fields={"profile":1})),
    }
    return render_to_response('admin/collections.html', result, context_instance=RequestContext(request))

@helpers.admin_required
@helpers.uses_mongo
def batches(request, mongo):
    result = {
        'batches': list(mongo.get_collection("cvm_batch").find(fields={"profile": 1, "reports": 1}, sort=[('profile.priority', -1)])),
        'codebooks': list(mongo.get_collection("cvm_codebook").find(sort=[('profile.created_at', 1)])),
        #! Not sure we need this query:
        'collections': list(mongo.get_collection("cvm_collection").find(fields={"profile":1})),
        #! Not sure we need this query:
        #! This query could be really inefficient:
        'users': helpers.jsonifyRecords(User.objects.all(), ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser']),
    }
    return render_to_response('admin/batches.html', result, context_instance=RequestContext(request))

@helpers.admin_required
def administration(request):
    result = {
        #! Not sure we need this query:
        #! This query could be really inefficient:
        'users': helpers.jsonifyRecords(User.objects.all(), ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'last_login']),
    }
    return render_to_response('administration.html', result, context_instance=RequestContext(request))

### Admin: Object list pages ###################################################

@helpers.admin_required
@helpers.uses_mongo
def user(request, mongo, username):
    print username
    result = {
        "user": mongo.get_collection("cvm_user").find_one( {"profile.user_name": username} ),
        "authuser": mongo.get_collection("auth_user").find_one( {"username": username} ),
    }    
    return render_to_response('admin/user.html', result, context_instance=RequestContext(request))

@helpers.admin_required
@helpers.uses_mongo
def codebook(request, mongo, id_):
    result = {
        "codebook": mongo.get_collection("cvm_codebook").find_one( {"_id": ObjectId(id_)} )
    }
    return render_to_response('admin/codebook.html', result, context_instance=RequestContext(request))

@helpers.admin_required
@helpers.uses_mongo
def collection(request, mongo, id_):
    result = {
        "collection": mongo.get_collection("cvm_collection").find_one(
            {"_id": ObjectId(id_)},
            {"profile": 1}
        )
    }
    return render_to_response('admin/collection.html', result, context_instance=RequestContext(request))

@helpers.admin_required
@helpers.uses_mongo
def batch(request, mongo, id_):
    batch = mongo.get_collection("cvm_batch").find_one({"_id": ObjectId(id_)}, fields={"profile": 1, "reports": 1, "documents": 1})
    result = {
        'batch': batch,
        'codebook': mongo.get_collection("cvm_codebook").find_one(
            {"_id": ObjectId(batch["profile"]["codebook_id"])},
            {"profile":1}
        ),
        #! Need to retrieve appropriate collections here
#        'collection': mongo.get_collection("cvm_collection").find_one(
#            {"_id": ObjectId(batch["profile"]["collection_id"])},
#            {"profile":1}
#        ),
        #! This query could be really inefficient
        #! Not sure we need this query here
        'users': helpers.jsonifyRecords(User.objects.all(), ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser']),
    }
    return render_to_response('admin/batch.html', result, context_instance=RequestContext(request))

@helpers.admin_required
@helpers.uses_mongo
def export_batch(request, mongo, batch_id):
    #! These should be populated from a form, but said form doesn't exist yet.
    include_empty_rows = False
    include_doc_content = False

    #Retrieve the relevant objects
    batch = mongo.get_collection("cvm_batch").find_one( {"_id": ObjectId(batch_id)} )
    documents = batch["documents"]
    collection = mongo.get_collection("cvm_collection").find_one({"_id": ObjectId(batch["profile"]["collection_id"])} )
    codebook = mongo.get_collection("cvm_codebook").find_one({"_id": ObjectId(batch["profile"]["codebook_id"])} )

    #Get column names...
    col_names = models.gen_codebook_column_names(codebook)
    col_index = models.gen_col_index_from_col_names(col_names)

    #Generate filename
    filename = helpers.sluggify(collection["profile"]["name"])+"-"+datetime.datetime.now().strftime("%Y-%M-%d-%H-%M-%S")+".csv"

    #Begin constructing a response
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+filename+'.csv'
    writer = csv.writer(response)

    #Generate and write column headers
    header = ['index', 'username']
    if include_doc_content:
        header += ['document']
    header += col_names
    writer.writerow(header)

    for i,doc in enumerate(documents):
        for coder in doc["labels"]:
            answer_set = models.get_most_recent_answer_set(doc["labels"][coder])
            if answer_set != {} or include_empty_rows:
                row = [i, coder]
                if include_doc_content:
                    row += [collection["documents"][i]["content"]]
                row += models.gen_csv_column_from_batch_labels(answer_set, col_index)
                writer.writerow(row)

    return response

### Admin: Ajax ################################################################

@helpers.admin_required
@helpers.uses_mongo
def create_account(request, mongo):
    #Validate first name
    if len(request.POST["first_name"]) == 0:
        return helpers.gen_json_response({"status": "failed", "msg": "First name cannot be blank."})

    #! Need more response validation!

    #Build the new user object from the response fields
    try:
        new_user = User.objects.create_user(
                request.POST["username"],
                request.POST["email"],
                request.POST["username"],   # Password
                )
        new_user.first_name = request.POST["first_name"]
        new_user.last_name = request.POST["last_name"]
        new_user.is_staff = "admin" in request.POST
        new_user.is_superuser = "admin" in request.POST
        
        #Save to database
        new_user.save()
    
    #If a required field is missing...
    except MultiValueDictKeyError:
        #Return an error message
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})

    #Construct the user_profile object, using new_user.username as the 1-to-1 key
    user_name = new_user.username
    lane_seed = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    
    #import cvm_app.models as models
    J = models.gen.user_profile( user_name, lane_seed )
    
    #Write to database
    mongo.get_collection("cvm_user").insert(J)    

    #Return a success message
    return helpers.gen_json_response({"status": "success", "msg": "Successfully created account."})

@helpers.admin_required
def update_account(request):
    #Validate response
    if len(request.POST["first_name"]) == 0:
        return helpers.gen_json_response({"status": "failed", "msg": "First name cannot be blank."})

    if len(request.POST["password"]) < 4:
        return helpers.gen_json_response({"status": "failed", "msg": "Password must be at least 4 characters long."})

    #! More validation needed

    #Retrieve the user object
    user = request.user
    
    #Update fields from the request
    try:
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        user.set_password(request.POST["password"])
        
        #Write to database
        user.save()
    
    #If a required field is missing...
    except MultiValueDictKeyError:
        #Return an error message
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})

    #Return a success message
    return helpers.gen_json_response({"status": "success", "msg": "Successfully updated account."})

@helpers.admin_required
def update_permission(request):
    #Retreive user object
    try:
        user = User.objects.get(username=request.POST["username"])
    except MultiValueDictKeyError:
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field 'username.'"})

    #Toggle 'active' status
    if "active" in request.POST:
        new_status = request.POST["active"] == 'true'
        if not new_status and user.is_superuser:
            return helpers.gen_json_response({"status": "failed", "msg": "Sorry, you can't deactivate a user with admin privileges."})
        else:
            user.is_active = new_status
            
            #When a user is reactivated, set his password to be the same as his username
            #! This behavior needs to change!
            if user.is_active:
                user.set_password(user.username)

    #Toggle admin status
    if "admin" in request.POST:
        new_status = request.POST["admin"] == 'true'
        if not new_status and User.objects.filter(is_superuser=True).count() < 2:
            return helpers.gen_json_response({"status": "failed", "msg": "Sorry, you can't remove admin privileges from the last administrator."})
        elif new_status and not user.is_active:
            return helpers.gen_json_response({"status": "failed", "msg": "Sorry, you can't grant admin privileges to an inactive user."})
        else:
            user.is_superuser = new_status
            
    #Write to database
    user.save()

    #Return success message
    return helpers.gen_json_response({"status": "success", "msg": "Successfully updated permissions.", "new_status": new_status})


@helpers.admin_required
@helpers.uses_mongo
def upload_collection(request, mongo):
    #! This method assumes the file is a csv file

    #Get name, description, and file handle
    try:
        name = request.POST["name"]
        csv_file = request.FILES["fileInput"]
        filename = unicode(csv_file)
        description = request.POST.get("description", '')

    #If a required field is missing...
    except MultiValueDictKeyError:
        #Return an error message
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})

    #Validate the collection name
    if len(name) == 0:
        return helpers.gen_json_response({"status": "failed", "msg": "Name cannot be blank."})

    #Read in the (full) contents of the csv file
    #! We could rewrite the whole document conversion process using an iterator
    csv_text = csv_file.read()
    
    #Convert csv_text to a bson object
    #! This is a legacy method from textbadger.
    documents = models.convert_document_csv_to_bson(csv_text)
    
    #Loop over documents
    doc_ids = []
    for document in documents:
        #! get_new_document_json could be consolidated with convert_document_csv_to_bson for greater clarity
        json_doc = models.gen.document(document)
        
        #Insert into DB
        doc_id = mongo.get_collection("cvm_document").insert(json_doc)
        
        #Add the document id to doc_ids
        doc_ids.append(doc_id)

    #Build final collection object
    J = models.gen.collection( name, description, doc_ids )
    mongo.get_collection("cvm_collection").insert(J)

    return redirect('/admin/collections/')

#!! Not sure about the status of this method.  Does it work?  Is it just for testing?
@helpers.admin_required
@helpers.uses_mongo
def upload_document(request, mongo):
    #Get name and description
    try:
        #name = request.POST["name"]
        csv_file = request.FILES["fileInput"]
        filename = unicode(csv_file)
        #description = request.POST.get("description", '')

    except MultiValueDictKeyError:
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})

    #if len(name) == 0:
    #    return helpers.gen_json_response({"status": "failed", "msg": "Name cannot be blank."})

    #Detect filetype
#    if re.search('\.csv$', filename.lower()):
    csv_text = csv_file.read()
    documents = models.convert_document_csv_to_bson(csv_text)

    for document in documents:
        J = models.get_new_document_json(document)
        #print json.dumps(J, cls=helpers.MongoEncoder, indent=2)
        mongo.get_collection("cvm_document").insert(J)

    return redirect('/admin/collections')

#!! Not sure about the status of this method.  Does it work?  Is it ever called from the code?
@helpers.admin_required
@helpers.uses_mongo
def import_collection(request, mongo):
    # Get name and description
    try:
        #name = request.POST["name"]
        #description = request.POST["description"]
        json_file = request.FILES["fileInput"]
        filename = unicode(json_file)

    except MultiValueDictKeyError:
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})

    text = json_file.read()
    print text
    print len(text)

    documents = json.loads(text, object_hook=json_util.object_hook)
    #contents = json.loads(file(f).read(), object_hook=json_util.object_hook)

    J = models.get_new_collection_json( name, description, documents )
    mongo.get_collection("cvm_collection").insert(J)
    #J = bson.decode(json_file.read())
    #J = json.loads(json_file.read())
    #print contents
    print json.dumps(J, cls=helpers.MongoEncoder, indent=2)
    return redirect('/admin/collections/')

#!! Not sure about the status of this method.  Does it work?  Is it ever called from the code?
@helpers.admin_required
@helpers.uses_mongo
def create_collection(request, mongo):
    #Get name and description
    try:
        name = request.POST["name"]
        description = request.POST.get("description", '')

    except MultiValueDictKeyError:
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})

    #Retrieve codebooks
    #!? Why are we retrieving codebooks here?
    total_docs = 0
    collections = {}
    for field in request.POST:
        if re.match('codebook_', field):
            try:
                val = int(request.POST[field])
                collections[field[9:]] = val
                total_docs += val
            except ValueError:
                return helpers.gen_json_response({"status": "failed", "msg": "Invalid entry in one or more codebook field(s)."})

    #Validate name
    if len(name) == 0:
        return helpers.gen_json_response({"status": "failed", "msg": "Name cannot be blank."})

    if total_docs == 0:
        return helpers.gen_json_response({"status": "failed", "msg": "Total document count must be greater than zero."})

    J = models.create_collection_json(name, description, collections)

    mongo.get_collection("cvm_collection").insert(J)

    #! Is this always the desired behavior?
    return redirect('/admin/collections/')

@helpers.admin_required
@helpers.uses_mongo
def get_collection_docs(request, mongo):
    #! Need to validate id field
    id_ = request.POST["id"]

    try:
        #Retrieve collection from database
        collection = mongo.get_collection("cvm_collection").find_one({"_id": ObjectId(id_)})

    except InvalidId:
        #Unless the ID is invalid
        return helpers.gen_json_response({"status": "failed", "msg": "Not a valid collection ID."})

    #Retrieve document content
    documents = []
    for doc_id in collection["doc_ids"]:
        document = mongo.get_collection("cvm_document").find_one({"_id": doc_id})
        documents.append(document)

    #Return result
    return helpers.gen_json_response({
            "status": "success",
            "msg": "Everything all good AFAICT.",
            "documents": documents,
            })

@helpers.admin_required
@helpers.uses_mongo
def update_collection(request, mongo):
    #Validate name and description
    try:
        id_ = request.POST["id_"]
        name = request.POST["name"]
        if len(request.POST["name"]) == 0:
            return helpers.gen_json_response({"status": "failed", "msg": "Name cannot be blank."})

        description = request.POST.get("description", '')

    except MultiValueDictKeyError:
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})

    #Retrieve and update collection object
    coll = mongo.get_collection("cvm_collection")
    J = coll.find_one({"_id": ObjectId(id_)})
    J["profile"]['name'] = name
    J["profile"]['description'] = description
    mongo.get_collection("cvm_collection").update({"_id": ObjectId(id_)}, J)

    #Return success message
    return helpers.gen_json_response({"status": "success", "msg": "Successfully updated collection."})

#!!! This method doesn't work since the database refactor.
#!!! Needs fixing.
@helpers.admin_required
@helpers.uses_mongo
def update_meta_data(request, mongo):
    #Updates collection meta data
    if request.method == 'POST':
        try:
            q = request.POST
            id_ = q.get("id_")
            doc_index = q.get("doc-index")
            keys = q.getlist("key")
            values = q.getlist("value")
        except MultiValueDictKeyError:
            return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})

        coll = mongo.get_collection("cvm_collection")
        t_coll = coll.find_one({"id_": ObjectId(id_)}, {"documents.metadata": 1, "documents": {"$slice": [doc_index, 1]}})
        for key, value in zip(keys, values):
            t_coll["documents"][0]["metadata"][key] = value

        #coll.update({"id_": ObjectId(id_)}, {"documents.metadata": 1, "documents": {"$slice": [doc_index, 1]}}, {"documents.$.metadata": t_coll})
        mongo.get_collection("cvm_collection").update(
        {"_id": ObjectId(id_)},
        {"$set": {'documents.' + str(doc_index) + '.metadata': t_coll}}
    )

        return helpers.gen_json_response({"status": "success", "msg": "Successfully updated collection."})
        
    #! Need handling for non-POST submission...?

@helpers.admin_required
@helpers.uses_mongo
def import_codebook(request, mongo):
    #Import direct from json
    try:
        json_file = request.FILES["fileInput"]

    except MultiValueDictKeyError:
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})

    #Convert file contents to json
    J = json.loads(json_file.read(), object_hook=json_util.object_hook)
    
    #If the json object has an "_id", remove it.
    if "_id" in J:
        del J["_id"]

    #Insert the new codebook
    mongo.get_collection("cvm_codebook").insert(J)
    
    #Redirect to /admin/codebooks/
    #! Is this always the desired behavior?
    return redirect('/admin/codebooks/')

@helpers.admin_required
@helpers.uses_mongo
def start_batch(request, mongo):
    #Validate form fields
    try:
        codebook_id = request.POST["codebook_id"]
        collection_id = request.POST.get("collection_id", None)
        pct_overlap = float(request.POST["pct_overlap"])
        replication = int(request.POST["replication"])
        old_batch_id = request.POST.get("comparison_batch_id", None)
    
    except MultiValueDictKeyError:
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})
    except ValueError:
        return helpers.gen_json_response({"status": "failed", "msg": "You have an improperly formatted number."})

    if not collection_id and not old_batch_id:
        return helpers.gen_json_response({"status": "failed", "msg": "Collection_id and batch_id cannot both be NULL."})

    try:
        pct_overlap = float(pct_overlap)
        assert pct_overlap >= 0
        assert pct_overlap <= 100
    except (AssertionError, ValueError) as e:
        return helpers.gen_json_response({"status": "failed", "msg": "Overlap must be a percentage between 0 and 100."})

    #Get a handle to the batch collection in mongo
    coll = mongo.get_collection("cvm_batch")

    #Count existing batches
    count = coll.find().count()

    #Retrieve the codebook and collection
    #! Pythonic coding: We can probably remove the "else: collection = None" clause
    codebook = mongo.get_collection("cvm_codebook").find_one({"_id": ObjectId(codebook_id)})
    if collection_id:
        collection = mongo.get_collection("cvm_collection").find_one({"_id": ObjectId(collection_id)})
    else:
        collection = None

    #! Pythonic coding: We can probably remove the "else: old_batch = None" clause
    if old_batch_id:
        old_batch = mongo.get_collection("cvm_batch").find_one({"_id": ObjectId(old_batch_id)})
    else:
        old_batch = None

    #Construct and save batch json object
    batch = models.logic.get_new_batch_json(count, pct_overlap, replication, codebook, collection, old_batch)
    add_new_collection = batch["add_new_collection"]
    del batch["add_new_collection"]
    batch_id = coll.save(batch)

    #print "batch_id is ", batch_id
    new_batch = mongo.get_collection("cvm_batch").find_one({"_id": ObjectId(batch_id)})
    #print json.dumps(new_batch, cls=helpers.MongoEncoder, indent=2)
    
    if new_batch:
        #print "add_new_collection is ", add_new_collection
        if add_new_collection == "yes":
            models.logic.gen_batch_responses_json(pct_overlap, replication, new_batch, collection)
        else:
            models.logic.gen_batch_responses_json(pct_overlap, replication, new_batch, None)

    #Return success message
    return helpers.gen_json_response({"status": "success", "msg": "New batch created."})

#! Needs updating
@helpers.admin_required
def update_batch_reliability(request):
    return helpers.gen_json_response({"status": "failed", "msg": "Nope.  You can't do this yet."})

#! This method is not thoroughly tested -- need label data first.
#! We probably need to do a DB refactor for batch coding, just like we did documents.
@helpers.admin_required
@helpers.uses_mongo
def compile_batch(request, mongo):
    #Validate batch_id field
    try:
        batch_id = request.POST["compile_batch_id"]

    except MultiValueDictKeyError:
        return helpers.gen_json_response({"status": "failed", "msg": "Missing field."})

    #Get a handle to the cvm_batch collection
    batch_db = mongo.get_collection("cvm_batch")

    #Count total batches
    count = batch_db.find().count()

    #Retrieve the batch
    current_batch = batch_db.find_one({"_id": ObjectId(str(batch_id))})
    index_compiled_batch = current_batch["profile"]["index"]
    codebook_id = current_batch["profile"]["codebook_id"]
    collection_ids = current_batch["profile"]["collection_ids"]
    doc_size = current_batch["profile"]["doc_size"]

    #Walk back up the batch inheritance tree to get all ancestor batches
    batch_list = []
    while current_batch["profile"]["parent_batch_id"]:
        batch_list.append(current_batch)
        current_batch = batch_db.find_one({"_id": current_batch["profile"]["parent_batch_id"]})
    batch_list.append(current_batch)

    #Compile all documents to a dictionary
    doc_dict = {}
    #Loop over batches
    for i,b in enumerate(batch_list):
        #Loop over documents within batches
        for d in b["documents"]:
            #Use the doc id as a  key
            key = str(d["document_id"])

            #For new keys, add the doc data structure
            #! Need testing here!
            if not key in doc_dict:
                doc_dict[key] = {
                    "document_id" : d["document_id"],
                    "labels" : {},
                }

            #Loop over labels
            for l in d["labels"]:
                #Generate a unique batch label
                label_key = str(i)+"_"+l#str(int(random.uniform(0,1)*10000))
                doc_dict[key]["labels"][label_key] = d["labels"][l]

#            doc_dict[key].values().append(d["labels"])

    #Fetch the values list from doc_dict
    docs = doc_dict.values()

    # index the docs
    for i,d in enumerate(docs):
        d["index"] = i

    #Generate compiled batch object and insert into database
    compiled_batch = models.generate_compiled_batch(count, index_compiled_batch, codebook_id, collection_ids, doc_size, docs)
    batch_db.insert(compiled_batch)

    #Return success message
    return helpers.gen_json_response({"status": "success", "msg": "Successfully compiled the batch."})



