from src.myString import myString

# This class encapsulates methods to manipulate data entries
# Including import / export methods
class DataEntry:
    date = ""
    action = ""
    refId = ""
    credit = ""
    debit = ""
    balance = ""
    isEmpty = False

    def __init__(self,d,a,r,c,de,b):
        self.date = d
        self.action = a
        self.refId = r
        self.credit = c
        self.debit = de
        self.balance = b
        if(myString.isEmpty(self.date)):
            self.isEmpty = True

    def toCSV(self):
        if(self.isEmpty):
            return
        set = [self.date,self.action,self.refId,self.credit,self.debit,self.balance]
        if (len(set) > 0):
            print(",".join(set))
