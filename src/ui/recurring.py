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
        css=[{'selector': '.selected .cell'}],
        #       'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
        n_fixed_rows=1,
        style_table={
            'overflowY': 'scroll',
            'maxHeight': '600',
            'maxWidth': '900',
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
    return ([{'id': p, 'name': p} for p in ['name','start_date','last_date','count','avg_amount','min_amount','max_amount']])

def getData(dataframe, max_rows=200):
    return [
            dict(entry=i,**{col: dataframe.iloc[i][col] for col in dataframe.columns})
            for i in range(min(len(dataframe), max_rows))
        ]

#=============================================================================================================
def getClassName(id,selectedIds):
    if id in selectedIds:
        return 'selected'
    else:
        return 'unselected'

def makeId(s):
    return '_'.join(s)

def parseId(id):
    params = id.split('_')
    return params

#=============================================================================================================
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


#=============================================================================================================
layout = html.Div(children=[
    html.H4(children='Recurring Expenses - Work In Pogress'),
    dcc.Graph(id='data', figure=generateTimeSeries(getTrackers(trackers_df), trackersData)),
    html.Div(id='slider',className='padded',children=[generateDatesSlider(trackersData.getDates())]),
    html.Div(id='trackers_table', children=[generateTable(trackers_df)])
])

#=============================================================================================================
# Callbacks
@app.callback(
    Output('data', 'figure'),
    [Input('dateRange', 'value'),Input('trackers','selected_rows')])
def updateGraph(dateRange,selected):
    figure = generateTimeSeries(getTrackers(trackers_df,selected), trackersData, dateRange[0], dateRange[1])
    return figure





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
# TODO: highlight selected rows
# TODO: style as cards
# TODO: apply slider to table: compute avg min max accordingly
# TODO: when the amount is constant, show it as avg, min & max
# TODO: rename columns
# TODO: make name editable (and only the name)
# TODO: apply new name to the monthly report and overview as well
# TODO: add section titles
# TODO: alerts
# TODO: align slider when resizing window
# TODO: control table width and center (the problem comes from the input styling)
# TODO: check what I can do with styling and selected rows. How do I apply css classes?
