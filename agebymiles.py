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

from agg import Agg

a = Agg( db.cars_summary_2013 )
a.match( { "count" : { "$gte" : 2000 }} )
a.sort( { "_id" : 1 } )
a.group( { "_id" : "$_id.make" , "years" : { "$push" : { "age" :"$_id.age", "miles" : "$miles" }}} )
a.out( "cars_milesperyear_2013")
results = a.aggregate()

figure = pyplot.figure();
axis = figure.add_subplot(111);

makes = {}
for r in db.cars_milesperyear_2013.find():
    
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
pyplot.xlabel( "Age")
pyplot.ylabel( "Miles Per Year")
pyplot.show()
