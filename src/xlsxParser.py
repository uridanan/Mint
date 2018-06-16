from openpyxl import Workbook
from openpyxl import load_workbook
from src.dataEntry import DataEntry


def example():
    wb = Workbook()

    # grab the active worksheet
    ws = wb.active

    # Data can be assigned directly to cells
    ws['A1'] = 42

    # Rows can also be appended
    ws.append([1, 2, 3])

    # Python types will automatically be converted
    import datetime
    ws['A2'] = datetime.datetime.now()

    # Save the file
    wb.save("sample.xlsx")

def loadFile(fileName):
    wb = load_workbook(fileName)
    sheets = wb.sheetnames
    print(sheets)
    sheet = wb.active
    return sheet

def process(sheet):
    cells = sheet.values

    for row in sheet.iter_rows(min_row=4, min_col=1, max_col=5):
        processRow(row)


def processRow(row):
    for cell in row:
        print(cell.internal_value)

    date = str(row[0].internal_value)
    action = row[1].internal_value
    amount = row[3].internal_value
    comment = row[4].internal_value
    entry = DataEntry(date,action,"7872","",amount,"")
    entry.toCSV()

#    date = self.extractDate(row)
#    action = self.extractAction(row)
#    refId = self.extractRefId(row)
#    credit = self.extractCredit(row)
#    debit = self.extractDebit(row)
#    balance = self.extractBalance(row)
#    entry = DataEntry(date,action,refId,credit,debit,balance)
#    return entry


def main():
    fileName = "inbox/7872_Transactions_30_05_2018.xlsx"
    sheet = loadFile(fileName)
    process(sheet)


main()
