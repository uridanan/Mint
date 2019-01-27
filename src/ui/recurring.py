from dash.dependencies import Input, Output, State, Event
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import src.dbAccess as db
from src.entities.businessEntry import BusinessEntry
import plotly.graph_objs as go
from src.app import app

#=============================================================================================================
#=============================================================================================================
layout = html.Div(children=[
    html.H4(children='Recurring Expenses - Work In Pogress'),
    html.Button('add', id='add'),
    html.Div(id='newtracker',style={'width':'40%'}),
    html.Div(id='trackers'),
    html.Div(id='data'),
    html.A(id='link')
])

#=============================================================================================================

def generateNewTrackerSection():
    # html.Div(id='newtracker',style={'width':'40%'},children=[
    children = [
        html.H5(children='Add new tracker'),
        html.Div(children=[html.P('Name: ')],className='inline20'),
        html.Div(children=[dcc.Input(id='name', type='text')],className='inline80'),
        html.Div(children=[html.P('Payment: ')],className='inline20'),
        html.Div(children=[dcc.Dropdown(id='payment',
                                  options=[
                                      {'label': 'Check', 'value': 'check'},
                                      {'label': 'Bank Account', 'value': 'bank'},
                                      {'label': 'Credit Card', 'value': 'card'}
                                  ])],className='inline80'),
        html.Div(children=[html.P('Type: ')], className='inline20'),
        html.Div(children=[dcc.Dropdown(id='type',
                              options=[
                                  {'label': 'Fixed amount', 'value': 'fixed'},
                                  {'label': 'Variable amount', 'value': 'variable'}
                              ])], className='inline80'),
        html.Div(children=[html.P('Amount: ')], className='inline20'),
        html.Div(children=[dcc.Input(id='amount', type='text')], className='inline80'),
        html.Button('Submit', id='submit')
    ]
    return children
# Select amount or select business or both

#=============================================================================================================


@app.callback(
    Output('newtracker', 'style'),
    [Input('add', 'n_clicks')],
    )
def toggleTrackers(n_clicks):
    if n_clicks % 2 == 1:
        return {'width': '40%','display': 'none'}
    else:
        return {'width': '40%','display': 'block'}


@app.callback(
    Output('newtracker', 'children'),
    [Input('add', 'n_clicks'),Input('payment', 'value')],
    )
def newTrackerContent(n_clicks,payment):
    return generateNewTrackerSection()

#https://stackoverflow.com/questions/9067892/how-to-align-two-elements-on-the-same-line-without-changing-html
#https://community.plot.ly/t/two-graphs-side-by-side/5312

# TODO: submit callback
# TODO: dependencies between controls for the various use cases: write down the use cases before implementing
# Check: bank account, fixed amount, params: amount, name of recipient
# Recurring Bank Transfer: bank account, fixed amount (+/-), params: amount, name of recipient
# Named bank transfer: bank account, variable amount, params: business
# Credit Card: credit card, params: business
# Boils down to
# Option 1: by amount - specify the amount and a recipient name - automatically look for recurring amounts and ask for a name
# Option 2: by business - select business in drop down, specify and expected amount or a max variation? -
# automatically look for recurring businesses, if no expected amount is provided, compute average and deviation from average
# NO NEED FOR INPUT, DO IT AUTOMATICALLY: add new tracker, add new report to trackers
# Show graph with slider and table with average, min, max, start date, end date and table with alerts