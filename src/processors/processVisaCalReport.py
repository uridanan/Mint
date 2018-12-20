from src.myString import myString
from datetime import datetime
from src.processors.processXslxFile import XSLXFile
from src.processors.processCreditReport import CreditReport


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