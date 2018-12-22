from src.processors.processLeumiReport import LeumiReport
from src.processors.processVisaCalReport import VisaCalReport
from src.processors.processLeumiCardReport import LeumiCardReport
from datetime import datetime


def testImportVISACALReport():
    fileName = "inbox/7872_8547_0205218_Transactions_30_05_2018.xlsx"
    reportDate = datetime(2018, 5, 2)
    cardNum = "7872"
    bankId = "8547"
    visaCal = VisaCalReport(fileName,reportDate,bankId,cardNum)
    #TODO: the date can be extracted from the bank entry when we mark it with hide = 1
    #TODO: handle the case when the credit report is imported before the bank report
    visaCal.process()


def testImportLeumiCardReport():
    fileName = "inbox/4014_Deals.xlsx"
    reportDate = datetime(2017, 3, 15)
    cardNum = "4014"
    bankId = "1111"
    visaCal = LeumiCardReport(fileName,reportDate,bankId,cardNum)
    #TODO: compute the total myself
    #TODO: this report can span many months, there is no report date or total
    #TODO: actually, report date is the second column, I can compute the total on my own, use dictionary of totals per report date
    visaCal.process()



def testImportLeumiReport():
    htmlFile ='inbox/bankleumi30052018.html'
    leumi = LeumiReport(htmlFile)
    leumi.process()


def main():
    #testImportLeumiReport()
    #testImportVISACALReport()
    testImportLeumiCardReport()

main()