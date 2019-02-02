from src.entities.recurrentExpense import RecurrentExpense
import src.dbAccess as db

# https://www.python-course.eu/python3_abstract_classes.php

# Postprocessing class. After importing entries for a bank or credit card report,
# automatically identify and mark recurring expenses

class ExpenseTracker():
    minOccurrences = 3
    # F_GETMONTHS = 'src/queries/queryMonthSelector.sql'
    # categories_df = db.runQueryFromFile(F_GETCATEGORIES)
    # db.runQueryFromFile(F_MONTHLYBYCATEGORY, params)

    def initTable(self):
        RecurrentExpense.createTable(ifNotExists=True)

    def queryByBusiness(self):
        pass

    def queryByAmount(self):
        pass

# 1. handle new trackers
# 2. update existing trackers
# 3. handle trackers that match both business query and amount query
# Preprocess all the data and computations now because it only changes when you import new data
# Mark all entries so I can join with the expense name when loading the report