from src.entities.businessEntry import BusinessEntry
from src.entities.bankEntry import BankEntry
from src.entities.fileEntry import FileEntry
from src.utils.myString import myString
from abc import ABC, abstractmethod
from src.sessions.globals import session


# TODO: handle the case when the credit report is imported before the bank report
# TODO: create bank report factory
# TODO: implement actual logging and debug mode

# https://www.python-course.eu/python3_abstract_classes.php
class BankReport(ABC):
    type = None
    account = None
    start = None
    end = None

    def process(self):
        self.initTables()
        self.processRows()
        self.processSummary()

    def initTables(self):
        BankEntry.createTable(ifNotExists=True)
        BusinessEntry.createTable(ifNotExists=True)
        FileEntry.createTable(ifNotExists=True)

    def processRows(self):
        for row in self.getRows():
            self.processRow(row)

    def processSummary(self):
        reportDate = self.start + ' to ' + self.end
        entry = FileEntry(userId=session.getUserId(), source=self.type, reportDate=reportDate, total=None,
                          refId=self.account)

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
        entry = BankEntry(date=date, business=business.id, hide=0, refId=refId, credit=credit, debit=debit, balance=balance, trackerId=0, userId=session.getUserId())
        entry.toCSV() # for debugging, find a better way to log only when in debug mode
        return entry

    def getBusinessEntry(self,businessName):
        business = BusinessEntry.selectBy(businessName=businessName, userId=session.getUserId()).getOne(None)
        if (business == None):
            marketingName = businessName.replace('שיק','check')
            business = BusinessEntry(businessName=businessName, marketingName=marketingName, category="", userId=session.getUserId())
        return business

    def renameChecks(self, name):
        name.replace('שיק','check')

    @abstractmethod
    def setAccount(self,val):
        pass

    @abstractmethod
    def setStart(self,val):
        pass

    @abstractmethod
    def setEnd(self,val):
        pass

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

