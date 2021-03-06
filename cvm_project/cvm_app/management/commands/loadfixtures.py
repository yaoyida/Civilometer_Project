#from django.core.management.base import BaseCommand, CommandError
from django.core import management
#from django.db import connections
from django.conf import settings

import json, glob, bson
from bson import json_util
#import pymongo.json_util

from pymongo import Connection
import pymongo.errors

class Command(management.BaseCommand):
    """Flush and initialize, or re-initialize, the database."""
    args = '<...>'
    help = 'Loads database fixtures'

    def handle(self, *args, **options):
        if 'verbosity' in options:
            verbosity = options['verbosity']
        else:
            verbosity = 1
        
        #Get DB connection
        #conn = connections["default"]
        db_name = settings.DATABASES['default']['NAME']
        conn = Connection()

        #Flush database
        #management.call_command('flush', interactive=False)

        conn.drop_database(db_name)

        #Sync database
        management.call_command('syncdb', interactive=False, verbosity=verbosity)

        #Ensure indexes
        #This is right to ensure an index *using* a subelement
        #conn[db_name]['cvm_batch'].ensure_index('profile.index', unique=True)
        #Ensuring indexes *within* subelements is not possible

        if len(args) > 0:
            subdirectory = args[0] + "/"
            if verbosity > 0 :
                print 'Selected fixtures subdirectory', args[0]
        else:
            subdirectory = ""
            if verbosity > 0 :
                print 'Using default fixtures directory'

        #Get all fixtures
        fixture_path = settings.PROJECT_PATH+'/fixtures/'+subdirectory
        if verbosity > 0 :
            print 'Loading fixtures from', fixture_path+'*'
        fixtures = glob.glob(fixture_path+'*.json')

        for f in fixtures:
            name = f.split('/')[-1].split('.')[0]
            if verbosity > 0 :
                print '\tLoading fixtures for collection', name, '...'
            
            contents = json.loads(file(f).read(), object_hook=json_util.object_hook)
            #conn.get_collection(name).insert(contents)
            
            try:
                conn[db_name][name].insert(contents)
            except pymongo.errors.InvalidOperation:
                if verbosity > 0 :
                    print "\t\tThe json file for", name, "appears to be empty.\n"


#        management.call_command('syncdb', interactive=False)

