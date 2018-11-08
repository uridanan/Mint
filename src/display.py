import dash
import dash_core_components as dcc
import dash_html_components as html
import src.dbAccess as db

from flask import send_from_directory
import os

#Am I better off getting the data via REST API or directly from DB?
#It seems more direct to use the DB, I see no need for the overhead of APIs just yet



#TODO Use my own CSS (would solve the scrollable problem)
# https://dash.plot.ly/external-resources
# https://github.com/plotly/dash-docs/blob/master/tutorial/external_css_and_js.py
#TODO Change the report to the data presented in the graphs
#TODO Use a control to select which graph to display
#TODO Use time series instead of working so hard on formatting the dates
#https://plot.ly/python/time-series/
#TODO Look at morning star tickers for proper time series?
#https://dash.plot.ly/gallery

#TODO: Format fields per data type
#TODO: Make the table scrollable (use my own CSS)
#TODO: Use tabs to select which graph to display https://dash.plot.ly/dash-core-components/tabs

#TODO: use datatable https://dash.plot.ly/datatable
#TODO: use range slider for date span and upload component for file import https://dash.plot.ly/dash-core-components
#TODO: mark expense category https://dash.plot.ly/datatable/editable
#TODO: monthly report expenses by category
#TODO: expenses by category over time
#TODO: import the rest of the credit cards
#TODO: start marking recurring expenses
#TODO: rename expense (save the new name, re-use when recurring)
#TODO: show credit (income) report

#Try an iplot instead
#https://plot.ly/python/table/
def generateTable(dataframe, max_rows=200):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



def generateBarGraph(data, xName, yNames, names):
    return {
        'data': [
            {'x': data[xName], 'y': data[yNames[i]], 'type': 'bar', 'name': names[i]} for i in range(0,(len(yNames)))
        ]
    }


F_BALANCE = 'src/queryBalanceReport.sql'
F_SAVINGS = 'src/querySavingsReport.sql'
Q_REPORT = 'SELECT * FROM bank_entry'

balanceData = db.runQueryFromFile(F_BALANCE)
savingsData = db.runQueryFromFile(F_SAVINGS)
reportData = db.runQuery(Q_REPORT)

#app = dash.Dash()
app = dash.Dash(__name__)

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

app.layout = html.Div(children=[
    html.H4(children='Bank Report - Work In Pogress'),
    dcc.Graph(id='balance-graph',figure=generateBarGraph(balanceData,"monthname",["balance"],["Balance"])),
    dcc.Graph(id='savings-graph',figure=generateBarGraph(savingsData,"monthname",["savings"],["Savings"])),
    dcc.Graph(id='income-graph',figure=generateBarGraph(savingsData,"monthname",["monthlycredit","monthlydebit"],["Income","Expenses"])),
    generateTable(reportData)
])



if __name__ == '__main__':
    app.run_server(debug=True)