from src.entities.recurrentExpense import RecurrentExpense
import src.dbAccess as db

# https://www.python-course.eu/python3_abstract_classes.php

# Postprocessing class. After importing entries for a bank or credit card report,
# automatically identify and mark recurring expenses
# Pre-process all the data and computations now because it only changes when you import new data

# TODO: add bank account / card number
# TODO: handle recurring credit
# TODO: for now compute avg, min and max until I fine tune the feature.
#    When I add time range in UI, these values should be computed based on the dates selected in UI
# TODO: Make min treshold configurable

class ExpenseTracker():
    minOccurrences = 3
    F_RECURRINGBYBUSINESS = 'src/queries/queryRecurringByBusiness.sql'
    F_RECURRINGBYAMOUNT = 'src/queries/queryRecurringByAmount.sql'
    trackers = []

    def initTable(self):
        RecurrentExpense.createTable(ifNotExists=True)

    def getExpenseTrackerByBusiness(self,businessId):
        tracker = RecurrentExpense.selectBy(businessId=businessId).getOne(None)
        return tracker

    def getExpenseTrackerByAmount(self,amount):
        tracker = RecurrentExpense.selectBy(amount=amount).getOne(None)
        return tracker

    def queryByBusiness(self):
        params = [
            {'name': 'mincount', 'value': [self.minOccurrences]}
        ]
        dataSet = db.runQueryFromFile(self.F_RECURRINGBYBUSINESS) #, params)
        for row in dataSet.values:
            name = row[2] #StringCol()
            businessId = row[0] #IntCol()
            amount = 0 #CurrencyCol()
            type = RecurrentExpense.TYPE_VARIABLE #StringCol()
            count = row[1] #IntCol()
            startDate = row[6] #DateCol()
            lastDate = row[7] #DateCol()
            avgAmount = row[3] #CurrencyCol()
            maxAmount = row[5] #CurrencyCol()
            minAmount = row[4] #CurrencyCol()

            tracker = self.getExpenseTrackerByBusiness(businessId)
            if (tracker == None):
                tracker = RecurrentExpense(businessId=businessId, name=name, type=type, amount=amount,
                                           count=count, startDate=startDate, lastDate=lastDate,
                                           avgAmount=avgAmount, minAmount=minAmount, maxAmount=maxAmount)
                print('New expense tracked by business ' + str(businessId))
            else:
                tracker.update(businessId, name, type, amount,
                               count, startDate, lastDate,
                               avgAmount, minAmount, maxAmount)
                print('Update expense tracked by business ' + str(businessId))

            self.trackers.append(tracker)
            print(tracker.id)
        return

    def queryByAmount(self):
        params = [
            {'name': 'mincount', 'value': [self.minOccurrences]}
        ]
        dataSet = db.runQueryFromFile(self.F_RECURRINGBYAMOUNT)
        for row in dataSet.values:
            # debit, COUNT(*), min(date) as first, max(date) as last
            amount = row[0]  # CurrencyCol()
            count = row[1]  # IntCol()
            startDate = row[2]  # DateCol()
            lastDate = row[3]  # DateCol()
            businessId = 0
            name = 'Check'
            type = RecurrentExpense.TYPE_FIXED  # StringCol()
            avgAmount = 0  # CurrencyCol()
            maxAmount = 0  # CurrencyCol()
            minAmount = 0  # CurrencyCol()

            # If recurring expense is already tracked by business, skip it
            # This is no longer relevant because we only track checks here
            # tracker = self.getExpenseTrackerByBusiness(businessId)
            # if (tracker != None):
            #     print('Recurring expense already tracked by business ' + str(businessId))
            #     continue

            tracker = self.getExpenseTrackerByAmount(amount)
            if (tracker == None):
                tracker = RecurrentExpense(businessId=0, name=name, type=type, amount=amount,
                                           count=count, startDate=startDate, lastDate=lastDate,
                                           avgAmount=avgAmount, minAmount=minAmount, maxAmount=maxAmount)
                print('New expense tracked by amount ' + str(amount))
            else:
                tracker.update(0, name, type, amount,
                               count, startDate, lastDate,
                               avgAmount, minAmount, maxAmount)
                print('Update expense tracked by amount ' + str(amount))

            self.trackers.append(tracker)
            print(tracker.id)
        return

    def findRecurringExpenses(self):
        self.initTable()
        self.queryByBusiness()
        self.queryByAmount()

    def markByBusiness(self):
        dataSet = db.runQueryFromFile(self.F_RECURRINGBYAMOUNT)

    def markRecurringExpenses(self):
        for t in self.trackers:
            t.markExpenses()

    def process(self):
        self.findRecurringExpenses()
        self.markRecurringExpenses()




