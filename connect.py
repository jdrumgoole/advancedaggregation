import pymongo
import pprint
import time
client = pymongo.MongoClient()
db = client.vosa
results2013 = db.results2013

time.sleep( 0.1)

print( "Client: '%s'" % client )


def cp( cursor, limit= 0 ):
    
    if ( isinstance( cursor, pymongo.cursor.Cursor ) or
       isinstance( cursor, pymongo.command_cursor.CommandCursor )):
        i = 0
        for x in cursor:
            if ( i != 0 ) and ( i == limit ):
                break
            pprint.pprint( x )
            print( "" )
            i = i + 1 
    else:
        pprint.pprint( cursor )

