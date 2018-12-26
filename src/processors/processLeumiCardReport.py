from src.myString import myString
from datetime import datetime
from src.processors.processXslxFile import XSLXFile
from src.processors.processCreditReport import CreditReport


class LeumiCardReport(CreditReport):
    data = None

    def __init__(self,filename,cardNumber):
        self.data = XSLXFile(filename).getData()
        self.setCardNumber(cardNumber)


    ####################################################################################################################
    # Methods to override
    ####################################################################################################################

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

    def computeTotals(self,business,date,amount):
        self.updateTotal(date, amount)
        return True