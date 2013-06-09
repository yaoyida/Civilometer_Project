"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from django.db import connections

import unittest
import json

"""
from bson.objectid import ObjectId
import csv, re, json, datetime, random
from cvm_app import models

class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

class SimpleTest(TestCase):
    def setUp(self):
        #call_command('loadfixtures', 'small-fixtures')
        pass
    
    def test_update_game_score(self):
        old_game_stats = {
            'total_score': 100.,
            'avg_score': .5,
            'tasks_completed': 100,
            'scored_tasks': 20,
            'bonus_credits': 0,
            'tasks_remaining': 400,
        }

        #No new score
        new_game_stats = models.update_game_stats(old_game_stats)
        self.assertEqual(new_game_stats["scored_tasks"], old_game_stats["scored_tasks"])
        self.assertEqual(new_game_stats["avg_score"], old_game_stats["avg_score"])
        self.assertEqual(new_game_stats["tasks_completed"], old_game_stats["tasks_completed"]+1)
        self.assertEqual(new_game_stats["total_score"], new_game_stats["avg_score"]*new_game_stats["tasks_completed"])

        #New score, worse than old average
        new_game_stats = models.update_game_stats(old_game_stats, 0)
        self.assertEqual(new_game_stats["scored_tasks"], old_game_stats["scored_tasks"]+1)
        self.assertTrue(new_game_stats["avg_score"] < old_game_stats["avg_score"])
        self.assertEqual(new_game_stats["tasks_completed"], old_game_stats["tasks_completed"]+1)
        self.assertEqual(new_game_stats["total_score"], new_game_stats["avg_score"]*new_game_stats["tasks_completed"])

        #New score, better than old average
        new_game_stats = models.update_game_stats(old_game_stats, 1)
        self.assertEqual(new_game_stats["scored_tasks"], old_game_stats["scored_tasks"]+1)
        self.assertTrue(new_game_stats["avg_score"] > old_game_stats["avg_score"])
        self.assertEqual(new_game_stats["tasks_completed"], old_game_stats["tasks_completed"]+1)
        self.assertEqual(new_game_stats["total_score"], new_game_stats["avg_score"]*new_game_stats["tasks_completed"])

        #New score, negative
        new_game_stats = models.update_game_stats(old_game_stats, -1)
        self.assertEqual(new_game_stats["scored_tasks"], old_game_stats["scored_tasks"]+1)
        self.assertTrue(new_game_stats["avg_score"] < old_game_stats["avg_score"])
        self.assertEqual(new_game_stats["tasks_completed"], old_game_stats["tasks_completed"]+1)
        self.assertEqual(new_game_stats["total_score"], new_game_stats["avg_score"]*new_game_stats["tasks_completed"])

        #No prior stats
        old_game_stats = {
            'total_score': 0.,
            'avg_score': 0.,
            'tasks_completed': 0,
            'scored_tasks': 0,
            'bonus_credits': 0,
            'tasks_remaining': 400,
        }

        #No new score
        new_game_stats = models.update_game_stats(old_game_stats)
        self.assertEqual(new_game_stats["scored_tasks"], 0)
        self.assertEqual(new_game_stats["avg_score"], 0)
        self.assertEqual(new_game_stats["tasks_completed"], 1)
        self.assertEqual(new_game_stats["total_score"], 0)

        #New score
        new_game_stats = models.update_game_stats(old_game_stats, .7)
        self.assertEqual(new_game_stats["scored_tasks"], 1)
        self.assertEqual(new_game_stats["avg_score"], .7)
        self.assertEqual(new_game_stats["tasks_completed"], 1)
        self.assertEqual(new_game_stats["total_score"], .7)

    def test_get_batch_documents_json(self):
        call_command('loadfixtures', 'small-fixtures')
        mongo = connections["default"]

        pct_overlap, replication = .7, 3
        collection = mongo.get_collection("cvm_collection").find_one()
        batch = mongo.get_collection("cvm_batch").find_one()

        docs = models.get_batch_documents_json( pct_overlap, replication, collection )#, batch )
#        print json.dumps(docs, indent=2, cls=MongoEncoder)

    def test_game_sessions(self):
        c = Client()
        call_command('loadfixtures', 'small-fixtures')
        response = c.post('/ajax/sign-in/', {'username': 'admin', 'password': '1234'})
        response = c.post('/ajax/create-account/', {'username': 'john', 'email': 'smith@asdasd.com', 'first_name':'A', 'last_name':'b',  'admin':"1"})
        response = c.post('/sign-out/')
        response = c.post('/ajax/sign-in/', {'username': 'john', 'password': 'john'})

        J = {
            "user" : {
		        "screen_info" : {
			        "browser" : {
				        "webkit" : True,
				        "version" : "536.11",
				        "safari" : True
			        },
			        "random" : 0.9406628250144422,
			        "screen_width" : 1280,
			        "screen_height" : 1024
		        },
		        "user_type" : "member"
            },
            'batch_id': '5012f12e0a665e12d4a6f296',
            'csrfmiddlewaretoken': '0000xxxx',
        }

        J_string = json.dumps(J)
        #response = c.post('/tasks/ajax/create-game-session/', data=J_string )
        
        response = c.post('/tasks/ajax/create-game-session/', content_type='application/json', data=J_string)

#        response = c.post('/tasks/ajax/create-game-session/',
#                            {'form':J_string},
#                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    #http://stackoverflow.com/questions/4794457/unit-testing-django-json-view


    def test_kripp(self):
        #array = [[1], [2,2],[1,1],[3,3],[3,3,4],[4,4,4],[1,3],[2,2],[1,1],[1,1],[3,3],[3,3],[],[3,4]]
        #print "nominal alpha: %.4f" % alpha(array,nominal)
        #print "ordinal alpha: %.4f" % alpha(array,ordinal)
        #print "interval alpha: %.4f" % alpha(array,interval)
        from cvm_app.algorithms import kripp

        #Wikipedia example
        array_1 = [[1], [2,2],[1,1],[3,3],[3,3,4],[4,4,4],[1,3],[2,2],[1,1],[1,1],[3,3],[3,3],[],[3,4]]
        self.assertAlmostEqual( kripp.alpha( array_1, kripp.nominal ), 0.691358024691 )
        self.assertAlmostEqual( kripp.alpha( array_1, kripp.interval ), 0.810844892812 )

        #Perfect agreement
        array_2 = [[2,2],[1,1],[3,3]]
        self.assertEqual( kripp.alpha( array_2, kripp.nominal ), 1 )
        self.assertEqual( kripp.alpha( array_2, kripp.interval ), 1 )
        self.assertEqual( kripp.alpha( array_2, kripp.ratio ), 1 )
"""

class SimpleTest(TestCase):
    def setUp(self):
        pass

    def test_import_views(self):
#        import cvm_app.models.gen as cvm_models_gen
        
        import cvm_app.models as models
        print '*'*80
        print len(models.__dict__.keys())#.gen#.user_profile('user_name', 'lane_seed')
        
        import cvm_app.views
        #print cvm_models_gen.__dict__
        pass

##### Tests for views #########################################################

class PageRenderTest(unittest.TestCase):
    # Make sure all public pages render
    # Test login/logout sequence
    # Make sure all member pages render, with appropriate permissions
    # Make sure all admin pages render, with appropriate permissions

    @classmethod
    def setUpClass(cls):
        call_command('loadfixtures', 'test-1')

    def setUp(self):
#        call_command('loadfixtures', 'test-1')
        self.client = Client()

    def test_public_pages(self):
        self.client.get('/')
        self.client.get('/how-it-works/')
        self.client.get('/play-with-data/')
        self.client.get('/get-involved/')
        self.client.get('/definitions/')
        self.client.get('/gallery/')

    def test_sign_in(self):
        #Right password
        response = self.client.post('/ajax/sign-in/', {'username': 'admin', 'password': '1234'} )
        self.assertEqual(json.loads(response.content)["status"], "success")
        
        #! Verify login against user...
        
        self.client.post('/sign-out/')

        #! Verify logout against request object...
        
        #Wrong password
        response = self.client.post('/ajax/sign-in/', {'username': 'admin', 'password': 'wrongpw'})
        self.assertEqual(json.loads(response.content)["status"], "failed")

        #! Verify not-logged in against request object...

    def test_member_pages(self):
        pass

    def test_admin_pages(self):
        #Logged in as admin
        self.client.post('/ajax/sign-in/', {'username': 'admin', 'password': '1234'} )

        self.assertEqual( self.client.get('/admin/').status_code, 200 )
        self.assertEqual( self.client.get('/admin/users/').status_code, 200 )
        self.assertEqual( self.client.get('/admin/codebooks/').status_code, 200 )
        self.assertEqual( self.client.get('/admin/collections/').status_code, 200 )
        self.assertEqual( self.client.get('/admin/batches/').status_code, 200 )

        #! Need to test object view pages (e.g. /admin/user/agong )

        #Not logged in
        self.client.post('/sign-out/')

        self.assertEqual( self.client.get('/admin/').status_code, 403 )
        self.assertEqual( self.client.get('/admin/users/').status_code, 403 )
        self.assertEqual( self.client.get('/admin/codebooks/').status_code, 403 )
        self.assertEqual( self.client.get('/admin/collections/').status_code, 403 )
        self.assertEqual( self.client.get('/admin/batches/').status_code, 403 )

        #! Need to test object view pages (e.g. /admin/user/agong )
        

class AjaxTest(TestCase):
    def setUp(self):
        call_command('loadfixtures', 'empty-init')
        self.client = Client()
        self.client.post('/ajax/sign-in/', {'username': 'admin', 'password': '1234'} )

    def test_create_user(self):
        j = {
            'csrfmiddlewaretoken': 'c08d8b1d54c4a91b380be2915baa0f71',
            'username': 'agong',
            'first_name': 'Abe', 
            'last_name': 'Gong',
            'email': 'agong@umich.edu'
        }
        
        response = self.client.post('/ajax/create-account/', j )
        self.assertEqual(json.loads(response.content)["status"], "success")

class ApiTest(TestCase):
    # Make sure all API calls work, with appropriate permissions
        #Security on public-facing (i.e., no "@admin_required) API calls needs to be extra tight
        #Security on API calls with DB writes needs to be *extra* tight
    def setUp(self):
        call_command('loadfixtures', 'test-2')
        self.client = Client()
        self.client.post('/ajax/sign-in/', {'username': 'admin', 'password': '1234'} )

    def test_mapreduce_query(self):
        response = self.client.post('/api/mapreduce-query/')
        self.assertEqual(json.loads(response.content)["status"], "success")
        
class TaskSequenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        call_command('loadfixtures', 'test-1', verbosity=0)
        
    def setUp(self):
        self.client = Client()
        
    # Make sure all task sequence works properly with an anonymous user
    def test_anonymous(self):
        self.client.post('/sign-out/')

        self.client.get('/tasks/')
        self.client.get('/tasks/choose-task/')
        #self.client.get('/tasks/game-session/'+gs_id)
        #self.client.post('/tasks/ajax/get-first-task/')
        #self.client.post('/tasks/ajax/submit-task/')     

    # Make sure all task sequence works properly with a member user
    def test_member(self):
        self.client.post('/ajax/sign-in/', {'username': 'admin', 'password': '1234'} )

        self.client.get('/tasks/')
        self.client.get('/tasks/choose-task/')
        #self.client.get('/tasks/game-session/'+gs_id)
        #self.client.post('/tasks/ajax/get-first-task/')
        #self.client.post('/tasks/ajax/submit-task/')
        
    # Make sure all task sequence works properly with an mturk user
    def test_mturk(self):
        #! What would happen if an mturk user was also signed in?
        self.client.post('/sign-out/')

        #No AssignmentId
        self.client.get('/tasks/mturk/')

        #! Has AssignmentId (need to write this)
        self.client.post('/ajax/sign-in/', {'username': 'admin', 'password': '1234'} )
        self.create_batch()

        response = self.client.get('/tasks/mturk/?assignmentId="afefefadfefe"&workerId="afefefefea"')
        print response.request["PATH_INFO"]
        
        response = self.client.post('/tasks/ajax/get-first-task/')
        print response
        response = self.client.post('/tasks/ajax/get-first-task/')
        print response
        
        
        submit = {
            "game_session_id":"502e4c932fa6cd0abf000000",
            "csrfmiddlewaretoken":"c08d8b1d54c4a91b380be2915baa0f71",
            "document_id":"502005ee0a665e0efae37c2c",
            "labels":{"Q1_1_rmatrix":"3","Q1_2_rmatrix":"3","Q1_3_rmatrix":"2","Q2_scope":"2","Q3_response":"3","Q4_notes":""}
        }

        #self.client.post('/tasks/ajax/submit-task/')     
        pass

    # Make sure all task sequence works properly with an anonymous user
    def test_create_batch(self):
        """ Assumes that cvm_responses is empty in the initial fixtures """
        self.client.post('/ajax/sign-in/', {'username': 'admin', 'password': '1234'} )
        response = self.create_batch()

        self.assertEqual( response.status_code, 200 )
        self.assertEqual(json.loads(response.content)["status"], "success")
        
        mongo = connections["default"]
        self.assertEqual( mongo.get_collection("cvm_response").count(), 10 )

        #! Need more testing here...

    def create_batch(self):
        J = {
            'codebook_id' : "500edd2833679d206395fbdd",
            'collection_id' : "502005d20a665e0efae37bc5",
#            'comparison_batch_id': '',
            'pct_overlap' : 40,
            'replication' : 3,
        }
        return self.client.post('/ajax/start-batch/', J )        

    def create_batch_with_comparison(self):
        pass
        
##### Tests for models ########################################################

class ModelTest(TestCase):
    #Test logic for each model method (Hard, but important!)

    def setUp(self):
        pass

    def test_import(self):
        from cvm_app import models
