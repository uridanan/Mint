from src.entities.businessEntry import BusinessEntry
from src.entities.bankEntry import BankEntry
from src.myString import myString
from abc import ABC, abstractmethod

# https://www.python-course.eu/python3_abstract_classes.php
class BankReport(ABC):
    def process(self):
        BankEntry.createTable(ifNotExists=True)
        BusinessEntry.createTable(ifNotExists=True)

        for row in self.getRows():
            self.processRow(row)

    def processRow(self,row):
        date = self.extractDate(row)
        action = self.extractBusiness(row)
        refId = self.extractRefId(row)
        credit = self.extractCredit(row)
        debit = self.extractDebit(row)
        balance = self.extractBalance(row)
        if(myString.isEmpty(date)):
            return None

        business = BusinessEntry.selectBy(businessName=action).getOne(None)
        if (business == None):
            business = BusinessEntry(businessName=action, marketingName=action, category="")
        entry = BankEntry(date=date, business=business.id, hide=0, refId=refId, credit=credit, debit=debit, balance=balance)
        entry.toCSV() # for debugging, find a better way to log only when in debug mode
        return entry

    @abstractmethod
    def getRows(self):
        pass

    @abstractmethod
    def extractDate(self,row):
        pass

    @abstractmethod
    def extractBusiness(self, row):
        pass

    @abstractmethod
    def extractRefId(self, row):
        pass

    @abstractmethod
    def extractCredit(self, row):
        pass

    @abstractmethod
    def extractDebit(self, row):
        pass

    @abstractmethod
    def extractBalance(self, row):
        pass


# TODO: test the refactor
# TODO: create bank report factory
# TODO: implement actual logging and debug mode
