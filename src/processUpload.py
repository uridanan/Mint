from src.uploadTypes import uploadType
from src.processors.markRecurrentExpenses import ExpenseTracker
from src.processors.processLeumiReport import LeumiReport
from src.processors.processMaxReport import MaxReport
from src.processors.processVisaCalReport import VisaCalReport
from src.processors.processLeumiCardReport import LeumiCardReport
from src.processors.processIsraCardReport import IsraCardReport


def processFile(type, content):
    upload = None
    if type == uploadType.BANKLEUMI:
        upload = LeumiReport(content)
    if type == uploadType.VISACAL:
        upload = VisaCalReport(content)
    if type == uploadType.ISRACARD:
        upload = IsraCardReport(content)
    if type == uploadType.LEUMICARD:
        cardNum = "0000"
        upload = LeumiCardReport(content,cardNum)
    if type == uploadType.MAX:
        upload = MaxReport(content)
    upload.process()
    ExpenseTracker().process()

