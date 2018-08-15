import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2


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


def runQuery(query):
    #cnx = dbConnect()
    return pd.read_sql_query(query, cnx)


def runQueryFromFile(sqlFile):
    #cnx = dbConnect()
    query = loadSingleQuery(sqlFile)
    return runQuery(query)


cnx = dbConnect()