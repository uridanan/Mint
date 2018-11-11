import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import src.dbAccess as db

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
    html.H5(id='output')
])

#=============================================================================================================



# params = [
#     'Weight', 'Torque', 'Width', 'Height',
#     'Efficiency', 'Power', 'Displacement'
# ]

# app.layout = html.Div([
#     dash_table.DataTable(
#         id='table-editing-simple',
#         columns=(
#             [{'id': 'Model', 'name': 'Model'}] +
#             [{'id': p, 'name': p} for p in params]
#         ),
#         data=[
#             dict(Model=i, **{param: 0 for param in params})
#             for i in range(1, 5)
#         ],
#         editable=True
#     ),
#     dcc.Graph(id='table-editing-simple-output')
# ])


#TODO: save updated data
#TODO: format the table
#https://community.plot.ly/t/solved-updating-a-dash-datatable-rows-with-row-update-and-rows/6573/2

@app.callback(
    Output('output', 'contentEditable'),
    [Input('monthly-report-table', 'row_update'),
     Input('monthly-report-table', 'columns')])

def display_output(rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    return {
        'data': [{
            'type': 'parcoords',
            'dimensions': [{
                'label': col['name'],
                'values': df[col['id']]
            } for col in columns]
        }]
    }


if __name__ == '__main__':
    app.run_server(debug=True)