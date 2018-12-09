import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import src.dbAccess as db
import copy
from src.businessEntry import BusinessEntry
import plotly.graph_objs as go

app = dash.Dash(__name__)
F_GETMONTHS = 'src/queryMonthSelector.sql'
F_GETCATEGORIES = 'src/queryCategoryFilter.sql'
F_MONTHLY = 'src/queryMonthlyReport.sql'
F_MONTHLYBYCATEGORY = 'src/queryMonthlyReportByCategory.sql'


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

def list(dict):
    return [v for v in dict.values()]

def generatePieChart(dataFrame):
    data = dataFrame.to_dict()
    labels = list(data['category'])
    values = list(data['amount'])
    figureData = [go.Pie(labels=labels,values=values)]
    figure = {
        'data': figureData,
        'layout': {'height': 500,'margin': {'l': 10, 'b': 10, 'r': 90, 't': 50}}
    }
    return figure

#=============================================================================================================
def generateTable(dataframe, max_rows=200):
    return dash_table.DataTable(
        id='monthlyReport',
        # Header
        columns=getColumns(dataframe),
        # Body
        #data=getData(dataframe, max_rows),
        data=[],
        editable=True,
    )

def getColumns(dataframe):
    return ([{'id': p, 'name': p} for p in dataframe.columns])

def getData(dataframe, max_rows=200):
    return [
            dict(entry=i,**{col: dataframe.iloc[i][col] for col in dataframe.columns})
            for i in range(min(len(dataframe), max_rows))
        ]

#=============================================================================================================

def generateDropDown(name,values,enableMultipleSelect,default):
    selector = dcc.Dropdown(
        id=name,
        options=[
            {'label': values.values[i][0], 'value': values.values[i][1]}
            for i in range(len(values))],
        multi=enableMultipleSelect,
        value=default
    )
    return selector

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
        {'name': 'filter', 'value': categories}
    ]
    return db.runQueryFromFile(F_MONTHLY, params)

def generatePieChartData(month,categories):
    params = [
        {'name': 'month', 'value': [month]},
        {'name': 'filter', 'value': categories}
    ]
    return db.runQueryFromFile(F_MONTHLYBYCATEGORY, params)

#=============================================================================================================

selectableMonths = db.runQueryFromFile(F_GETMONTHS)
categories_df = db.runQueryFromFile(F_GETCATEGORIES)
categories_list = getAllCategories(categories_df)
defaultMonth = selectableMonths.iloc[0][1]
reportData = generateMonthlyReport(defaultMonth,categories_list)
graphData = generatePieChartData(defaultMonth,categories_list)

app.layout = html.Div(children=[
    html.H4(children='Editable Expense Report - Work In Pogress'),
    generateMonthSelector(selectableMonths),
    generateCategorySelector(categories_df),
    generateTable(reportData),
    dcc.Graph(id='pieChart',figure=generatePieChart(graphData)),
    html.Div(id='output')
])

#=============================================================================================================
#=============================================================================================================

#TODO: format the table
#TODO: format the pie chart
#TODO: add a label for undefined category
#TODO: handle exceptions
#https://community.plot.ly/t/solved-updating-a-dash-datatable-rows-with-row-update-and-rows/6573/2

@app.callback(
    Output('output', 'data-*'),
    [Input('monthlyReport', 'data')],
    [State('monthlyReport', 'data_previous'),State('monthlyReport', 'active_cell')])
def processInput(data,previous,cell):
    if(cell != None):
        row=cell[0]
        col=cell[1]+1
        headers = list(data[row].keys())
        new=data[row]
        old=previous[row]
        oldName=old['marketing_name']
        newName = new['marketing_name']
        newCategory = new['category']
        if(headers[col] in ('marketing_name','category')):
            updateBusinessEntry(oldName,newName,newCategory)
        print("")

def updateBusinessEntry(oldName,newName,newCategory):
    business = BusinessEntry.selectBy(marketingName=oldName).getOne(None)
    if (business != None):
        business.set(marketingName=newName, category=newCategory)

def getSelectedCategories(filter):
    selectedCategories = categories_list
    if (filter != None and len(filter) > 0):
        selectedCategories = filter
    return selectedCategories

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
    [Input('selectMonth', 'value'),Input('filterCategories', 'value')])
def onMonthSelected(month,filter):
    return updatePieChart(month, filter)

def updatePieChart(month,filter):
    selectedCategories = getSelectedCategories(filter)
    graphData = generatePieChartData(month,selectedCategories)
    figure = generatePieChart(graphData)
    return figure


#On how to display a pie chart in tabs
#https://community.plot.ly/t/how-to-create-a-pie-chart-in-dash-app-under-a-particular-tab/7700

if __name__ == '__main__':
    app.run_server(debug=True)