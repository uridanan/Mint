from dash.dependencies import Input, Output, State, Event
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import src.dbAccess as db
from src.entities.businessEntry import BusinessEntry
import plotly.graph_objs as go
from src.app import app
from src.ui.timeseries import *
from src.utils import *

#=============================================================================================================
#TODO: Format using the example "Label Lines with Annotations" from https://plot.ly/python/line-charts/
#TODO: add name for undefined
def generateTimeSeries(trackers,timeSeries,start=0,stop=None):
    #df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    #timeSeries = TimeSeriesData(dataFrame)
    data = []
    if stop != None:
        stop = stop + 1  # the [x:y] notation excludes the last index
    for key,name in trackers.items():
        trace = go.Scatter(
            x=timeSeries.getDates()[start:stop],
            y=timeSeries.getSeriesByName(key)[start:stop],
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
        id='dateRange',
        marks={i:dates[i] for i in range(iMax+1)}, # range excludes the last index
        min=0,
        max=iMax,
        value=[iMax-3,iMax])
    return slider

#=============================================================================================================

#=============================================================================================================
# TODO: replace datatables with divs and use CSS to make it look like cards that you can toggle
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
# Custom table because dash datatable cannot be styled...
def generateCustomTable(dataframe, max_rows=200):
    # Header
    columns = ['','name','start_date','last_date','count','avg_amount','min_amount','max_amount']
    # Body
    data = getData(dataframe, max_rows)

    return html.Table(

        # Header
        [html.Tr([html.Th(col) for col in columns])] +

        # Body
        [html.Tr(
            id = makeId(['row',str(data[i]['id'])]),
            className = 'unselected',
            children = [html.Td(cellContent(data,i,col)) for col in columns]
        ) for i in range(min(len(data), max_rows))]
    )

def makeId(s):
    return '_'.join(s)

def parseId(id):
    params = id.split('_')
    return params

def editableCell(text,row,col):
    strId = makeId([str(col),str(row)])
    cell = dcc.Input(id=strId, name=strId, type='text', value=text, disabled=False) #setProps,debounce
    return cell

def cellContent(data,row,col):
    editableColumns = ['name']
    id = data[row]['id']
    if col == '':
        content = buttonCell('Show', id)
    else:
        text = data[row][col]
        content = text
        if col in editableColumns:
            content = editableCell(text,id,col)
    return content

def buttonCell(text, row):
    strId = makeId(['toggle', str(row)])
    button = html.Button(text,id=strId)
    return button


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

def initSelectedTrackers(count,trackers):
    max = len(trackers)
    if count > max:
        count = max
    selected = {}
    i = 0
    for k,v in trackers.items():
        if i < count:
            selected[k] = v
            i = i+1
        else:
            break
    return selected


trackersData = getDataPoints()
trackers = getTrackers(trackers_df)
selectedTrackers = initSelectedTrackers(3,trackers)

def generateHiddenPipe():
    pipe = html.Div(id='pipe', children=[
        html.P(id=makeId(['pipe',str(i)]), children='unselected') for i in trackers.keys()
    ])
    return pipe


#=============================================================================================================
layout = html.Div(children=[
    html.H4(children='Recurring Expenses - Work In Pogress'),
    dcc.Graph(id='data', figure=generateTimeSeries(selectedTrackers, trackersData)),
    html.Div(id='slider',className='padded',children=[generateDatesSlider(trackersData.getDates())]),
    html.Div(id='trackers_table',children=[generateCustomTable(trackers_df)]),
    html.Div(id='hidden_output', hidden=True, children=[generateHiddenPipe()])
])

#=============================================================================================================
# Callbacks
@app.callback(
    Output('data', 'figure'),
    [Input('dateRange', 'value'),Input('pipe','children')])
def updateGraph(dateRange,selected):
    for i in range(len(selected)):
        state = selected[i]['props']['children']
        id = int(parseId(selected[i]['props']['id'])[1])
        if state == 'selected':
            selectedTrackers[id] = trackers.get(id)
        if state == 'unselected' and id in selectedTrackers.keys():
            selectedTrackers.pop(id)
    #figure = generateTimeSeries(getTrackers(trackers_df), trackersData, range[0], range[1])
    figure = generateTimeSeries(selectedTrackers, trackersData, dateRange[0], dateRange[1])
    return figure


def toggleState(event,state):
    newState = 'unselected'
    if state == newState:
        newState = 'selected'
    # All callbacks are called at startup, need to compensate for that
    if event == None:
        newState = state
    return newState

for i in trackers.keys():
    @app.callback(
        Output(makeId(['name',str(i)]), 'value'),
        [Input(makeId(['name',str(i)]), 'n_submit')],
        [State(makeId(['name',str(i)]), 'value'),State(makeId(['name',str(i)]), 'name')]
       )
    def updateName(event,value,name):
        params = parseId(name)
        row = params[1]
        col = params[0]
        return value

    @app.callback(
        Output(makeId(['row',str(i)]), 'className'),
        [Input(makeId(['toggle',str(i)]), 'n_clicks')],
        [State(makeId(['row',str(i)]), 'className')]
    )
    def toggleTracker(event, state):
        return toggleState(event,state)


    @app.callback(
        Output(makeId(['pipe',str(i)]), 'children'),
        [Input(makeId(['toggle',str(i)]), 'n_clicks')],
        [State(makeId(['row',str(i)]), 'className')]
    )
    def toggleTracker(event, state):
        return toggleState(event,state)


#=============================================================================================================

#https://stackoverflow.com/questions/9067892/how-to-align-two-elements-on-the-same-line-without-changing-html
#https://community.plot.ly/t/two-graphs-side-by-side/5312

# TODO: Show graph with slider and table with average, min, max, start date, end date and table with alerts
# DONE: show only name, start, last, count, avg, min, max
# DONE: add slider
# DONE: align the slider with the graph and add a separation from the table
# DONE: add table, the table allows toggling the graph and naming the expense.
# DONE: apply slider to graph
# DONE: fix last value on slider
# DONE: toggle graph lines based on table
# TODO: apply slider to table: compute avg min max accordingly
# TODO: when the amount is constant, show it as avg, min & max
# TODO: rename columns
# TODO: make name editable
# TODO: apply new name to the monthly report and overview as well
# TODO: add section titles
# TODO: alerts
# TODO: align slider when resizing window


# Format table and add toggles
# option 1: format datatable and catch onselect events to toggle
# option 2: make my own table or list of divs and figure out the callback, style it as cards (use the projects I downloaded)

# TODO: control table width and center (the problem comes from the input styling)
# DONE: make only name cell editable
# DONE: check callbacks viability
# DONE: style as cards
# TODO: automatically select the first 3 rows
# TODO: show rows as selected in table on start
# TODO: trigger graph update on button click
# TODO: change the style of the show / hide button or replace with an eye
# TODO: in toggle callback, change the appearance of the button
