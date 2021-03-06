from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import src.db.dbAccess as db
from src.entities.businessEntry import BusinessEntry
from src.entities.recurrentExpense import RecurrentExpense
import plotly.graph_objs as go
from src.app import app
from src.utils.utils import *
from src.sessions.globals import session
from src.ui.mydatatable import myDataTable, Column, Currency
from src.utils.myString import myString

F_GETMONTHS = 'queries/queryMonthSelector.sql'
F_GETCATEGORIES = 'queries/queryCategoryFilter.sql'
F_MONTHLY = 'queries/queryMonthlyReport.sql'
F_MONTHLYBYCATEGORY = 'queries/queryMonthlyReportByCategory.sql'


#=============================================================================================================
#=============================================================================================================

def generatePieChart(dataFrame):
    data = dataFrame.to_dict()
    labels = toList(data['category'])
    values = toList(data['amount'])
    figureData = [go.Pie(labels=labels,values=values)]
    figure = {
        'data': figureData,
        'layout': {'height': 500,'margin': {'l': 10, 'b': 10, 'r': 90, 't': 50}}
    }
    return figure

#=============================================================================================================
def generateTable(dataframe):
    # date,ref_id,debit,marketing_name,category
    columns = [Column('date', 'Date', False, 'left'),
               Column('ref_id', 'ID', False, 'left'),
               Column('marketing_name', 'Expense', True, 'left'),
               Column('category', 'Category', True, 'left'),
               Column('debit', 'Amount', False, 'right', currency=Currency.NIS)
               ]
    table = myDataTable('monthlyReport',dataframe,columns)
    table.enableSort()
    #table.enableFilter()
    return table.generate()

#=============================================================================================================

def generateDropDown(name,values,enableMultipleSelect,default):
    selector = dcc.Dropdown(
        id=name,
        options=getDropDownData(values),
        multi=enableMultipleSelect,
        value=default
    )
    return selector

def getDropDownData(values):
    return [ {'label': values.values[i][0], 'value': values.values[i][1]}
            for i in range(len(values)) ]

# Inject output into the monthly report query
def generateMonthSelector(months):
    return generateDropDown('selectMonth', months, False, months.values[0][1])

# Filter the datatable
def generateCategorySelector(categories):
    return generateDropDown('filterCategories',categories,True,None)

def getAllCategories(dataframe):
    list = [v[0] for v in dataframe.values]
    return list


# myString.singleQuote(categories.values[i][0]) for i in range(len(categories.values))
def generateMonthlyReport(month,categories):
    params = [
        {'name': 'month', 'value': [month]},
        {'name': 'filter', 'value': categories},
        {'name': 'userid', 'value': [session.getUserId()]}
    ]
    return db.runQueryFromFile(F_MONTHLY, params)

def generatePieChartData(month,categories):
    params = [
        {'name': 'month', 'value': [month]},
        {'name': 'filter', 'value': categories},
        {'name': 'userid', 'value': [session.getUserId()]}
    ]
    return db.runQueryFromFile(F_MONTHLYBYCATEGORY, params)

#=============================================================================================================

reportData = generateMonthlyReport(None,[''])

### Create months and categories dropdowns in callbacks, otherwise they use userId=0
layout = html.Div(children=[
    html.H4(id='title', children='Editable Expense Report - Work In Pogress'),
    dcc.Dropdown(id='selectMonth', multi=False),  #generateMonthSelector(selectableMonths),
    dcc.Dropdown(id='filterCategories', multi=True),  #generateCategorySelector(categories_df),
    generateTable(reportData),
    dcc.Graph(id='pieChart'),
    html.Div(id='output',hidden=True),
])

#=============================================================================================================
#=============================================================================================================

# TODO: format the table
# TODO: format the pie chart
# TODO: add a label for undefined category
# TODO: trackers are created even if the expenses happen in the same month
# DONE: When updating marketing name or category, I need to update all the entries with the same business ID (update the table)
# DONE: entries only appear if they have a tracker, entries without tracker don't appear in the report
# DONE: edit marketing name won't work if the name comes from a tracker. I need to change the name of the tracker too

# https://community.plot.ly/t/solved-updating-a-dash-datatable-rows-with-row-update-and-rows/6573/2


@app.callback(
    Output('selectMonth', 'options'),
    [Input('title', 'children')]
)
def updateMonthSelector(title):
    selectableMonths = db.runQueryFromFile(F_GETMONTHS, session.getUserIdParam())
    months = getDropDownData(selectableMonths)
    return months


@app.callback(
    Output('selectMonth', 'value'),
    [Input('selectMonth', 'options')]
)
def updateDefaultMonth(selectableMonths):
    if len(selectableMonths) < 1:
        return ""
    defaultMonth = selectableMonths[0]['value']
    return defaultMonth


@app.callback(
    Output('filterCategories', 'options'),
    [Input('title', 'children'),Input('output', 'data-*')]
)
def updateCategoryFilter(title,newCategory):
    categories_df = db.runQueryFromFile(F_GETCATEGORIES, session.getUserIdParam())
    filter = getDropDownData(categories_df)
    return filter


@app.callback(
    Output('output', 'data-*'),
    [Input('monthlyReport', 'data_timestamp')],
    [State('monthlyReport', 'data'),State('monthlyReport', 'active_cell')]
)
def processInput(timestamp,data,cell):
    if(cell != None):
        row=cell['row']
        new=data[row]
        newName = new['marketing_name']
        newCategory = new['category']
        businessId = new['business_id']
        trackerId = new['tracker_id']
        updateBusinessEntry(businessId, newName, newCategory)
        updateTrackerEntry(trackerId, newName)
        return newCategory

def updateTrackerEntry(trackerId, newName):
    tracker = RecurrentExpense.selectBy(id=trackerId, userId=session.getUserId()).getOne(None)
    if (tracker != None):
        tracker.set(name=newName)

def updateBusinessEntry(businessId,newName,newCategory):
    business = BusinessEntry.selectBy(id=businessId, userId=session.getUserId()).getOne(None)
    if (business != None):
        business.set(marketingName=newName, category=newCategory)

def getSelectedCategories(filter):
    if (filter != None and len(filter) > 0):
        selectedCategories = filter
    else:
        categories_df = db.runQueryFromFile(F_GETCATEGORIES, session.getUserIdParam())
        selectedCategories = getAllCategories(categories_df)

    #Empty list triggers SQL syntax error, append value ''
    if len(selectedCategories) < 1:
        selectedCategories.append('')
    return selectedCategories

def addCategory(category):
    categories_df = db.runQueryFromFile(F_GETCATEGORIES, session.getUserIdParam())
    categories_list = getAllCategories(categories_df)
    if category not in categories_list:
        categories_list.append(category)


@app.callback(
    Output('monthlyReport', 'data'),
    [Input('selectMonth', 'value'),Input('filterCategories', 'value'),Input('output', 'data-*')])
def onMonthSelected(month,filter,input):
    return updateTable(month, filter)

def updateTable(month,filter):
    selectedCategories = getSelectedCategories(filter)
    reportData = generateMonthlyReport(month,selectedCategories)
    tableData = myDataTable.getData(reportData)
    return tableData


@app.callback(
    Output('pieChart', 'figure'),
    [Input('selectMonth', 'value'),Input('filterCategories', 'value'),Input('output', 'data-*')])
def onMonthSelected(month,filter,newCategory):
    if newCategory is not None and myString.isEmpty(newCategory):
            addCategory(newCategory)
    return updatePieChart(month, filter)

def updatePieChart(month,filter):
    selectedCategories = getSelectedCategories(filter)
    graphData = generatePieChartData(month,selectedCategories)
    figure = generatePieChart(graphData)
    return figure


#On how to display a pie chart in tabs
#https://community.plot.ly/t/how-to-create-a-pie-chart-in-dash-app-under-a-particular-tab/7700


