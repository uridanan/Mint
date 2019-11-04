from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import src.db.dbAccess as db
from src.entities.recurrentExpense import RecurrentExpense
import plotly.graph_objs as go
from src.app import app
from src.ui.timeseries import *
from src.sessions.globals import session
from src.ui.mydatatable import myDataTable, Column, Currency
from src.ui.colors import Colors
from datetime import datetime



#=============================================================================================================
#TODO: Format using the example "Label Lines with Annotations" from https://plot.ly/python/line-charts/
#TODO: add name for undefined
def generateTimeSeries(trackers,timeSeries,start=0,stop=None):
    #df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    #timeSeries = TimeSeriesData(dataFrame)
    data = []
    if stop != None:
        stop = stop + 1  # the [x:y] notation excludes the last index

    if trackers is not None and timeSeries is not None:
        for key,name in trackers.items():
            trace = go.Scatter(
                x=timeSeries.getDates()[start:stop],
                y=timeSeries.getSeriesByName(key)[start:stop],
                name = name,
                #line = dict(color = '#17BECF'),
                opacity = 0.8)
            data.append(trace)

    layout = dict(
        title = "",
        xaxis = dict(title='Month'),
        yaxis = dict(title='Expenses'),
        height = 300
    )
    figure = dict(data=data, layout=layout)
    return figure

#=============================================================================================================
# Max number of marks that can actually display nicely is 30
# Above 30, start alternating with empty labels
# Range slider
MAGIC_NUMBER = 30
def createLabels(dates):
    iMax = len(dates)
    skip = 1 + iMax // MAGIC_NUMBER
    labels = []
    for i in range(iMax):
        labels.append("")
        if i % skip == 0:
            labels[i] = dates[i]
    return labels

def generateDatesSlider(dates):
    iMax = len(dates)-1
    labels = createLabels(dates)
    slider = dcc.RangeSlider(
        id='dateRange',
        marks={i: {'label': labels[i], 'style': {'transform':'matrix(0.8,0.8,-0.8,0.8,-5,15)', 'height': 'fit-content', 'width': 'fit-content'}} for i in range(iMax + 1)},  # range excludes the last index
        min=0,
        max=iMax,
        value=[iMax-3,iMax],
        allowCross=False,
        step=None
    )
    return slider

#=============================================================================================================

#=============================================================================================================
def generateTable(dataframe):
    columns = [Column('name', 'Expense', True, 'left'), Column('start', 'First', False, 'left', '10%'),
               Column('stop', 'Last', False, 'left', '10%'), Column('occurences', 'Count', False, 'right', '6%'),
               Column('average', 'Avg Amount', False, 'right', '10%', Currency.NIS),Column('minimum', 'Min Amount', False, 'right', '10%', Currency.NIS),
               Column('maximum', 'Max Amount', False, 'right', '10%', Currency.NIS)]

    table = myDataTable('trackers',dataframe,columns)
    table.enableSort()
    table.setSelectRows([0,1,2])
    #table.enableFilter()
    return table.generate()

#=============================================================================================================
def getTrackers():
    df = db.runQuery(Q_GETTRACKERS,session.getUserIdParam())
    rDict = {v[0]: v[1] for v in df.values}
    return rDict


def getDataPoints():
    dataFrame = db.runQueryFromFile(F_GETRECURRINGDATA, session.getUserIdParam())
    dataPoints = TimeSeriesData(dataFrame)
    return dataPoints


def getDates(dateRange):
    trackersData = getDataPoints()
    datesCount = len(trackersData.getDates())

    if datesCount < 2:
        return None

    if dateRange is None:
        dateRange = [0, datesCount-1]

    if dateRange[0] < 0:
        dateRange[0] = 0

    if dateRange[1] > datesCount -1:
        dateRange[1] = datesCount -1

    start = trackersData.getDates()[dateRange[0]]
    stop = trackersData.getDates()[dateRange[1]]

    return [start,stop]


def generateTrackersReport(dateRange):
    if dateRange is None:
        return None

    params = [
        {'name': 'start', 'value': [dateRange[0]]},
        {'name': 'stop', 'value': [dateRange[1]]},
        {'name': 'userid', 'value': [session.getUserId()]}
    ]
    return db.runQueryFromFile(F_TRACKERS, params)

F_TRACKERS = 'queries/queryTrackersFromTo.sql'
Q_GETTRACKERS = 'select * from recurrent_expense where user_id = <userid>'
F_GETRECURRINGDATA = 'queries/queryRecurringDataPoints.sql'


#trackersData = getDataPoints()

#=============================================================================================================
# Layout
layout = html.Div(children=[
    html.H4(id='title', children='Recurring Expenses - Work In Pogress',className="row"),
    dcc.Graph(id='data', className='row'),
    html.Div(className='row', children=[
        html.Div(className="one column"),
        html.Div(className="ten columns", children=[html.Div(id='slider', className='padded')]),
        html.Div(className="one column")
    ]),
    html.Div(id='trackers_table', className='row', children=[
        html.Div(className="one column"),
        html.Div(className="ten columns", children=[generateTable(None)]),
        html.Div(className="one column")
    ]),
    html.Div(id='hidden'),
    html.A(id='link')
])

#=============================================================================================================
# Callbacks


@app.callback(
    Output('slider', 'children'),
    [Input('title', 'children')]
)
def updateSlider(title):
    trackersData = getDataPoints()
    slider = generateDatesSlider(trackersData.getDates())
    return slider


# Update the graph
# Edit tracker name
@app.callback(
    Output('data', 'figure'),
    [Input('dateRange', 'value'),Input('trackers','selected_rows'),Input('trackers', 'data')],
    [State('trackers', 'data_previous'),State('trackers', 'active_cell')])
def updateGraph(dateRange,selected,data,previous,cell):
    #Update tracker name in DB
    if cell is not None:
        row = cell['row']
        new = data[row]
        old = previous[row]
        id = new['id']
        newName = new['name']
        oldName = old['name']
        if newName != oldName:
            updateTrackerEntry(id, newName)

    #Update graph
    if data is not None:
        trackers = {}
        for i in selected:
            if i < len(data):
                trackerId = data[i]['id']
                trackerName = data[i]['name']
                trackers[trackerId]=trackerName

    figure = generateTimeSeries(trackers, getDataPoints(), dateRange[0], dateRange[1])
    return figure


# Update the table
@app.callback(
    Output('trackers', 'data'),
    [Input('dateRange', 'value')])
def updateTrackers(dateRange):
    dates = getDates(dateRange)
    df = generateTrackersReport(dates)
    data = myDataTable.getData(df)
    return data


# Hilghlight selected rows
@app.callback(
    Output('trackers','style_data_conditional'),
    [Input('trackers','selected_rows')])
def highlightRows(selected):
    style=[
        myDataTable.setRowColor('odd', 'white'),
        myDataTable.setRowColor('even', Colors.light_grey)
    ]
    for i in selected:
        style.append({'if': {'row_index': i}, 'backgroundColor': Colors.light_cyan})
    return style


def updateTrackerEntry(id,newName):
    tracker = RecurrentExpense.selectBy(id=id,userId=session.getUserId()).getOne(None)
    if tracker is not None:
        tracker.set(name=newName)


#=============================================================================================================

#https://stackoverflow.com/questions/9067892/how-to-align-two-elements-on-the-same-line-without-changing-html
#https://community.plot.ly/t/two-graphs-side-by-side/5312

# TODO: add alerts when expense deviates from expectations / norm
