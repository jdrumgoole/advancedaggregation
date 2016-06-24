'''
Created on 20 May 2016

@author: jdrumgoole
'''

from pymongo import  *
from pprint import pprint
from matplotlib import pyplot as pyplot
import time
client = MongoClient()
db = client.vosa

filter = {"$match" : { "count" : { "$gte" : 2000 } } }
sort = {"$sort": { "_id" : 1 }}
groupmake = { "$group" : { "_id" : "$_id.make" , "years" : { "$push" : { "age" :"$_id.age", "miles" : "$miles" } } } }
results = db.cars_summary.aggregate([filter,sort,groupmake])

figure = pyplot.figure();
axis = figure.add_subplot(111);

makes = {}
for r in results:
    
    make = r['_id']
    age=[]
    miles=[]
    yeardata = r['years']
    for y in yeardata:
        age.append(y['age'])
        miles.append(y['miles'])
    tp = axis.plot(age,miles,picker=5)
    makes[tp[0]]=make

def onpick(event):
    artist = event.artist
    print makes[artist]

figure.canvas.mpl_connect('pick_event',onpick)
pyplot.show()
