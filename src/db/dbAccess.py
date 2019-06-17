import pandas as pd
from sqlalchemy import create_engine
from src.utils.myString import myString


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

def insertParams(query,params={}):
    finalQuery = query
    for param in params:
        name = "<" + param['name'] + ">"
        value = ','.join(myString.singleQuote(v) for v in param['value'])
        finalQuery = finalQuery.replace(name, value)
    return finalQuery

def runQuery(query,params={}):
    #cnx = dbConnect()
    finalQuery = insertParams(query,params)
    return pd.read_sql_query(finalQuery, cnx)

def runQueryFromFile(sqlFile,params={}):
    #cnx = dbConnect()
    query = loadSingleQuery(sqlFile)
    return runQuery(query,params)


cnx = dbConnect()