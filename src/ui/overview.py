import dash_core_components as dcc
import dash_html_components as html
import src.dbAccess as db
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from src.app import app



#TODO Change the report to the data presented in the graphs
#https://plot.ly/python/time-series/
#TODO Look at morning star tickers for proper time series?
#https://dash.plot.ly/gallery
#https://dash.plot.ly/dash-core-components/tabs

#TODO: Format fields per data type
#TODO: Make the table scrollable (use my own CSS)

#TODO: use range slider for date span and upload component for file import https://dash.plot.ly/dash-core-components
#TODO: manage categories form: create categories and assign businesses to them
#TODO: think of suggesting categories based on classification by others, but each uesr gets to assign businesses as they like

#TODO: add range slider to select dates range
#TODO: start marking recurring expenses
#TODO: import the rest of the credit cards
#TODO: rename expense (save the new name, re-use when recurring)
#TODO: show credit (income) report
#TODO: use upload component to upload files



class TimeSeriesData:
    data = dict()
    dates = []
    start = None
    end = None

    def __init__(self,dataFrame):
        self.data = self.groupByDate(dataFrame)

    def groupByDate(self,dataFrame):
        data = dict()
        start = None
        end = None
        for row in dataFrame.values:
            date = row[0]
            key = row[1]
            value = row[2]
            self.addDate(date)
            if date in data:
                entry = data[date]
            else:
                entry = dict()
            entry[key] = value
            data[date] = entry
        return data

    def addDate(self,date):
        if date in self.dates:
            return
        self.dates.append(date)
        if self.start == None:
            start = date
        self.end = date

    def getSeriesByName(self,name):
        values = []
        for k in self.data.keys():
            v = 0
            if name in self.data[k].keys() and self.data[k][name] != None:
                v = self.data[k][name]
            values.append(v)
        return values

    def getDates(self):
        return self.dates

    def getRange(self):
        return [self.start,self.end]

#TODO: Format using the example "Label Lines with Annotations" from https://plot.ly/python/line-charts/
#TODO: add name for undefined
def generateTimeSeries(categories,dataFrame):
    #df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    timeSeries = TimeSeriesData(dataFrame)
    data = []
    for c in categories:
        trace = go.Scatter(
            x=timeSeries.getDates(),
            y=timeSeries.getSeriesByName(c),
            name = c,
            #line = dict(color = '#17BECF'),
            opacity = 0.8)
        data.append(trace)
    layout = dict(
        title = "Expenses by category over time",
        xaxis = dict(title='Month'),
        yaxis=dict(title='Expenses')
    )
    figure = dict(data=data, layout=layout)
    return figure


def testFigure():
    # Add data
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December']
    high_2000 = [32.5, 37.6, 49.9, 53.0, 69.1, 75.4, 76.5, 76.6, 70.7, 60.6, 45.1, 29.3]
    low_2000 = [13.8, 22.3, 32.5, 37.2, 49.9, 56.1, 57.7, 58.3, 51.2, 42.8, 31.6, 15.9]
    high_2007 = [36.5, 26.6, 43.6, 52.3, 71.5, 81.4, 80.5, 82.2, 76.0, 67.3, 46.1, 35.0]
    low_2007 = [23.6, 14.0, 27.0, 36.8, 47.6, 57.7, 58.9, 61.2, 53.3, 48.5, 31.0, 23.6]
    high_2014 = [28.8, 28.5, 37.0, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9]
    low_2014 = [12.7, 14.3, 18.6, 35.5, 49.9, 58.0, 60.0, 58.6, 51.7, 45.2, 32.2, 29.1]

    # Create and style traces
    trace0 = go.Scatter(
        x=month,
        y=high_2014,
        name='High 2014',
        line=dict(color=('rgb(205, 12, 24)'),
            width=4)
    )
    trace1 = go.Scatter(
        x=month,
        y=low_2014,
        name='Low 2014',
        line=dict(
            color=('rgb(22, 96, 167)'),
            width=4, )
    )
    trace2 = go.Scatter(
        x=month,
        y=high_2007,
        name='High 2007',
        line=dict(
            color=('rgb(205, 12, 24)'),
            width=4,
            dash='dash')  # dash options include 'dash', 'dot', and 'dashdot'
    )
    trace3 = go.Scatter(
        x=month,
        y=low_2007,
        name='Low 2007',
        line=dict(
            color=('rgb(22, 96, 167)'),
            width=4,
            dash='dash')
    )
    trace4 = go.Scatter(
        x=month,
        y=high_2000,
        name='High 2000',
        line=dict(
            color=('rgb(205, 12, 24)'),
            width=4,
            dash='dot')
    )
    trace5 = go.Scatter(
        x=month,
        y=low_2000,
        name='Low 2000',
        line=dict(
            color=('rgb(22, 96, 167)'),
            width=4,
            dash='dot')
    )
    data = [trace0, trace1, trace2, trace3, trace4, trace5]

    # Edit the layout
    layout = dict(title='Average High and Low Temperatures in New York',
                  xaxis=dict(title='Month'),
                  yaxis=dict(title='Temperature (degrees F)'),
                  )

    fig = dict(data=data, layout=layout)
    return fig

#Try an iplot instead
#https://plot.ly/python/table/
def generateTable(dataframe, max_rows=200):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



def generateBarGraph(data, xName, yNames, names):
    return {
        'data': [
            {'x': data[xName], 'y': data[yNames[i]], 'type': 'bar', 'name': names[i]} for i in range(0,(len(yNames)))
        ]
    }


F_BALANCE = 'src/queries/queryBalanceReport.sql'
F_SAVINGS = 'src/queries/querySavingsReport.sql'
F_GETCATEGORIES = 'src/queries/queryCategoryFilter.sql'
F_CATEGORIESOVERTIME = 'src/queries/queryExpensesByCategoryOverTime.sql'

def getCategories():
    df = db.runQueryFromFile(F_GETCATEGORIES)
    list = [v[0] for v in df.values]
    return list

balanceData = db.runQueryFromFile(F_BALANCE)
savingsData = db.runQueryFromFile(F_SAVINGS)
categories = getCategories()
categoriesData = db.runQueryFromFile(F_CATEGORIESOVERTIME)


layout = html.Div(children=[
    html.H4(children='Bank Report - Work In Pogress'),
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Balance', value='tab1'),
        dcc.Tab(label='Savings', value='tab2'),
        dcc.Tab(label='IncomeVSExpenses', value='tab3')
    ]),
    html.Div(id='tabsContent'),
    dcc.Graph(id='byCategory',figure=generateTimeSeries(categories,categoriesData))
])


@app.callback(Output('tabsContent', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab1':
        return html.Div([
            html.H3('Balance over time'),
            dcc.Graph(id='balance-graph', figure=generateBarGraph(balanceData, "monthname", ["balance"], ["Balance"]))
        ])
    elif tab == 'tab2':
        return html.Div([
            html.H3('Savings over time'),
            dcc.Graph(id='savings-graph', figure=generateBarGraph(savingsData, "monthname", ["savings"], ["Savings"]))
        ])
    elif tab == 'tab3':
        return html.Div([
            html.H3('Savings over time'),
            dcc.Graph(id='income-graph',
                      figure=generateBarGraph(savingsData, "monthname", ["monthlycredit", "monthlydebit"],["Income", "Expenses"]))
        ])
