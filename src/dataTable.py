import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import src.dbAccess as db
import copy

app = dash.Dash(__name__)

#=============================================================================================================
def generateTable(dataframe, max_rows=200):
    return dash_table.DataTable(
        id='monthly-report-table',
        # Header
        columns=(
            [{'id': p, 'name': p} for p in dataframe.columns]
        ),
        # Body
        data=[
            dict(entry=i,**{col: dataframe.iloc[i][col] for col in dataframe.columns})
            for i in range(min(len(dataframe), max_rows))
        ],
        editable=True
    )

F_MONTHLY = 'src/queryMonthlyReport.sql'
reportData = db.runQueryFromFile(F_MONTHLY)

app.layout = html.Div(children=[
    html.H4(children='Editable Expense Report - Work In Pogress'),
    generateTable(reportData),
    html.Div(id='output')
])

#=============================================================================================================


#TODO: save updated data
#TODO: format the table
#https://community.plot.ly/t/solved-updating-a-dash-datatable-rows-with-row-update-and-rows/6573/2

@app.callback(
    Output('output', 'data-*'),
    [Input('monthly-report-table', 'data')],
    [State('monthly-report-table', 'active_cell')])
def processInput(data,cell):
    if(cell != None):
        row=cell[0]
        col=cell[1]
        headers = list(data[row].keys())
        values=data[row]
        value=values[headers[col]]
        print(','.join([headers[col],value]))


def updateBusiness():
    print("")




# @app.callback(
#     Output('editable-table', 'rows'),
#     [Input('editable-table', 'row_update')],
#     [State('editable-table', 'rows')])
# def update_rows(row_update, rows):
#     row_copy = copy.deepcopy(rows)
#     if row_update:
#         updated_row_index = row_update[0]['from_row']
#         updated_value = row_update[0]['updated'].values()[0]
#         row_copy[updated_row_index]['Output'] = (
#             float(updated_value) ** 2
#         )
#     return row_copy



if __name__ == '__main__':
    app.run_server(debug=True)