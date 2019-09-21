from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import src.db.dbAccess as db
from src.entities.businessEntry import BusinessEntry
import plotly.graph_objs as go
from src.app import app
from src.utils.utils import *
from src.sessions.globals import session

F_GETMONTHS = 'queries/queryMonthSelector.sql'
F_GETCATEGORIES = 'queries/queryCategoryFilter.sql'
F_MONTHLY = 'queries/queryMonthlyReport.sql'
F_MONTHLYBYCATEGORY = 'queries/queryMonthlyReportByCategory.sql'


# dt.DataTable(
# rows=df.to_dict(‘records’),
# columns=(df.columns),
# filters=True,
# resizable=True,
# sortColumn=True,
# editable=True,
# row_selectable=True,
# filterable=True,
# sortable=True,
# selected_row_indices=[],
# id=‘datatable-gapminder’)

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
def generateTable(dataframe, editable=[], hidden=[], max_rows=200):
    return dash_table.DataTable(
        id='monthlyReport',
        # Header
        columns=getColumns(dataframe, editable, hidden),
        # Body
        #data=getData(dataframe, max_rows),
        data=[],
        editable=True,
    )

#hidden is deprecated, instead add the columns in data but not in columns
def getColumns(dataframe, editable=[], hidden=[]):
    #return ([{'id': p, 'name': p, 'editable': p in editable, 'hidden': p in hidden} for p in dataframe.columns])
    cols = []
    for p in dataframe.columns:
        if p not in hidden:
            cols.append({'id': p, 'name': p, 'editable': p in editable})
    return cols

def getData(dataframe, max_rows=200):
    return [
            dict(entry=i,**{col: dataframe.iloc[i][col] for col in dataframe.columns})
            for i in range(min(len(dataframe), max_rows))
        ]

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

### Run all these queries on load and update layout accordingly
#categories_df = db.runQueryFromFile(F_GETCATEGORIES, session.getUserIdParam())
#categories_list = getAllCategories(categories_df)
#selectableMonths = db.runQueryFromFile(F_GETMONTHS, session.getUserIdParam())
#defaultMonth = selectableMonths.iloc[0][1]
#reportData = generateMonthlyReport(defaultMonth,categories_list)
#graphData = generatePieChartData(defaultMonth,categories_list)
reportData = generateMonthlyReport(None,[''])

### Create months and categories dropdowns in callbacks, otherwise they use userId=0
layout = html.Div(children=[
    html.H4(id='title', children='Editable Expense Report - Work In Pogress'),
    dcc.Dropdown(id='selectMonth', multi=False),  #generateMonthSelector(selectableMonths),
    dcc.Dropdown(id='filterCategories', multi=True),  #generateCategorySelector(categories_df),
    generateTable(reportData,['marketing_name','category'],['business_id','tracker_id']),
    dcc.Graph(id='pieChart'),
    html.Div(id='output'),
    html.A(id='link')
])

#=============================================================================================================
#=============================================================================================================

#TODO: format the table
#TODO: format the pie chart
#TODO: add a label for undefined category
#TODO: handle exceptions
#https://community.plot.ly/t/solved-updating-a-dash-datatable-rows-with-row-update-and-rows/6573/2


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
    [Input('monthlyReport', 'data'),Input('link', 'n_clicks ')],
    [State('monthlyReport', 'data_previous'),State('monthlyReport', 'active_cell')]
)
def processInput(data,clicks,previous,cell):
    if(cell != None):
        row=cell[0]
        col=cell[1]+1
        headers = list(data[row].keys())
        new=data[row]
        #old=previous[row]
        #oldName=old['marketing_name']
        newName = new['marketing_name']
        newCategory = new['category']
        businessId = new['business_id']
        # if(headers[col] in ('marketing_name','category')):
        #     updateBusinessEntry(businessId,newName,newCategory)
        # If only the relevant columns are editable, no need to test for them
        updateBusinessEntry(businessId, newName, newCategory)
        print("")
        return newCategory


#TODO: apply category to Check (not a regular business, it doesn't stick)
#The problem is that the marketing name was taken from the recurring expenses
#When updating it needs to be applied there too
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
    return selectedCategories

def addCategory(category):
    categories_df = db.runQueryFromFile(F_GETCATEGORIES, session.getUserIdParam())
    categories_list = getAllCategories(categories_df)
    if category not in categories_list:
        categories_list.append(category)


@app.callback(
    Output('monthlyReport', 'data'),
    [Input('selectMonth', 'value'),Input('filterCategories', 'value')])
def onMonthSelected(month,filter):
    return updateTable(month, filter)

def updateTable(month,filter):
    selectedCategories = getSelectedCategories(filter)
    reportData = generateMonthlyReport(month,selectedCategories)
    tableData = getData(reportData)
    return tableData


@app.callback(
    Output('pieChart', 'figure'),
    [Input('selectMonth', 'value'),Input('filterCategories', 'value'),Input('output', 'data-*')])
def onMonthSelected(month,filter,newCategory):
    addCategory(newCategory)
    return updatePieChart(month, filter)

def updatePieChart(month,filter):
    selectedCategories = getSelectedCategories(filter)
    graphData = generatePieChartData(month,selectedCategories)
    figure = generatePieChart(graphData)
    return figure


#On how to display a pie chart in tabs
#https://community.plot.ly/t/how-to-create-a-pie-chart-in-dash-app-under-a-particular-tab/7700
