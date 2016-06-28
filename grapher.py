'''
@author: jdrumgoole
'''

age=[]
reliability=[]
labels = []
colours = []

from matplotlib import pyplot as pyplot

def graph( collection ):
    
    '''
    for collections like this:
    {u'_id': {u'age': 39.0, u'make': u'MERCEDES-BENZ'},
     u'count': 2,
     u'miles': 209459.0,
     u'passes': 2}
     
     Graph 
     '''

    
    for r in collection.find():
        #print( "Checking...")
        count = r['count']
        if count > 2000 :
            #print( "Plotting: %s" % r[ "Make"])
            m_id = r['_id']
            age.append(m_id['age'])
            if m_id[ 'age'] < 0 :
                print( "age: %i" % m_id[ 'age' ])
            passes = r['passes']
            passesToCountRatio = passes/float( count )
            if passesToCountRatio < 0 :
                print( "p to c : %f" % passesToCountRatio)
            reliability.append( passesToCountRatio )
            make = m_id['make']
            labels.append(make)
            colours.append(hash(make) % 65535)
    
    figure = pyplot.figure();
    axis = figure.add_subplot(111);
    axis.scatter(age,reliability,c=colours,picker=5,s=500,alpha=0.3)
    
    #axis.set_xlim(-5, 60 )
    
    def onpick(event):
        print labels[event.ind[0]]
    
    
    figure.canvas.mpl_connect('pick_event',onpick)
    pyplot.show()
    
if __name__ == "__main__" :
    
    import pymongo
    mc = pymongo.MongoClient()
    db = mc[ 'vosa']
    #graph(  db.cars_summary )
    graph(  db.carsByAgeAndMileage2013 )