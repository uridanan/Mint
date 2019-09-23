from src.processUpload import processFile
from src.uploadTypes import uploadTypes
from src.app import app
import src.db.dbAccess as db
from src.sessions.globals import session
from src.ui.mydatatable import myDataTable, Column

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
# Elements
def getReportsTable():
    df = getFileEntries()
    table = generateTable(df)
    return table

def generateTable(dataframe):
    columns = [Column('source', 'Report', False, 'left', '55%'), Column('ref_id', 'Account or Card', False, 'left', '15%'),
               Column('report_date', 'Date', False, 'left', '15%'), Column('total', 'Amount', False, 'right', '15%')]

    table = myDataTable('files',dataframe,columns)
    table.enableSort()
    #table.enableFilter()
    return table.generate()



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
    html.Div(id='output-data-upload',children=[getReportsTable()])
])


#=============================================================================================================
# Callbacks

@app.callback(Output('files', 'data'),
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
    output = myDataTable.getData(getFileEntries())
    return output


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

