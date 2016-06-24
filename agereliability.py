'''
Created on 19 May 2016

@author: jdrumgoole
'''
age=[]
reliability=[]
labels = []
colours = []

from pymongo import *

from pprint import pprint
from matplotlib import pyplot as pyplot
import time
client = MongoClient()
db = client.vosa

for r in db.summary.find():
    count = r['count']
    if count > 2000:
        m_id = r['_id']
        age.append(m_id['age'])
        passes = r['passes']
        reliability.append(passes/float(count))
        make = m_id['make']
        labels.append(make)
        colours.append(hash(make) % 65535)

figure = pyplot.figure();
axis = figure.add_subplot(111);
axis.scatter(age,reliability,c=colours,picker=5,s=80,alpha=0.3)

def onpick(event):
    print labels[event.ind[0]]


figure.canvas.mpl_connect('pick_event',onpick)
pyplot.show()
