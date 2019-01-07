from src.entities.creditEntry import CreditEntry
from src.entities.businessEntry import BusinessEntry
from src.entities.bankEntry import BankEntry
from src.myString import myString
from abc import ABC, abstractmethod
from datetime import datetime,timedelta
import src.dbAccess as db
from sqlobject.sqlbuilder import AND

#TODO: build in generic support for multiple cards, multiple dates
#TODO: step 1 - figure out how each updates the cards array
#TODO: step 2 - process the cards totals
#TODO: step 3 - refactor isracard to return rows that can be processed in a unified manner / override processRows


class CardData:
    cardNumber = ""
    reportDate = None
    total = 0

    def __init__(self, cardNumber, reportDate, total=0):
        self.cardNumber = cardNumber
        self.reportDate = reportDate
        self.total = total

    def setTotal(self,total):
        self.total = total


#TODO: handle +/-
#TODO: handle currency? what do I do with it?

class CreditReport(ABC):
    bankReportRefId = "0"
    totals = {}
    cards = []
    currentCard = None  # TODO: make this an index into cards[]


    def initTables(self):
        CreditEntry.createTable(ifNotExists=True)
        BusinessEntry.createTable(ifNotExists=True)

    def process(self):
        self.initTables()
        self.processRows()
        self.processTotals()

    def processRows(self):
        for row in self.getRows():
            self.processRow(row)

    def processTotals(self):
        for date, total in self.totals.items():
            self.processTotal(date,total)
        for card in self.cards:
            self.processTotal(card.reportDate,card.total)  # refactor to pass card as parameter

    def processRow(self,row):
        purchaseDate = self.extractPurchaseDate(row)
        reportDate = self.extractReportDate(row)
        businessName = self.extractBusinessName(row)
        amount = self.extractAmount(row)

        #ComputeTotals returns true if an entry should be created
        if self.computeTotals(businessName,reportDate,amount):
            self.addCreditEntry(reportDate, purchaseDate, businessName,
                                self.getCardNumber(), self.bankReportRefId, amount)

    @staticmethod
    def credit(amount):
        if amount < 0:
            return amount
        else:
            return 0

    @staticmethod
    def debit(amount):
        if amount > 0:
            return amount
        else:
            return 0

    def addTotal(self,date,amount):
        self.totals[date] = amount

    def updateTotal(self,date,amount):
        if self.totals.get(date) == None:
            self.totals[date] = amount
        else:
            self.totals[date] += amount

    def addCreditEntry(self, reportDate, purchaseDate, businessName, cardNumber, bankRefId, amount):
        business = self.getBusinessEntry(businessName)
        entry = CreditEntry(reportDate=reportDate, purchaseDate=purchaseDate, business=business.id,
                            cardNumber=cardNumber, bankId=bankRefId, credit=self.credit(amount), debit=self.debit(amount),
                            balance=0)
        #entry.toCSV()
        return entry

    def getBusinessEntry(self,businessName):
        business = BusinessEntry.selectBy(businessName=businessName).getOne(None)
        if (business == None):
            business = BusinessEntry(businessName=businessName, marketingName=businessName, category="")
        return business

    #lookup by month and amount
    def processTotal(self, date, total):
        reportDate = datetime.strptime(date, '%Y-%m-%d').date()
        start = datetime(reportDate.year,reportDate.month,1).date()
        end = datetime(reportDate.year,reportDate.month,28).date()
        # delta = timedelta(days=3)
        # start = reportDate - delta
        # end = reportDate + delta
        bList = BankEntry.select( AND( BankEntry.q.date >= start , BankEntry.q.date <= end, BankEntry.q.debit == total) )
        for b in bList:
            b.hide = 1

    def getCardNumber(self):
        return self.currentCard.cardNumber

    def setCardNumber(self, id):
        self.currentCard.cardNumber = id

    @abstractmethod
    def getRows(self):
        pass

    @abstractmethod
    def extractPurchaseDate(self,row):
        pass

    @abstractmethod
    def extractReportDate(self,row):
        pass

    @abstractmethod
    def extractBusinessName(self, row):
        pass

    @abstractmethod
    def extractAmount(self, row):
        pass

    @abstractmethod
    def extractComment(self,row):
        pass

    @abstractmethod
    def extractCurrency(self, row):
        pass

    @abstractmethod
    def computeTotals(self,business,date,amount):
        pass