import sqlobject
from sqlobject import *
import src.connection
from src.myString import myString

# This class encapsulates methods to manipulate data entries
# Including import / export methods

class BusinessEntry(SQLObject):
    businessName = StringCol()
    marketingName = StringCol()
    category = StringCol()


    def toCSV(self):
        set = [self.businessName, self.marketingName, self.category]
        if (len(set) > 0):
            print("") #(",".join(set))
