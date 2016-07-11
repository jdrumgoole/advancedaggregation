'''
@author: jdrumgoole
'''
from agg import Agg

def carsByAgeAndMileage( collection ):
    
    ageinusecs = { "$subtract" : [ "$TestDate", "$FirstUseDate" ] }
    ageinyears = { "$divide" :[ ageinusecs , (1000*3600*24*365) ] }
    floorage   = { "$floor" : ageinyears }
    ispass     = { "$cond" : [{"$eq": ["$TestResult","P"]},1,0]}
    
    proj = { "Make"        : 1,
             "Model"       : 1,
             "VehicleID"   : 1,
             "TestResult"  : 1,
             "TestDate"    : 1,
             "TestMileage" : 1,
             "FirstUseDate": 1,
             "Age"         : floorage,
             "pass"        : ispass }

    group = { "_id"    : { "make": "$Make",  "age" : "$Age" }, 
              "count"  : {"$sum":1} , 
              "miles"  : {"$avg":"$TestMileage"},
              "passes" : {"$sum":"$pass"}}
    
    sorter = { "count" : -1 }

    a = Agg( collection )
    a.project( proj ).group( group ).sort( sorter)

    return a

def cbam( collection ):
    return carsByAgeAndMileage( collection ).aggregate()
