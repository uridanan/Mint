from src.entities.creditEntry import CreditEntry
from src.entities.businessEntry import BusinessEntry
from src.entities.bankEntry import BankEntry
from src.myString import myString
from datetime import datetime
from abc import ABC, abstractmethod
from src.processors.processXslxFile import XSLXFile


class CreditReport(ABC):
    date = None
    bankReportRefId = None
    cardNumber = None

    def process(self):
        CreditEntry.createTable(ifNotExists=True)
        BusinessEntry.createTable(ifNotExists=True)

        for row in self.getRows():
            self.processRow(row)


    # TODO: handle credit line items
    def processRow(self,row):
        # for cell in row:
        #     print(cell.internal_value)
        purchaseDate = self.extractPurchaseDate(row)
        reportDate = self.getReportDate()
        businessName = self.extractBusinessName(row)
        amount = self.extractAmount(row)
        if (myString.isEmpty(businessName)):
            self.handleTotal(amount)
            businessName = "__TOTAL__"

        business = self.getBusinessEntry(businessName)
        entry = CreditEntry(reportDate=reportDate, purchaseDate=purchaseDate, business=business.id,
                            cardNumber=self.getCardNumber(), bankId=self.getBankReportRefId(), credit=0, debit=amount, balance=0)
        entry.toCSV()
        return entry

    def getBusinessEntry(self,businessName):
        business = BusinessEntry.selectBy(businessName=businessName).getOne(None)
        if (business == None):
            business = BusinessEntry(businessName=businessName, marketingName=businessName, category="")
        return business

    def handleTotal(self, total):
        bList = BankEntry.selectBy(debit=total, refId=self.getBankReportRefId())
        for b in bList:
            b.hide = 1

    def getReportDate(self):
        return self.date.strftime("%Y-%m-%d")

    def setReportDate(self,date):
        self.date = date

    def getBankReportRefId(self):
        return self.bankReportRefId

    def setBankReportRefId(self, id):
        self.bankReportRefId = id

    def getCardNumber(self):
        return self.cardNumber

    def setCardNumber(self, id):
        self.cardNumber = id

    @abstractmethod
    def getRows(self):
        pass

    @abstractmethod
    def extractPurchaseDate(self,row):
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


class VisaCalReport(CreditReport):
    data = None

    def __init__(self,filename,reportDate,bankReportRefId,cardNumber):
        self.data = XSLXFile(filename).getData()
        self.setReportDate(reportDate)
        self.setBankReportRefId(bankReportRefId)
        self.setCardNumber(cardNumber)


    ####################################################################################################################
    # Methods to override
    ####################################################################################################################

    def getRows(self):
        rows = self.data.iter_rows(min_row=4, min_col=1, max_col=5)
        return rows

    def extractPurchaseDate(self,row):
        dateString = str(row[0].internal_value)
        if (myString.isEmpty(dateString)):
            return None
        try:
            date = datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S').date().strftime("%Y-%m-%d")
        except:
            date = None
        return date

    def extractAmount(self,row):
        amount = row[3].internal_value
        if (myString.isEmpty(amount)):
            return None
        amount = amount.replace(',', '')
        credit = amount[1:len(amount)]
        return credit

    def extractBusinessName(self, row):
        name = row[1].internal_value
        return name

    def extractComment(self,row):
        comment = row[4].internal_value
        return comment