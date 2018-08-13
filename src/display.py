import dash
import dash_core_components as dcc
import dash_html_components as html
import src.dbAccess as db

#Am I better off getting the data via REST API or directly from DB?
#It seems more direct to use the DB, I see no need for the overhead of APIs just yet


#Refactor data extraction to separate file - done
#Step 1 : monthly input/output graph in 3 variants: income vs expenses, savings, total - done
#Learn to load sql from file - done
#REFACTOR - done

#Format fields per data type
#Make the table scrollable
#Use a control to select which graph to display
#Step 2 : combined table from all sources
#Step 3 : start marking recurring expenses
#Step 4 : mark expenses by type
#Step 5 : rename expense (save the new name, re-use when recurring)


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
Q_REPORT = 'SELECT * FROM data_entry'

balanceData = db.runQueryFromFile(F_BALANCE)
savingsData = db.runQueryFromFile(F_SAVINGS)
reportData = db.runQuery(Q_REPORT)

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