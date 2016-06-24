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

miles=[]
reliability=[]
labels = []
colours = []

for r in db.cars_summary.find():
    count = r['count']
    if count > 2000:
        if r["miles"] < 150000 :
            id = r['_id']
            miles.append(r['miles'])
            passes = r['passes']
            reliability.append(passes/float(count))
            make = id['make']
            labels.append(make)
            colours.append(hash(make) % 65535)

figure = pyplot.figure();
axis = figure.add_subplot(111);
axis.scatter(miles,reliability,c=colours,picker=5,s=80,alpha=0.3)

def onpick(event):
    print labels[event.ind[0]]


figure.canvas.mpl_connect('pick_event',onpick)
pyplot.show()
