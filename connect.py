import pymongo
import pprint
client = pymongo.MongoClient()
db = client.vosa
results2013 = db.results2013

def cp( cursor, limit= 1 ):
    
    if ( isinstance( cursor, pymongo.cursor.Cursor ) or
       isinstance( cursor, pymongo.command_cursor.CommandCursor )):
        i = 0
        for x in cursor:
            if i == limit:
                break
            pprint.pprint( x )
            print( "" )
            i = i + 1 
    else:
        pprint.pprint( cursor )

