'''
@author: jdrumgoole
'''
from agg import Agg

def countMakes( collection, output=None, limit=None ):
    #
    # expects a collection sorted by Make
    #
    
    a = Agg( collection )
    
    ageinusecs = { "$subtract" : [ "$TestDate", "$FirstUseDate" ] }
    ageinyears = { "$divide" :[ ageinusecs , (1000*3600*24*365) ] }
    floorage   = { "$floor" : ageinyears }
    ispass     = { "$cond" : [{"$eq": ["$TestResult","P"]},1,0]}
    
    projection = { "Make"         : 1,
                   "Model"        : 1,
                   "VehicleID"    : 1,
                   "TestResult"   : 1,
                   "TestDate"     : 1,
                   "TestMileage"  : 1,
                   "FirstUseDate" : 1,
                   "Age"          : floorage,
                   "pass"         : ispass }
    
    matcher = { "Age"   : { "$lt" : 20 }, "pass": { "$gt" : 0 }}
    
    grouper = { "_id" : "$Make", "total"   : { "$sum" : 1 },
                                 "passes"  : { "$sum" : "$pass"}, 
                                 "mileage" : { "$sum" : "$TestMileage" },
                                 "avgAge"  : { "$avg" : "$Age" }}
    
    return a.limit( limit ).project( projection ).match( matcher ).group( grouper ).out( output ).echo().aggregate()
