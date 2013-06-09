from django.core import management
from django.conf import settings

import json, glob, bson, re, datetime
from bson import json_util
import subprocess

from pymongo import Connection
from cvm_app import helpers

### boto/mturk imports ###

from collections import defaultdict
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from boto.mturk.connection import MTurkConnection
from boto.mturk.price import Price
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, NumberHitsApprovedRequirement, LocaleRequirement
from boto.mturk.question import ExternalQuestion

### Import credentials ###
from local import cred

class Command(management.BaseCommand):
    """Dump auth_user, tb_app_codebook, tb_app_collection, and tb_app_batch collections to files."""
    args = '<...>'
    help = 'Handle mturk integration'

    def handle(self, *args, **options):
        #Get DB connection
        db_name = settings.DATABASES['default']['NAME']
        self.db_conn = Connection()[db_name]
        
        self.mt_conn = MTurkConnection(cred.diss_key, cred.diss_secret_key, host=cred.host)
        print 'MTurk API endpoint :', self.mt_conn

        if args:
            try:
                self.__class__.__dict__[re.sub('-', '_', args[0])](self, *args[1:])
            except KeyError:
                print "No function called", args[0], "exists."

    def create_hit_type(self, *args):
        print "Creating HIT Type..."
        
        #Set up qualifications
        my_qual_req = Qualifications()
        #my_qual_req.add(PercentAssignmentsApprovedRequirement("GreaterThan", 85))
        #my_qual_req.add(NumberHitsApprovedRequirement("GreaterThan", 100))
        #my_qual_req.add(LocaleRequirement("EqualTo", "US"))
        
        #Create json object for storage to mongo
        J = {
            'title' : "Read a blog post or news article and answer questions about it",
            'description' : "Read a short blog post or news article and answer questions about it. These are quick HITs, and there are going to be a lot of them.  Bonuses for accurate answers!",
            'reward' : 0.06,
            'duration' : 3600,
            'keywords' : "blog, news, article, quick, easy, bonus, civility",
            'approval_delay' : 2592000,
            'qual_req' : [req.__dict__ for req in my_qual_req.requirements],
        }

        #Register HIT type on mongo
        HT_id = self.mt_conn.register_hit_type(
            title = J["title"],
            description = J["description"],
            reward = Price(J["reward"]),
            duration = J["duration"],
            keywords = J["keywords"],
            approval_delay = J["approval_delay"],
            qual_req = my_qual_req,
        )
        
        #Retrieve the HITTypeId
        J["hittypeid"] = HT_id[0].HITTypeId
        J["created_at"] = datetime.datetime.now()

#        print json.dumps(J, cls=helpers.MongoEncoder, indent=2)
        print "\tHIT Type created with ID", J["hittypeid"]
        
        #Save the object to mongo
        db_id = self.db_conn['cvm_mturk_hittypeid'].insert(J)
        print "\tHIT Type stored to database with ID ", db_id

        return 1

    def list_hit_types(self):
        #? Is it possible to list hit types from mturk?
        J = list(self.db_conn['cvm_mturk_hittypeid'].find())
        print json.dumps(J, cls=helpers.MongoEncoder, indent=2)

        print "\nID list:"
        print [j["hittypeid"] for j in J]

    def list_batches(self):
        J = list(self.db_conn["cvm_batch"].find({},{"profile":1, "reports.progress":1}))        
        print json.dumps(J, cls=helpers.MongoEncoder, indent=2)

        print "\nID list:"
        print [str(j["_id"]) for j in J]

    def publish_hits(self, hit_type, count):
        count = int(count)
        
        print hit_type
        print count

#        assert False

        for i in range(count):
#            url = 'http://civilometer.com/tasks/mturk/'
#            url += '?source_url=' + urllib.quote(source_url)
#            url += '&amp;source_type=' + urllib.quote(source_type)

            #http://alexeymk.com/xsanyuri-doesnt-allow-ampersands
            q_form = ExternalQuestion(cred.url, 800)

            r = self.mt_conn.create_hit(
                hit_type= hit_type,
                question= q_form,
                max_assignments=1,
                annotation="",
            )
            
            print r

#            group_size += 1

#        db_id = self.db_conn['cvm_mturk_hittypeid'].insert(J)

#        row = [str(x) for x in [group_id, publish_time, args.batch, args.codebook, base_url, group_size]]
#        log_file = file('log/chowderhead.log','a')
#        log_file.write('\t'.join(row)+'\n')


        #create_hit(hit_type=None, question=None, lifetime=datetime.timedelta(7), max_assignments=1, title=None, description=None, keywords=None, reward=None, duration=datetime.timedelta(7), approval_delay=None, annotation=None, questions=None, qualifications=None, response_groups=None)
        #Creates a new HIT. Returns a ResultSet See: http://docs.amazonwebservices.com/AWSMechanicalTurkRequester/2006-10-31/ApiReference_CreateHITOperation.html
    
    def list_hits(self):
        #get_assignments(hit_id, status=None, sort_by='SubmitTime', sort_direction='Ascending', page_size=10, page_number=1, response_groups=None)
        pass
    
    def delete_all_hits(self):
        pass

    def award_bonuses(self):
        
        #self.mt_conn.grant_bonus(worker_id, assignment_id, bonus_price, reason)
        pass
