from src.processUpload import processFile
from src.uploadTypes import uploadTypes
from src.app import app
import src.db.dbAccess as db
from src.sessions.globals import session

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import base64
import datetime
import io


#=============================================================================================================
# Queries
Q_GETFILEENTRY = 'select * from file_entry where user_id = <userid>'
def getFileEntries():
    df = db.runQuery(Q_GETFILEENTRY,session.getUserIdParam())
    return df

#=============================================================================================================
# Layout
layout = html.Div([
    html.H4(id='title', children='Upload Files - Work In Pogress'),
    html.Div(id='upload-control', className="row", children=[
        html.Div(className="two columns",children=dcc.Dropdown(id='upload-type', multi=False, options=uploadTypes)),
        html.Div(className="two columns",children=dcc.Upload(id='upload-button',children=html.Button('Upload File',style={'backgroundColor': '#d6fbff'}),multiple=True)),
        html.Div(className="eight columns")
    ]),
    html.Hr(),
    # dcc.Upload(
    #     id='upload-data',
    #     children=html.Div([
    #         'Drag and Drop or ',
    #         html.A('Select Files')
    #     ]),
    #     style={
    #         'width': '100%',
    #         'height': '60px',
    #         'lineHeight': '60px',
    #         'borderWidth': '1px',
    #         'borderStyle': 'dashed',
    #         'borderRadius': '5px',
    #         'textAlign': 'center',
    #         'margin': '10px'
    #     },
    #     # Allow multiple files to be uploaded
    #     multiple=True
    # ),
    html.Div(id='output-data-upload')
])


#=============================================================================================================
# Callbacks

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-button', 'contents')],
              [State('upload-button', 'filename'),
               State('upload-button', 'last_modified'),
               State('upload-type','value')])
def update_output(list_of_contents, list_of_names, list_of_dates, upload_type):
    if list_of_contents is not None:
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            parse_contents(c, n, d, upload_type)
        # children = [
        #     parse_contents(c, n, d, upload_type) for c, n, d in
        #     zip(list_of_contents, list_of_names, list_of_dates)]
        # return children
    return getReportsTable()


def parse_contents(contents, filename, date, type):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        processFile(type, decoded)

        # if 'csv' in filename:
        #     # Assume that the user uploaded a CSV file
        #     df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        # elif 'xls' in filename:
        #     # Assume that the user uploaded an excel file
        #     df = pd.read_excel(io.BytesIO(decoded))
        #     #processFile(uploadType.MAX, decoded)
        # elif 'html' in filename:
        #     df = pd.read_html(io.BytesIO(decoded))
        #     #processFile(uploadType.BANKLEUMI, decoded)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing ' + filename
        ])


def getReportsTable():
    df = getFileEntries()
    table = generateTable(df)
    return table

def generateTable(dataframe, max_rows=200):
    return dash_table.DataTable(
        id='files',
        # Header
        columns= getColumns(dataframe),
        # Body
        #data=[],
        data=getData(dataframe, max_rows),
        sort_action='native',
        filter_action='native',
        editable=False,
        row_selectable=False,
        style_as_list_view=True,
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

def getColumnWidths():
    return [{'source','55%'},{'ref_id','15%'},{'report_date','15%'},{'total','15%'}]

def getColumns(dataframe):
    #columns = [{'id': p, 'name': p} for p in dataframe.columns[1:]]
    columns = [
        {'id': 'source', 'name': 'Report'},
        {'id': 'ref_id', 'name': 'Account or Card'},
        {'id': 'report_date', 'name': 'Date'},
        {'id': 'total', 'name': 'Amount'}
    ]
    return columns

def getData(dataframe, max_rows=200):
    return [
            dict(entry=i,**{col: dataframe.iloc[i][col] for col in dataframe.columns})
            for i in range(min(len(dataframe), max_rows))
        ]