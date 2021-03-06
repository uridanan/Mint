from sqlobject import *


# This class encapsulates methods to manipulate data entries
# Including import / export methods

class BankEntry(SQLObject):
    date = DateCol()
    business = IntCol()
    refId = StringCol()
    hide = IntCol()
    credit = DecimalCol(size=10, precision=2) #use CurrencyCol?
    debit = DecimalCol(size=10, precision=2)
    balance = DecimalCol(size=10, precision=2)
    trackerId = IntCol()
    userId = StringCol()

    def toCSV(self):
        set = [self.date, self.refId, self.credit, self.debit, self.balance]
        if (len(set) > 0):
            print("") #(",".join(set))
