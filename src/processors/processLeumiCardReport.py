from src.utils.myString import myString
from datetime import datetime
from src.processors.processXlsxFile import XLSXFile
from src.processors.processExcel import ExcelContent
from src.processors.processCreditReport import CreditReport
from src.uploadTypes import uploadType

#This report includes a single card over multiple months
# TODO: replace dict and param names with list and indices then fix processRows()
# TODO: rework the interface to allow switching between file and string


class LeumiCardReport(CreditReport):
    data = None
    cardNumber = None

    def __init__(self,fileContent,cardNumber):
        self.data = ExcelContent(fileContent).getData()
        self.setCardNumber(cardNumber)
        self.type = uploadType.LEUMICARD


    ####################################################################################################################
    # Methods to override
    ####################################################################################################################

    def getCardNumber(self, row):
        return self.cardNumber

    def setCardNumber(self, number):
        self.cardNumber = number

    def getRows(self):
        rows = self.data
        return rows

    def extractPurchaseDate(self,row):
        dateString = row['תאריך עסקה']
        if (myString.isEmpty(dateString)):
            return None
        try:
            date = datetime.strptime(dateString, '%d/%m/%Y').date().strftime("%Y-%m-%d")
        except:
            date = None
        return date

    def extractReportDate(self,row):
        dateString = row['תאריך חיוב']
        if (myString.isEmpty(dateString)):
            return None
        try:
            date = datetime.strptime(dateString, '%d/%m/%Y').date().strftime("%Y-%m-%d")
        except:
            date = None
        return date

    #TODO: handle +/- in conversion to float
    def extractAmount(self,row):
        amount = row['סכום חיוב ₪']  #returns as float
        return amount

    def extractBusinessName(self, row):
        name = row['שם בית העסק']
        return name

    def extractComment(self,row):
        comment = row['הערות']
        return comment

    def extractCurrency(self,row):
        currency = row['מטבע עסקה']
        return currency

    def computeMonthlyTotal(self, row):
        reportDate = self.extractReportDate(row)
        amount = self.extractAmount(row)
        cardNumber = self.getCardNumber(row)
        self.updateMonthlyTotal(cardNumber, reportDate, amount)
        return False




class LeumiCardReportFile(CreditReport):
    data = None
    cardNumber = None

    def __init__(self,filename,cardNumber):
        self.data = XLSXFile(filename).getData()
        self.setCardNumber(cardNumber)


    ####################################################################################################################
    # Methods to override
    ####################################################################################################################

    def getCardNumber(self, row):
        return self.cardNumber

    def setCardNumber(self, number):
        self.cardNumber = number

    def getRows(self):
        rows = self.data.iter_rows(min_row=2, min_col=1, max_col=8)
        return rows

    def extractPurchaseDate(self,row):
        dateString = str(row[0].internal_value)
        if (myString.isEmpty(dateString)):
            return None
        try:
            date = datetime.strptime(dateString, '%d/%m/%Y').date().strftime("%Y-%m-%d")
        except:
            date = None
        return date

    def extractReportDate(self,row):
        dateString = str(row[1].internal_value)
        if (myString.isEmpty(dateString)):
            return None
        try:
            date = datetime.strptime(dateString, '%d/%m/%Y').date().strftime("%Y-%m-%d")
        except:
            date = None
        return date

    #TODO: handle +/- in conversion to float
    def extractAmount(self,row):
        amount = str(row[6].internal_value)
        if myString.isEmpty(amount):
            return None
        amount = amount.replace(',', '')
        #credit = amount[1:len(amount)]
        credit = float(amount)
        return credit

    def extractBusinessName(self, row):
        name = row[2].internal_value
        return name

    def extractComment(self,row):
        comment = row[7].internal_value
        return comment

    def extractCurrency(self,row):
        currency = row[4].internal_value
        return currency

    def computeMonthlyTotal(self, row):
        reportDate = self.extractReportDate(row)
        amount = self.extractAmount(row)
        cardNumber = self.getCardNumber(row)
        self.updateMonthlyTotal(cardNumber, reportDate, amount)
        return False