import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import src.dbAccess as db
import copy
from src.businessEntry import BusinessEntry

app = dash.Dash(__name__)
F_GETMONTHS = 'src/queryMonthSelector.sql'
F_MONTHLY = 'src/queryMonthlyReport.sql'


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


# Inject output into the monthly report query
def generateMonthSelector(months):
    monthSelector = dcc.Dropdown(
        id='selectMonth',
        options=[
            {'label': months.iloc[i][0], 'value': months.iloc[i][1]}
            for i in range(len(months))],
        value=months.iloc[0][1]
    )
    return monthSelector

def generateMonthlyReport(month):
    return db.runQueryFromFile(F_MONTHLY, [{'name': 'month', 'value': month}])


selectableMonths = db.runQueryFromFile(F_GETMONTHS)
defaultMonth = selectableMonths.iloc[0][1]
reportData = generateMonthlyReport(defaultMonth)

app.layout = html.Div(children=[
    html.H4(children='Editable Expense Report - Work In Pogress'),
    generateMonthSelector(selectableMonths),
    generateTable(reportData),
    html.Div(id='output')
])

#=============================================================================================================


# Filter the datatable
def generateCategoryFilter(categories):
    monthSelector = dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        multi=True,
        value="MTL"
    )
    return monthSelector


#=============================================================================================================

#TODO: format the table
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


@app.callback(
    Output('monthlyReport', 'data'),
    [Input('selectMonth', 'value')])
def onMonthSelected(value):
    reportData = generateMonthlyReport(value)
    tableData = getData(reportData)
    return tableData


if __name__ == '__main__':
    app.run_server(debug=True)