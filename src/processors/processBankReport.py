from src.entities.businessEntry import BusinessEntry
from src.entities.bankEntry import BankEntry
from src.myString import myString
from abc import ABC, abstractmethod


# TODO: handle the case when the credit report is imported before the bank report
# TODO: create bank report factory
# TODO: implement actual logging and debug mode

# https://www.python-course.eu/python3_abstract_classes.php
class BankReport(ABC):
    def process(self):
        BankEntry.createTable(ifNotExists=True)
        BusinessEntry.createTable(ifNotExists=True)

        for row in self.getRows():
            self.processRow(row)

    def processRow(self,row):
        date = self.extractDate(row)
        businessName = self.extractBusiness(row)
        refId = self.extractRefId(row)
        credit = self.extractCredit(row)
        debit = self.extractDebit(row)
        balance = self.extractBalance(row)
        if(myString.isEmpty(date)):
            return None

        business = self.getBusinessEntry(businessName)
        entry = BankEntry(date=date, business=business.id, hide=0, refId=refId, credit=credit, debit=debit, balance=balance)
        entry.toCSV() # for debugging, find a better way to log only when in debug mode
        return entry

    def getBusinessEntry(self,businessName):
        business = BusinessEntry.selectBy(businessName=businessName).getOne(None)
        if (business == None):
            business = BusinessEntry(businessName=businessName, marketingName=businessName, category="")
        return business

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

