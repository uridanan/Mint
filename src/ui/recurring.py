from dash.dependencies import Input, Output, State, Event
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import src.dbAccess as db
from src.entities.businessEntry import BusinessEntry
import plotly.graph_objs as go
from src.app import app
from src.ui.timeseries import *

#=============================================================================================================
#TODO: Format using the example "Label Lines with Annotations" from https://plot.ly/python/line-charts/
#TODO: add name for undefined
def generateTimeSeries(trackers,timeSeries):
    #df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    #timeSeries = TimeSeriesData(dataFrame)
    data = []
    for key,name in trackers.items():
        trace = go.Scatter(
            x=timeSeries.getDates(),
            y=timeSeries.getSeriesByName(key),
            name = name,
            #line = dict(color = '#17BECF'),
            opacity = 0.8)
        data.append(trace)
    layout = dict(
        title = "Recurring Expenses",
        xaxis = dict(title='Month'),
        yaxis = dict(title='Expenses')
    )
    figure = dict(data=data, layout=layout)
    return figure

#=============================================================================================================
# Range slider

def generateDatesSlider(dates):
    iMax = len(dates)-1
    slider = dcc.RangeSlider(
        marks={i:dates[i] for i in range(iMax)},
        min=0,
        max=iMax,
        value=[iMax-3,iMax])
    return slider

#=============================================================================================================

#=============================================================================================================
def generateTable(dataframe, max_rows=200):
    return dash_table.DataTable(
        id='Trackers',
        # Header
        columns=getColumns(dataframe),
        # Body
        #data=[],
        data=getData(dataframe, max_rows),
        editable=True,
    )

def getColumns(dataframe):
    return ([{'id': p, 'name': p} for p in ['name','start_date','last_date','count','avg_amount','min_amount','max_amount']])

def getData(dataframe, max_rows=200):
    return [
            dict(entry=i,**{col: dataframe.iloc[i][col] for col in dataframe.columns})
            for i in range(min(len(dataframe), max_rows))
        ]

#=============================================================================================================
#=============================================================================================================
Q_GETTRACKERS = 'select * from recurrent_expense'
F_GETRECURRINGDATA = 'src/queries/queryRecurringDataPoints.sql'

trackers_df = db.runQuery(Q_GETTRACKERS)

def getTrackers(df):
    #df = db.runQuery(Q_GETTRACKERS)
    dict = {v[0]:v[1] for v in df.values}
    return dict

def getDataPoints():
    dataFrame = db.runQueryFromFile(F_GETRECURRINGDATA)
    dataPoints = TimeSeriesData(dataFrame)
    return dataPoints

trackersData = getDataPoints()

#=============================================================================================================
layout = html.Div(children=[
    html.H4(children='Recurring Expenses - Work In Pogress'),
    dcc.Graph(id='data', figure=generateTimeSeries(getTrackers(trackers_df), trackersData)),
    generateDatesSlider(trackersData.getDates()),
    generateTable(trackers_df),
    html.Div(id='trackers_table')
])

#=============================================================================================================
# Callbacks

#=============================================================================================================

#https://stackoverflow.com/questions/9067892/how-to-align-two-elements-on-the-same-line-without-changing-html
#https://community.plot.ly/t/two-graphs-side-by-side/5312

# TODO: Show graph with slider and table with average, min, max, start date, end date and table with alerts
# TODO: add slider
# TODO: add table, the table allows toggling the graph and naming the expense.
# TODO: The new name applies to the monthly report and overview as well
# DONE: show only name, start, last, count, avg, min, max
# TODO: align the slider with the graph and add a separation from the table
# TODO: when the amount is constant, show it as avg, min & max
# TODO: rename columns
# TODO: add section titles
# TODO: table content dynamic based on slider
# TODO: make name editable
# TODO: apply new name to the monthly report and overview as well
# TODO: toggle graph lines based on table
# TODO: alerts

