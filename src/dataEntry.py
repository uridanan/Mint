import sqlobject
from sqlobject import *
import src.connection
from src.myString import myString

# This class encapsulates methods to manipulate data entries
# Including import / export methods

class DataEntry(SQLObject):
    date = DateCol()
    partner = StringCol()
    refId = StringCol()
    credit = DecimalCol(size=10, precision=2)
    debit = DecimalCol(size=10, precision=2)
    balance = DecimalCol(size=10, precision=2)

    def toCSV(self):
        set = [self.date, self.partner, self.refId, self.credit, self.debit, self.balance]
        if (len(set) > 0):
            print("") #(",".join(set))
