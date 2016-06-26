'''

Aggregation operator that creates an MOT collection that only contains valid
first use dates. No NULL values. This allows use to accurately calculate the age
of a vehicle.

@author: jdrumgoole
'''
from agg import Agg

def dataCleanse( collection, output=None, limitSize=None ):
    
    #
    # Create a collection of clean vehicles with good dates
    #
    matcher = { "FirstUseDate" : { "$ne" : "NULL" }, 
                "Make"         : { "$ne" : "UNCLASSIFIED" }, 
                "Model"        : { "$ne" : "UNCLASSIFIED" },
                "TestClassID"  : "4" }
                
    x = Agg( collection )
    return x.limit( limitSize ).match( matcher).out( output ).aggregate()
