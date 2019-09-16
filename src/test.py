import src.db.connection
from src.processors.markRecurrentExpenses import ExpenseTracker
from src.processors.processHTMLFile import HTMLFile
from src.processors.processLeumiReport import LeumiReport
from src.processors.processVisaCalReport import VisaCalReport, VisaCalReportFile
from src.processors.processLeumiCardReport import LeumiCardReport, LeumiCardReportFile
from src.processors.processIsraCardReport import IsraCardReport, IsraCardReportFile
from src.sessions.globals import session
from src.user import User
from src.tests import htmlBankLeumi, xlsIsraCard, xlsLeumiCard, xlsVisaCal, originalxlsVisaCal

# TODO: change to XLS instead of XLSX



def testImportVISACALReport():
    fileName = "../inbox/7872_Transactions_03_09_2019.xls"
    visaCal = VisaCalReportFile(fileName)
    visaCal.process()

def testImportLeumiCardReport():
    fileName = "../inbox/4014_Deals.xlsx"
    cardNum = "4014"
    visaCal = LeumiCardReportFile(fileName,cardNum)
    visaCal.process()

def testImportLeumiReport():
    htmlFile ='inbox/bankleumi30052018.html'
    htmlContent = HTMLFile(htmlFile).getData()
    leumi = LeumiReport(htmlContent)
    leumi.process()

def testImportIsraCardReport():
    fileName ='inbox/AMEX_Export_03_2018.xls'
    amex = IsraCardReportFile(fileName)
    amex.process()

def testExpenseTracker():
    run = ExpenseTracker()
    run.process()

def clearDB():
    pass

def startFakeSession():
    tokenInfo = dict()
    tokenInfo['sub'] = '0'
    tokenInfo['email'] = 'fakeuser@clarity.com'
    tokenInfo['name'] = 'Fake User'
    tokenInfo['picture'] = ''
    session.currentUser = User(tokenInfo)



def importLeumiCardContent():
    content = xlsLeumiCard.content
    card = LeumiCardReport(content,'4014')
    card.process()


def importIsraCardContent():
    content = xlsIsraCard.content2019
    card = IsraCardReport(content)
    card.process()


def importVisaCalContent():
    content = xlsVisaCal.content
    card = VisaCalReport(content)
    card.process()

def importOriginalVisaCalContent():
    content = originalxlsVisaCal.content
    card = VisaCalReport(content)
    card.process()

def importBankLeumiContent():
    content = htmlBankLeumi.content
    card = LeumiReport(content)
    card.process()


def importContent():
    importLeumiCardContent()
    importIsraCardContent()
    importVisaCalContent
    importBankLeumiContent()


def main():
    startFakeSession()
    testImportLeumiReport()
    testImportIsraCardReport()
    testImportVISACALReport()
    testImportLeumiCardReport()
    testExpenseTracker()

#main()
startFakeSession()
#importVisaCalContent()
importOriginalVisaCalContent()
#testImportVISACALReport()
#ExpenseTracker().process()