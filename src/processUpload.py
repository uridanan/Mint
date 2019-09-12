from src.processors.markRecurrentExpenses import ExpenseTracker
from src.processors.processLeumiReport import LeumiReport
from src.processors.processMaxReport import MaxReport
from src.processors.processVisaCalReport import VisaCalReport
from src.processors.processLeumiCardReport import LeumiCardReport
from src.processors.processIsraCardReport import IsraCardReport

class uploadType():
    VISACAL = 0
    LEUMICARD = 1
    ISRACARD = 2
    MAX = 3
    BANKLEUMI = 10

uploadTypes = [
    {'label': 'Bank Leumi', 'value': uploadType.BANKLEUMI},
    {'label': 'Visa CAL', 'value': uploadType.VISACAL},
    {'label': 'LeumiCard', 'value': uploadType.LEUMICARD},
    {'label': 'IsraCard', 'value': uploadType.ISRACARD},
    {'label': 'MAX', 'value': uploadType.MAX}
]

def processFile(type, content):
    upload = None
    if type == uploadType.BANKLEUMI:
        upload = LeumiReport(content)
    if type == uploadType.VISACAL:
        upload = VisaCalReport(content)
    if type == uploadType.LEUMICARD:
        cardNum = "4014"
        upload = LeumiCardReport(content,cardNum)
    if type == uploadType.ISRACARD:
        upload = IsraCardReport(content)
    if type == uploadType.MAX:
        upload = MaxReport(content)
    upload.process()
    ExpenseTracker().process()

