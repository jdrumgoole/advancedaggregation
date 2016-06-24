


age=[]
reliability=[]
labels = []
colours = []

for r in db.summary.find():
    count = r['count']
    if count > 2000:
        m_id = r['_id']
        age.append(id['age'])
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

filter = {"$match" : { "count" : { "$gte" : 2000 } } }
sort = {"$sort": { "_id" : 1 }}
groupmake = { "$group" : { "_id" : "$_id.make" , "years" : { "$push" : { "age" :"$_id.age", "miles" : "$miles" } } } }
results = db.summary.aggregate([filter,sort,groupmake])

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

miles=[]
reliability=[]
labels = []
colours = []

for r in db.summary.find():
    count = r['count']
    if count > 2000:
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
