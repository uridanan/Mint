from src.entities.creditEntry import CreditEntry
from src.entities.businessEntry import BusinessEntry
from src.entities.bankEntry import BankEntry
from src.entities.fileEntry import FileEntry
from src.processors.markCreditCardReports import BankEntriesPostProcessor
from abc import ABC, abstractmethod
from datetime import datetime
from sqlobject.sqlbuilder import AND
from src.sessions.globals import session


class CardData:
    cardNumber = ""
    reportDate = None
    total = 0
    flagged = False

    def __init__(self, cardNumber, reportDate, total=0):
        self.cardNumber = cardNumber
        self.reportDate = reportDate
        self.total = total
        self.flagged = False

    def setTotal(self,total):
        self.total = total

    def update(self,amount):
        self.total += amount

    def flag(self):
        self.flagged = True


# A matrix of card data as a dictionary by date then by card number
class Cards:
    cards = {}

    def __init__(self):
        return

    def add(self,card):
        if card is None or card.reportDate is None or card.cardNumber is None:
            return
        byDate = self.cards.get(card.reportDate,None)
        if byDate is None:
            byDate = {}
            self.cards[card.reportDate] = byDate
        byDate[card.cardNumber] = card

    def get(self,date,number):
        card = None
        byDate = self.cards.get(date,None)
        if byDate is not None:
            card = byDate.get(number,None)
        return card

    def getAll(self):
        arrayOfCards = []
        for date, byDate in self.cards.items():
            for number, card in byDate.items():
                arrayOfCards.append(card)
        return arrayOfCards


# TODO: handle currency? what do I do with it?
class CreditReport(ABC):
    type = None
    cards = Cards()

    def initTables(self):
        CreditEntry.createTable(ifNotExists=True)
        BusinessEntry.createTable(ifNotExists=True)
        BankEntry.createTable(ifNotExists=True)
        FileEntry.createTable(ifNotExists=True)

    def process(self):
        self.initTables()
        self.processRows()
        self.processMonthlyTotals()
        self.processSummary()

    def processRows(self):
        for row in self.getRows():
            #row = list(r.values())
            self.processRow(row)

    def processMonthlyTotals(self):
        for card in self.cards.getAll():
            if BankEntriesPostProcessor.hideCreditCardReport(card.reportDate, card.total):
                card.flag()

    #TODO: pass filename along?
    def processSummary(self):
        for card in self.cards.getAll():
            entry = FileEntry(userId=session.getUserId(), source=self.type, reportDate=card.reportDate, total=card.total, refId=card.cardNumber, flagged=card.flagged)

    def processRow(self,row):
        # ComputeTotals returns False if an entry should be created (i.e. this is an actual entry, not a monthly total)
        if not self.computeMonthlyTotal(row):
            self.addCreditEntry(row)
            return False

        # This was a monthly total row, not an actual entry
        return True

    # Return a value from a dict by index
    def getValue(self,row,index):
        return list(row.values())[index]

    @staticmethod
    def credit(amount):
        if amount < 0:
            return -amount
        else:
            return 0

    @staticmethod
    def debit(amount):
        if amount > 0:
            return amount
        else:
            return 0

    def addMonthlyTotal(self, number, date, amount):
        self.cards.add(CardData(number, date, amount))

    def updateMonthlyTotal(self, number, date, amount):
        card = self.cards.get(date,number)
        if card is None:
            self.cards.add(CardData(number,date,amount))
        else:
            card.update(amount)

    def addCreditEntry(self, row):
        reportDate = self.extractReportDate(row)
        purchaseDate = self.extractPurchaseDate(row)
        businessName = self.extractBusinessName(row)
        amount = self.extractAmount(row)
        cardNumber = self.getCardNumber(row)

        business = self.getBusinessEntry(businessName)
        entry = CreditEntry(reportDate=reportDate, purchaseDate=purchaseDate, business=business.id,
                            cardNumber=cardNumber, bankId="0", credit=self.credit(amount), debit=self.debit(amount),
                            balance=0, trackerId=0, userId=session.getUserId())
        return entry

    def getBusinessEntry(self,businessName):
        business = BusinessEntry.selectBy(businessName=businessName,userId=session.getUserId()).getOne(None)
        if (business == None):
            business = BusinessEntry(businessName=businessName, marketingName=businessName, category="", userId=session.getUserId())
        return business

    @abstractmethod
    def getCardNumber(self, row):
        pass

    @abstractmethod
    def setCardNumber(self, id):
        pass

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
    def computeMonthlyTotal(self, business, date, amount):
        pass