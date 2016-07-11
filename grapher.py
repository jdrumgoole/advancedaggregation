'''
@author: jdrumgoole
'''

age=[]
reliability=[]
labels = []
colours = []

from matplotlib import pyplot as pyplot

def graphAvgPassesAge( collection ):
    
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
            passes = r['passes']
            passesToCountRatio = passes/float( count )
            #print( "passesToCountRatio: %f" % passesToCountRatio )
            reliability.append( passesToCountRatio )
            make = m_id['make']
            labels.append(make)
            colours.append(hash(make) % 65535)
    
    figure = pyplot.figure();
    axis = figure.add_subplot(111);
    axis.scatter(age,reliability,c=colours,picker=5,s=80,alpha=0.3)
    axis.set_xlim([ 0, 30])
    axis.set_ylim([0.2, 1])
   
    pyplot.xlabel( "Age")
    pyplot.ylabel( "Pass Ratio")
    #axis.set_xlim(-5, 60 )
    
    def onpick(event):
        print labels[event.ind[0]]
    
    
    figure.canvas.mpl_connect('pick_event',onpick)
    pyplot.show()
    
def graphAvgMilesByAge( collection ):
    
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
        total = r['total']
        if total > 2000 :
            #print( "Plotting: %s" % r[ "Make"])
            age.append( r['avgAge'])
            
            carsToMileageRatio = r["total"]/float( r[ "mileage"])
            print( "carsToMileageRatio: %f" % carsToMileageRatio )
            reliability.append( carsToMileageRatio )
            make = r[ "_id" ] 
            labels.append(make)
            colours.append(hash(make) % 65535)
    
    figure = pyplot.figure();
    axis = figure.add_subplot(111);
    axis.scatter(age,reliability,c=colours,picker=5,s=80,alpha=0.3)
    
    axis.set_xlim([0, 20])
    axis.set_ylim([0, 0.00008])
   
    pyplot.xlabel( "Age")
    pyplot.ylabel( "Average miles per car")
    
    def onpick(event):
        print labels[event.ind[0]]
    
    
    figure.canvas.mpl_connect('pick_event',onpick)
    pyplot.show()


graphAvgPassesAge( db.cars_summary_2013 )

##if __name__ == "__main__" :
##     
##    import pymongo
##    mc = pymongo.MongoClient()
##    db = mc[ 'vosa']
##    graphAvgPassesAge( db.cars2013 )
##    graphAvergPasses(  db.cars_summary )
##    graphAvgMilesByAge(  db.makes2013 )
