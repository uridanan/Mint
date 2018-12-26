from src.processors.processLeumiReport import LeumiReport
from src.processors.processVisaCalReport import VisaCalReport
from src.processors.processLeumiCardReport import LeumiCardReport
from datetime import datetime


def testImportVISACALReport():
    fileName = "inbox/7872_8547_0205218_Transactions_30_05_2018.xlsx"
    reportDate = datetime(2018, 5, 2)
    cardNum = "7872"
    bankId = "8547"
    visaCal = VisaCalReport(fileName,cardNum)
    visaCal.process()


def testImportLeumiCardReport():
    fileName = "inbox/4014_Deals.xlsx"
    reportDate = datetime(2017, 3, 15)
    cardNum = "4014"
    bankId = "1111"
    visaCal = LeumiCardReport(fileName,cardNum)
    visaCal.process()



def testImportLeumiReport():
    htmlFile ='inbox/bankleumi30052018.html'
    leumi = LeumiReport(htmlFile)
    leumi.process()


def main():
    #testImportLeumiReport()
    testImportVISACALReport()
    testImportLeumiCardReport()

main()