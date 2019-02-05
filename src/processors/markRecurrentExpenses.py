from src.entities.recurrentExpense import RecurrentExpense
import src.dbAccess as db

# https://www.python-course.eu/python3_abstract_classes.php

# Postprocessing class. After importing entries for a bank or credit card report,
# automatically identify and mark recurring expenses

class ExpenseTracker():
    minOccurrences = 3
    TYPE_FIXED = 'FIXED'
    TYPE_VARIABLE = 'VARIABLE'
    F_RECURRINGBYBUSINESS = 'src/queries/queryRecurringByBusiness.sql'
    F_RECURRINGBYAMOUNT = 'src/queries/queryRecurringByAmount.sql'

    def initTable(self):
        RecurrentExpense.createTable(ifNotExists=True)

    def queryByBusiness(self):
        params = [
            {'name': 'mincount', 'value': [self.minOccurrences]}
        ]
        dataSet = db.runQueryFromFile(self.F_RECURRINGBYBUSINESS) #, params)
        for row in dataSet.values:
            # name = StringCol()
            # businessId = IntCol()
            # amount = CurrencyCol()
            # type = StringCol()
            # count = IntCol()
            # startDate = DateCol()
            # lastDate = DateCol()
            # avgAmount = CurrencyCol()
            # maxAmount = CurrencyCol()
            # minAmount = CurrencyCol()
            entry = RecurrentExpense(name = row[2], businessId = row[0], type = self.TYPE_VARIABLE, amount = 0,
                                     count = row[1], startDate = row[6], lastDate = row[7],
                                     avgAmount = row[3], maxAmount = row[5], minAmount = row[4])
            print(entry.id)
        return

    def queryByAmount(self):
        pass

# 1. handle new trackers
# 2. update existing trackers
# 3. handle trackers that match both business query and amount query
# 4. handle recurring credit
# Preprocess all the data and computations now because it only changes when you import new data
# Mark all entries so I can join with the expense name when loading the report

run = ExpenseTracker()
run.initTable()
run.queryByBusiness()