'''
Created on 19 May 2016

@author: jdrumgoole
'''
from pymongo import *

from pprint import pprint
from matplotlib import pyplot as pyplot
import time
client = MongoClient()
db = client.vosa
db.results_2013.count()
doc = db.results_2013.find_one()
pprint(doc)

'''
Some calculations we will use in the script
'''

ageinusecs = { "$subtract" : [ "$TestDate", "$FirstUseDate" ] }
ageinyears = { "$divide" :[ ageinusecs , (1000*3600*24*365) ] }
floorage = { "$floor" : ageinyears }
ispass =  { "$cond" : [{"$eq": ["$TestResult","P"]},1,0]}
project = { "$project" : { "Make":1, "Model" : 1, "VehicleID" : 1, "TestResult":1, "TestDate":1,"TestMileage":1,"FirstUseDate":1,"Age":floorage,"pass":ispass }}
results = db.results_2013.aggregate([project,{"$limit":5}])
pprint(list(results))

'''
1  : Small Motor cycles
2  : large Motor cycles
3  : three wheeled vehicles
4  : Cars
4A : Cars with weird seat belts
5  : Private passenger vehicles
5A : passenger vehicles with weird seat belts
7  : Goods vehicles
'''


#
# collection with valud first use dates

removeNulls = { "$match" : { "FirstUseDate" : { "$ne" : "NULL" }}}
goodDates = { "$out" : "goodDates" }

carsonly = { "$match" : { "TestClassID" : 4 }}

carsWithPasses = { "$match" : { "TestClassID" : { "$eq" : "4" }, "TestResult" : "P" }}# , {"TestResult" : "P" }}

knownage = { "$match" : {  "FirstUseDate" : { "$ne" : "NULL" }}}
onlyPasses = { "$match" : { "pass" : 1 }}

#
# Group by make and age. Find the total number and their average mileage.
#
group = { "$group" : { "_id" : { "make": "$Make", "age" : "$Age" }, "count" : {"$sum":1} , "miles": {"$avg":"$TestMileage"},"passes":{"$sum":"$pass"}}}

#
# Group by make, age and model.
#
groupModel = { "$group" : { "_id" : { "make": "$Make", 'model' : "$Model",  "age" : "$Age" }, "count" : {"$sum":1} , "miles": {"$avg":"$TestMileage"},"passes":{"$sum":"$pass"}}}

out = { "$out" : "cars_summary" }

#main
avgMilesPerMake = { "$group" : { "_id" : "$Make", "avgMiles" : { "$avg" : "$TestMileage"}}}
#Summary
countPasses = { "$group" : { "_id" : "$_id.make", "passCount" : {"$sum" : "$passes" }}} 

countVehicles = { "$group" : { "_id" : "$VehicleID", "count" : { "$sum" : 1 }}}
countMakes = { "$group" : { "_id" : "$Make"} , "total" : {"$sum" : 1 }}

countMiles = { "$group" : { "_id" : "$Make" , "totalMileage" : {"$sum" : "$TestMileage" }}}


cars_summary = db.cars_2013.aggregate( [ project, group, out ])

sort = { "$sort": "passCount "}
t0 = time.time()
results = db.results_2013.aggregate([carsonly,knownage,project,group,out])
#results = db.mot_results.aggregate([carsonly, out])

print time.time() - t0