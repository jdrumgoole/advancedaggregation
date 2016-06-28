'''
@author: jdrumgoole
'''
from agg import Agg

def cbam( collection ):
    return carsByAgeAndMileage( collection,  output="carsByAgeAndMileage2013", limit=None )

def carsByAgeAndMileage( collection, output=None, limit=None):
    
    ageinusecs = { "$subtract" : [ "$TestDate", "$FirstUseDate" ] }
    ageinyears = { "$divide" :[ ageinusecs , (1000*3600*24*365) ] }
    floorage   = { "$floor" : ageinyears }
    ispass     = { "$cond" : [{"$eq": ["$TestResult","P"]},1,0]}
    
    projection = { "Make": 1, "Model" : 1, "VehicleID" : 1, "TestResult": 1, "TestDate": 1,
                   "TestMileage": 1,"FirstUseDate":1,"Age":floorage,"pass":ispass }
    
    '''
    Cars that are 10 yrs old or less
    '''
    
    matcher = { "Age"   : { "$lt" : 10 }, 
                "Model" : { "$ne" : "UNCLASSIFIED"}, 
                "Make"  : { "$ne" : "UNCLASSIFIED"}}

    grouper = { "_id"    : { "make": "$Make", "model": "$Model", "age" : "$Age" }, 
                "count"  : {"$sum":1} , 
                "miles"  : {"$avg":"$TestMileage"},
                "passes" : {"$sum":"$pass"}}
    
    sorter = { "count" : -1 }

    a = Agg( collection )
    return a.limit( limit ).project( projection ).match( matcher ).group( grouper ).sort( sorter).out(output).echo().aggregate()