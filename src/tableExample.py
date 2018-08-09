import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine
import psycopg2


#Refactor data extraction to separate file
#Format fields per data type
#Step 1 : monthly input/output graph in 3 variants: income vs expenses, savings, total
#Learn to load sql from file
#"select extract (MONTH from date) as month, extract (YEAR from date) as year, sum(credit) as credit, sum(debit) as debit from data_entry group by month,year order by year, month"
#"select extract (MONTH from date) as month, extract (YEAR from date) as year, max(balance) as balance from data_entry group by month,year order by year, month"

#Step 2 : combined table from all sources
#Step 3 : start marking recurring expenses
#Step 4 : mark expenses by type
#Step 5 : rename expense (save the new name, re-use when recurring)

#This method assumes that the sql file contains only a single command
def loadSingleQuery(fileName):
    fd = open(fileName, 'r')
    sql = fd.read()
    fd.close()
    return sql

#Am I better off getting the data via REST API or directly from DB?
#It seems more direct to use the DB, I see no need for the overhead of APIs just yet
def getData():
    # Create your connection.
    #cnx = builder()(db='mintdb', user='postgres')
    connectionString = "postgres://postgres@localhost:5432/mintdb"
    cnx = create_engine(connectionString)
    df = pd.read_sql_query("SELECT * FROM data_entry", cnx)
    return df

data = getData()

def generate_table(dataframe, max_rows=200):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def getBalanceData():
    connectionString = "postgres://postgres@localhost:5432/mintdb"
    cnx = create_engine(connectionString)
    query = loadSingleQuery('src/queryBalanceReport.sql')
    df = pd.read_sql_query(query, cnx)
    return df

def getSavingsData():
    connectionString = "postgres://postgres@localhost:5432/mintdb"
    cnx = create_engine(connectionString)
    query = loadSingleQuery('src/querySavingsReport.sql')
    df = pd.read_sql_query(query, cnx)
    return df

balanceData = getBalanceData()
savingsData = getSavingsData()

def generate_balance_graph(dataframe):
    return {
        'data': [
        {'x': dataframe.monthname, 'y': dataframe.balance, 'type': 'bar', 'name': 'Balance'}
        ]
    }

def generate_savings_graph(dataframe):
    return {
        'data': [
        {'x': dataframe.monthname, 'y': dataframe.savings, 'type': 'bar', 'name': 'Savings'}
        ]
    }

def generate_income_graph(dataframe):
    return {
        'data': [
        {'x': dataframe.monthname, 'y': dataframe.monthlycredit, 'type': 'bar', 'name': 'Income'},
        {'x': dataframe.monthname, 'y': dataframe.monthlydebit, 'type': 'bar', 'name': 'Expenses'}
        ]
    }

app = dash.Dash()

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

app.layout = html.Div(children=[
    html.H4(children='Bank Report - Work In Pogress'),
    dcc.Graph(id='balance-graph',figure=generate_balance_graph(balanceData)),
    dcc.Graph(id='savings-graph',figure=generate_savings_graph(savingsData)),
    dcc.Graph(id='income-graph',figure=generate_income_graph(savingsData)),
    generate_table(data)
])

if __name__ == '__main__':
    app.run_server(debug=True)