import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine
import psycopg2

#Am I better off getting the data via REST API or directly from DB?
#It seems more direct to use the DB, I see no need for the overhead of APIs just yet


#Refactor data extraction to separate file
#Format fields per data type
#Step 1 : monthly input/output graph in 3 variants: income vs expenses, savings, total - done
#Learn to load sql from file - done
#REFACTOR
#Step 2 : combined table from all sources
#Step 3 : start marking recurring expenses
#Step 4 : mark expenses by type
#Step 5 : rename expense (save the new name, re-use when recurring)

#Get connection to DB
#Use a pattern to only create a new connection if none exists
def dbConnect():
    connectionString = "postgres://postgres@localhost:5432/mintdb"
    cnx = create_engine(connectionString)
    return cnx

#This method assumes that the sql file contains only a single command
def loadSingleQuery(fileName):
    fd = open(fileName, 'r')
    sql = fd.read()
    fd.close()
    return sql


def runQuery(cnx, query):
    return pd.read_sql_query(query, cnx)


def getData(sqlFile):
    cnx = dbConnect()
    query = loadSingleQuery(sqlFile)
    return runQuery(cnx, query)


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


Q_BALANCE = 'src/queryBalanceReport.sql'
Q_SAVINGS = 'src/querySavingsReport.sql'

balanceData = getData(Q_BALANCE)
savingsData = getData(Q_SAVINGS)
reportData = runQuery(dbConnect(),"SELECT * FROM data_entry")

app = dash.Dash()

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