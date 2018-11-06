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
#TODO: Format fields per data type
#TODO: Make the table scrollable
#TODO: Use a control to select which graph to display


#TODO: Step 2 : combined table from all sources
#TODO: Step 3 : start marking recurring expenses
#TODO: Step 4 : mark expenses by type
#TODO: Step 5 : rename expense (save the new name, re-use when recurring)

#TODO: make a table of all expenses: name, new name, category, refId, replace
#TODO: keep bank account and credit cards in separate tables. each credit card in a separate table? NO


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

def generateTablePandas(dataFrame):
    return dataFrame.describe().to_html()


def generateBarGraph(data, xName, yNames, names):
    return {
        'data': [
            {'x': data[xName], 'y': data[yNames[i]], 'type': 'bar', 'name': names[i]} for i in range(0,(len(yNames)))
        ]
    }


F_BALANCE = 'src/queryBalanceReport.sql'
F_SAVINGS = 'src/querySavingsReport.sql'
Q_REPORT = 'SELECT * FROM credit_entry'
Q_MONTHLY = "select report_date, purchase_date,business,card_number,credit,debit from credit_entry where to_char(report_date, 'YYYY-MM') = '2018-04' order by purchase_date asc"

#balanceData = db.runQueryFromFile(F_BALANCE)
#savingsData = db.runQueryFromFile(F_SAVINGS)
reportData = db.runQuery(Q_MONTHLY)

app = dash.Dash()

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

app.layout = html.Div(children=[
    html.H4(children='Bank Report - Work In Pogress'),
 #   dcc.Graph(id='balance-graph',figure=generateBarGraph(balanceData,"monthname",["balance"],["Balance"])),
 #   dcc.Graph(id='savings-graph',figure=generateBarGraph(savingsData,"monthname",["savings"],["Savings"])),
 #   dcc.Graph(id='income-graph',figure=generateBarGraph(savingsData,"monthname",["monthlycredit","monthlydebit"],["Income","Expenses"])),
    generateTable(reportData)
])



if __name__ == '__main__':
    app.run_server(debug=True)