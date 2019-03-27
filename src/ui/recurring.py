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
        css=[{'selector': '.dash-cell div.dash-cell-value',
              'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
        n_fixed_rows=1,
        style_table={
            #'overflowY': 'scroll',
            #'maxHeight': '600',
            'maxWidth': '1500',
            '--accent':'#78daf1',
            '--hover': '#d6fbff',
            '--selected-row': '#d6fbff',
            '--selected-background': '#d6fbff'
        },
        style_cell={
            'whiteSpace': 'normal',
            'text-align': 'left'
        },
        style_header={
            'background-color': '#555',
            'color': 'white',
            'font-weight': 'bold',
            'height': '50px'
        }
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


def getColumns(dataframe):
    return ([{'id': p, 'name': p} for p in dataframe.columns[1:]])

def getData(dataframe, max_rows=200):
    return [
            dict(entry=i,**{col: dataframe.iloc[i][col] for col in dataframe.columns})
            for i in range(min(len(dataframe), max_rows))
        ]

#=============================================================================================================
F_TRACKERS = 'src/queries/queryTrackersFromTo.sql'
Q_GETTRACKERS = 'select * from recurrent_expense'
F_GETRECURRINGDATA = 'src/queries/queryRecurringDataPoints.sql'

trackers_df = db.runQuery(Q_GETTRACKERS)

def getTrackers(df, selected=None):
    #df = db.runQuery(Q_GETTRACKERS)
    dict = {}
    if selected == None:
        dict = {v[0]: v[1] for v in df.values}
    else:
        i=0
        for v in df.values:
            if i in selected:
                dict[v[0]] = v[1]
            i = i+1
    return dict

def getDataPoints():
    dataFrame = db.runQueryFromFile(F_GETRECURRINGDATA)
    dataPoints = TimeSeriesData(dataFrame)
    return dataPoints

trackersData = getDataPoints()
trackers = getTrackers(trackers_df)

def getDates(dateRange):
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

#=============================================================================================================
# Layout
layout = html.Div(children=[
    html.H4(children='Recurring Expenses - Work In Pogress'),
    dcc.Graph(id='data', figure=generateTimeSeries(getTrackers(trackers_df), trackersData)),
    html.Div(id='slider',className='padded',children=[generateDatesSlider(trackersData.getDates())]),
    html.Div(id='trackers_table', children=[generateTable(generateTrackersReport(getDates([13,16])))])
])

#=============================================================================================================
# Callbacks
@app.callback(
    Output('data', 'figure'),
    [Input('dateRange', 'value'),Input('trackers','selected_rows')])
def updateGraph(dateRange,selected):
    figure = generateTimeSeries(getTrackers(trackers_df,selected), trackersData, dateRange[0], dateRange[1])
    return figure


@app.callback(
    Output('trackers', 'data'),
    [Input('dateRange', 'value')])
def updateTrackers(dateRange):
    df = generateTrackersReport(getDates(dateRange))
    data = generateTable(df)
    return data

#=============================================================================================================

#https://stackoverflow.com/questions/9067892/how-to-align-two-elements-on-the-same-line-without-changing-html
#https://community.plot.ly/t/two-graphs-side-by-side/5312

# TODO: Show graph with slider and table with average, min, max, start date, end date and table with alerts
# TODO: apply slider to table: compute avg min max accordingly
# TODO: when the amount is constant, show it as avg, min & max
# TODO: rename columns
# TODO: make name editable
# TODO: apply new name to the monthly report and overview as well
# TODO: make other columns non editable
# TODO: add section titles
# TODO: alerts
# TODO: check what I can do with styling and selected rows. How do I apply css classes?
# TODO: use grid and columns to position and resize the graph and table
# TODO: highlight selected rows
# TODO: style as cards
# TODO: cleanup: remove global variables, fetch all data in callbacks
# TODO: format dates
# TODO: format amounts
# TODO: fix last date
# TODO: get table to update when slider changes, why isn't it working?
