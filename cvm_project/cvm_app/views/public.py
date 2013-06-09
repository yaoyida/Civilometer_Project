#! Need to remoev unused imports
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

from cvm_app.views import helpers

def signin(request):
    """Attempt to sign in via AJAX"""
    
    #Validate username and password
    try:
        username = request.POST['username']
        password = request.POST['password']
    except MultiValueDictKeyError:
        result = {"status": "failed", "msg": "Missing email or password.  Both fields are required."}
        return HttpResponse(json.dumps(result, indent=2), mimetype='application/json')

    #Attempt to authenticate
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Return a success message
            result = {"status": "success", "msg": "Sign in succeeded.  Welcome back, " + username}
        else:
            # Return a 'disabled account' error message
            result = {"status": "failed", "msg": "Sorry, this account has been disabled."}
    else:
        # Return an 'invalid login' error message.
        result = {"status": "failed", "msg": "Sorry, this username and password don't go together.  Try again?"}

    #Whatever the result, return it to the user
    return HttpResponse(json.dumps(result, indent=2), mimetype='application/json')

#This is only kinda sorta ajax, but it belongs with signin.
def signout(request):
    logout(request)
    return redirect('/')
    
@helpers.uses_mongo
def definitions(request, mongo):
    result = {
        'codebooks': list(mongo.get_collection("cvm_codebook").find()),
    }
    return render_to_response('public/definitions.html', result, context_instance=RequestContext(request))

@helpers.uses_mongo
def definition(request, mongo, collection_index):
    result = {
        'codebooks': list(mongo.get_collection("cvm_codebook").find()),
    }
    return render_to_response('public/definitions.html', result, context_instance=RequestContext(request))
