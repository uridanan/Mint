from dash.dependencies import Input, Output, State, Event
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import src.dbAccess as db
from src.entities.businessEntry import BusinessEntry
from src.entities.recurrentExpense import RecurrentExpense
import plotly.graph_objs as go
from src.app import app, auth
from src.ui.timeseries import *
from src.utils import *
from flask import session

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
        title = "",
        xaxis = dict(title='Month'),
        yaxis = dict(title='Expenses'),
        height = 300
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
def generateTable(dataframe, max_rows=200):
    return dash_table.DataTable(
        id='trackers',
        # Header
        columns=getColumns(dataframe),
        # Body
        #data=[],
        data=getData(dataframe, max_rows),
        editable=True,
        row_selectable="multi",
        selected_rows=[0,1,2],
        style_as_list_view=True,
        # css=[{'selector': '.dash-cell div.dash-cell-value',
        #       'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
        # n_fixed_rows=1,
        css=[
            {
                'selector': 'td.cell--selected, td.focused',
                'rule': 'background-color: #d6fbff; --accent: #78daf1; text-align: left'
            },
            {
                'selector': 'td.cell--selected *, td.focused *',
                'rule': 'background-color: #d6fbff; --accent: #78daf1; text-align: left'
            }
        ],
        style_table={
            #'overflowY': 'scroll',
            #'maxHeight': '600',
            #'maxWidth': '1500',
            '--accent':'#78daf1',
            '--hover': '#d6fbff',
            '--selected-row': '#d6fbff',
            '--selected-background': '#d6fbff'
        },
        style_cell={
            'whiteSpace': 'normal',
            'text-align': 'left',
            'hover': 'hotpink'
        },
        style_header={
            'whiteSpace': 'normal',
            'background-color': '#555',
            'color': 'white',
            'font-weight': 'bold',
            'height': '50px',
            'textAlign': 'left'
        },
        style_header_conditional=[
            {'if': {'column_id': c}, 'width': w} for c,w in getColumnWidths()
        ],
        style_cell_conditional=[
            {'if': {'column_id': c}, 'width': w} for c,w in getColumnWidths()
        ],
        style_data={
            'accent': '#78daf1',
            'hover': '#d6fbff'
        }

        # ,
        # style_data_conditional=[
        #     {'if': {'row_index': i}, 'backgroundColor': '#3D9970', 'color': 'white'} for i in selected_rows
        # ]
        # content_style
        # style_cell, style_cell_conditional
        # style_data, style_data_conditional,
        # style_header, style_header_conditional,
        # style_table
    )
# https://dash.plot.ly/datatable/sizing
# Allowed arguments: active_cell, column_conditional_dropdowns, column_static_dropdown, columns, content_style, css,
# data, data_previous, data_timestamp, derived_viewport_data, derived_viewport_indices, derived_virtual_data,
# derived_virtual_indices, dropdown_properties, editable, end_cell, filtering, filtering_settings, filtering_type,
# filtering_types, id, is_focused, merge_duplicate_headers, n_fixed_columns, n_fixed_rows, navigation, pagination_mode,
# pagination_settings, row_deletable, row_selectable, selected_cells, selected_rows, sorting, sorting_settings,
# sorting_treat_empty_string_as_none, sorting_type, start_cell, style_as_list_view, style_cell, style_cell_conditional,
# style_data, style_data_conditional, style_filter, style_filter_conditional, style_header, style_header_conditional, style_table


def getColumnWidths():
    return [{'start','10%'},{'stop','10%'},{'occurences','6%'},{'average','10%'},{'minimum','10%'},{'maximum','10%'}]


def getColumns(dataframe):
    #([{'id': p, 'name': p} for p in dataframe.columns[1:]])
    columns = [
        {'id': 'name', 'name': 'Expense'},
        {'id': 'start', 'name': 'First'},
        {'id': 'stop', 'name': 'Last'},
        {'id': 'occurences', 'name': 'Count'},
        {'id': 'average', 'name': 'Avg Amount'},
        {'id': 'minimum', 'name': 'Min Amount'},
        {'id': 'maximum', 'name': 'Max Amount'}
    ]
    return columns

def getData(dataframe, max_rows=200):
    return [
            dict(entry=i,**{col: dataframe.iloc[i][col] for col in dataframe.columns})
            for i in range(min(len(dataframe), max_rows))
        ]

#=============================================================================================================
def getTrackers():
    df = db.runQuery(Q_GETTRACKERS)
    dict = {}
    dict = {v[0]: v[1] for v in df.values}
    return dict


def getDataPoints():
    dataFrame = db.runQueryFromFile(F_GETRECURRINGDATA)
    dataPoints = TimeSeriesData(dataFrame)
    return dataPoints


def getDates(dateRange):
    trackersData = getDataPoints()
    if dateRange is None:
        dateRange = [0, len(trackersData.getDates())-1]
    start = trackersData.getDates()[dateRange[0]]
    stop = trackersData.getDates()[dateRange[1]]
    return [start,stop]


def generateTrackersReport(dateRange):
    params = [
        {'name': 'start', 'value': [dateRange[0]]},
        {'name': 'stop', 'value': [dateRange[1]]}
    ]
    return db.runQueryFromFile(F_TRACKERS, params)

F_TRACKERS = 'src/queries/queryTrackersFromTo.sql'
Q_GETTRACKERS = 'select * from recurrent_expense'
F_GETRECURRINGDATA = 'src/queries/queryRecurringDataPoints.sql'


trackersData = getDataPoints()

#=============================================================================================================
# Layout
layout = html.Div(children=[
    html.H4(id='title', children='Recurring Expenses - Work In Pogress',className="row"),
    dcc.Graph(id='data', figure=generateTimeSeries(getTrackers(), trackersData), className="row"),
    html.Div(id='slider', className='padded',children=[generateDatesSlider(trackersData.getDates())]),
    html.Div(id='trackers_table', className="row", children=[
        html.Div(className="one column"),
        html.Div(className="ten columns", children=[generateTable(generateTrackersReport(getDates([13,16])))]),
        html.Div(className="one column")
    ]),
    html.Div(id='hidden'),
    html.A(id='link')
])

#=============================================================================================================
# Callbacks

# Update the graph
# Edit tracker name
@app.callback(
    Output('data', 'figure'),
    [Input('dateRange', 'value'),Input('trackers','selected_rows'),Input('trackers', 'data')],
    [State('trackers', 'data_previous'),State('trackers', 'active_cell')])
def updateGraph(dateRange,selected,data,previous,cell):
    #Update tracker name in DB
    if cell is not None:
        row=cell[0]
        new=data[row]
        old=previous[row]
        id=new['id']
        newName=new['name']
        oldName = old['name']
        if newName != oldName:
            updateTrackerEntry(id, newName)

    #Update graph
    trackers = {}
    for i in selected:
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
    df = generateTrackersReport(getDates(dateRange))
    data = getData(df)
    return data


# Hilghlight selected rows
@app.callback(
    Output('trackers','style_data_conditional'),
    [Input('trackers','selected_rows')])
def highlightRows(selected):
    style=[
        {'if': {'row_index': i}, 'backgroundColor': '#d6fbff'} for i in selected
    ]
    return style


def updateTrackerEntry(id,newName):
    tracker = RecurrentExpense.selectBy(id=id).getOne(None)
    if tracker is not None:
        tracker.set(name=newName)


#=============================================================================================================

#https://stackoverflow.com/questions/9067892/how-to-align-two-elements-on-the-same-line-without-changing-html
#https://community.plot.ly/t/two-graphs-side-by-side/5312

# TODO: fix hover color
# TODO: add currency symbols
# TODO: make other columns non editable
# TODO: use grid and columns to position and resize the graph and table
# TODO: add alerts when expense deviates from expectations / norm
# TODO: style as cards

