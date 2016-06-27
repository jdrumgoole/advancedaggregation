'''
@author: jdrumgoole
'''

from agg import Agg

def cars( collection ):
    return SummaryCollection( collection, output="carsByAgeAndMileage2013", limit=None )

def SummaryCollection( collection, limit=1000, output=None ):
    
    match = { "FirstUseDate" : { "$ne" : "NULL" }}
    
    ageinusecs = { "$subtract" : [ "$TestDate", "$FirstUseDate" ] }
    ageinyears = { "$divide" :[ ageinusecs , (1000*3600*24*365) ] }
    floorage = { "$floor" : ageinyears }
    ispass =  { "$cond" : [{"$eq": ["$TestResult","P"]},1,0]}
    project = { "Make":1, "Model" : 1, "VehicleID" : 1, "TestResult":1, "TestDate":1,"TestMileage":1,"FirstUseDate":1,"Age":floorage,"pass":ispass }

    #
    # Group by make and age. Find the total number and their average mileage.
    #
    group = { "_id" : { "make": "$Make", "age" : "$Age" }, "count" : {"$sum":1} , "miles": {"$avg":"$TestMileage"},"passes":{"$sum":"$pass"}}

    a = Agg( collection )
    
    return a.limit( limit ).match( match ).project( project ).group( group ).out( output ).echo().aggregate()