from src.utils.myString import myString
from datetime import datetime
from src.processors.processXlsxFile import XLSXFile
from src.processors.processExcel import ExcelContent
from src.processors.processCreditReport import CreditReport

#This report includes multiple cards over multiple months
# TODO: replace dict and param names with list and indices then fix processRows()
# TODO: rework the interface to allow switching between file and string


class MaxReport(CreditReport):
    data = None
    cardNumber = None

    def __init__(self,fileContent):
        self.data = ExcelContent(fileContent).getData()

    def extractCardNumber(self, row):
        return self.getValue(row,3)

    ####################################################################################################################
    # Methods to override
    ####################################################################################################################

    def getCardNumber(self, row):
        return self.extractCardNumber(row)

    def setCardNumber(self, number):
        self.cardNumber = number

    def getRows(self):
        rows = self.data[3:]
        return rows

    def extractPurchaseDate(self,row):
        dateString = self.getValue(row,0)
        return dateString

    def extractReportDate(self,row):
        dateString = self.getValue(row,9)
        return dateString

    #TODO: handle +/- in conversion to float
    def extractAmount(self,row):
        amount = self.getValue(row,5)  #returns as float
        return amount

    def extractBusinessName(self, row):
        name = self.getValue(row,1)
        return name

    def extractComment(self,row):
        comment =self.getValue(row,10)
        return comment

    def extractCurrency(self,row):
        currency = self.getValue(row,6)
        return currency

    def computeMonthlyTotal(self, row):
        reportDate = self.extractReportDate(row)
        amount = self.extractAmount(row)
        cardNumber = self.getCardNumber(row)
        self.updateMonthlyTotal(cardNumber, reportDate, amount)
        return False




class MaxReportFile(CreditReport):
    data = None
    cardNumber = None

    def __init__(self,filename,cardNumber):
        self.data = XLSXFile(filename).getData()
        self.setCardNumber(cardNumber)

    def extractCardNumber(self, row):
        return self.getValue(row,3)

    ####################################################################################################################
    # Methods to override
    ####################################################################################################################

    def getCardNumber(self, row):
        return self.extractCardNumber(row)

    def setCardNumber(self, number):
        self.cardNumber = number

    def getRows(self):
        rows = self.data[3:]
        return rows

    def extractPurchaseDate(self,row):
        dateString = self.getValue(row,0)
        if (myString.isEmpty(dateString)):
            return None
        try:
            date = datetime.strptime(dateString, '%d/%m/%Y').date().strftime("%Y-%m-%d")
        except:
            date = None
        return date

    def extractReportDate(self,row):
        dateString = self.getValue(row,9)
        if (myString.isEmpty(dateString)):
            return None
        try:
            date = datetime.strptime(dateString, '%d/%m/%Y').date().strftime("%Y-%m-%d")
        except:
            date = None
        return date

    #TODO: handle +/- in conversion to float
    def extractAmount(self,row):
        amount = self.getValue(row,5)  #returns as float
        return amount

    def extractBusinessName(self, row):
        name = self.getValue(row,1)
        return name

    def extractComment(self,row):
        comment =self.getValue(row,10)
        return comment

    def extractCurrency(self,row):
        currency = self.getValue(row,6)
        return currency

    def computeMonthlyTotal(self, row):
        reportDate = self.extractReportDate(row)
        amount = self.extractAmount(row)
        cardNumber = self.getCardNumber(row)
        self.updateMonthlyTotal(cardNumber, reportDate, amount)
        return False
