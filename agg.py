'''

@author: jdrumgoole
'''
import pprint

class Agg(object):
    '''
    A wrapper class for the MongoDB Aggregation framework (MongoDB 3.2)
    '''

    def __init__(self, collection ):
        '''
        Constructor
        '''
        self._collection = collection
        self.clear()
        
        
    def _typeCheckDict( self, val ):
        if not isinstance( val, dict ):
            t = type( val )
            raise ValueError( "Parameters must be dict objects: %s is a %s object " % ( val, t ))
        
    def _hasDollarOutCheck(self, op ):
        if self._hasDollarOut :
            raise ValueError( "Cannot have more aggregation pipeline operations after $out: operation '%s'" % op )
        
    def limit(self, size=None):
        
        if size is None :
            return self
        
        self._hasDollarOutCheck( "limit: %i" % size )
        self._agg.append( { "$limit" : size })
        
        return self
    
    def sample(self, size=100):
        
        self._hasDollarOutCheck( "sample: %i" % size )
        self._agg.append( { "$sample" : { "size" : size  }})
        
        return self
    
    def match(self, matcher ):
        self._typeCheckDict( matcher )
        self._hasDollarOutCheck( "match: %s" % matcher )
        self._agg.append( { "$match" : matcher })
        
        return self
        
    def project(self, projector ):
        
        self._typeCheckDict( projector )
        self._hasDollarOutCheck( "project: %s" % projector )
        self._agg.append( {"$project": projector })
        
        return self
    
    def sort(self, sorter ):
        
        self._typeCheckDict( sorter )
        self._hasDollarOutCheck( "$sort: %s" % sorter )
        self._agg.append( { "$sort" : sorter })
        
        return self
    
    def group(self, grouper ):
        self._typeCheckDict( grouper )
        self._hasDollarOutCheck( "$group: %s" % grouper )
        self._agg.append( {"$group": grouper } )
        
        return self
    
    def clear(self):
        self._agg = []
        self._hasDollarOut = False
        
    def out(self, output=None ):
        
        if output is None :
            return self
        
        if self._hasDollarOut :
            raise ValueError( "Aggregation already has $out defined: %s" % self._agg )
        else:
            self._agg.append( { "$out" : output })
            self._hasDollarOut = True
            
        return self
    
    def echo(self):
        pprint.pprint( self._agg )
        return self
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return str( self._agg )
    
    def aggregate(self):
        
        return self._collection.aggregate( self._agg )
    
    def __call__(self ):
    
        return self.aggregate()
