import dash
import dash_core_components as dcc
import dash_html_components as html
import src.dbAccess as db
from dash.dependencies import Input, Output
from src.ui import overview, monthly
import pandas as pd
import plotly.graph_objs as go
from flask import send_from_directory
import os

#Am I better off getting the data via REST API or directly from DB?
#It seems more direct to use the DB, I see no need for the overhead of APIs just yet

#TODO Use my own CSS (would solve the scrollable problem)
# https://dash.plot.ly/external-resources
# https://github.com/plotly/dash/pull/171

# How to build a multi-page app
# https://dash.plot.ly/urls
# https://github.com/plotly/dash/issues/133
# Cool Themes: https://1stwebdesigner.com/free-bootstrap-dashboard-templates/

app = dash.Dash(__name__)

# This layout displays a sidebar and page content
# Create each layout in a separate dedicated file
app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='sidebar',className='sidebar',children=[
        dcc.Link('Overview', href='overview'),
        dcc.Link('Monthly Reports', href='monthly'),
        dcc.Link('About', href='about')
        ]),
    html.Div(id='content',className='content'),
])

# TODO: all the callbacks here or leave them in the dedicated files per page?
@app.callback(Output('content', 'children'),[dash.dependencies.Input('url', 'pathname')])
def display_page(pageName):
    if pageName == '/overview' or pageName == '/':
        return overview.layout
    elif pageName == '/monthly':
        return monthly.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)