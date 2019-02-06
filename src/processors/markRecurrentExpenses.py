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
            type = self.TYPE_VARIABLE #StringCol()
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
            print(tracker.id)
        return

    def queryByAmount(self):
        params = [
            {'name': 'mincount', 'value': [self.minOccurrences]}
        ]
        dataSet = db.runQueryFromFile(self.F_RECURRINGBYAMOUNT)
        for row in dataSet.values:
            businessId = row[0]  # IntCol()
            count = row[1]  # IntCol()
            name = row[2]  # StringCol()
            amount = row[3]  # CurrencyCol()
            type = self.TYPE_FIXED  # StringCol()
            startDate = row[4]  # DateCol()
            lastDate = row[5]  # DateCol()
            avgAmount = 0  # CurrencyCol()
            maxAmount = 0  # CurrencyCol()
            minAmount = 0  # CurrencyCol()

            # If recurring expense is already tracked by business, skip it
            tracker = self.getExpenseTrackerByBusiness(businessId)
            if (tracker != None):
                print('Recurring expense already tracked by business ' + str(businessId))
                continue

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

            print(tracker.id)
        return


# 1. handle new trackers - done
# 2. update existing trackers - done
# 2.5 handle per amount
# 2.6 add bank account / card number
# 3. handle trackers that match both business query and amount query
# 4. handle recurring credit
# 5. for now compute avg, min and max until I fine tune the feature.
# 6. Make min treshold configurable
#    When I add time range in UI, these values should be computed based on the dates selected in UI
# Preprocess all the data and computations now because it only changes when you import new data
# Mark all entries so I can join with the expense name when loading the report

# TODO: there is something wrong with the aggregation by amount in general and checks in particular
# TODO: Review the expenses by amount, if the only ones relevant are checks let's deal with them differently

run = ExpenseTracker()
run.initTable()
run.queryByBusiness()
run.queryByAmount()