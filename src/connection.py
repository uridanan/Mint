#For help checkout http://www.sqlobject.org/SQLObject.html#postgres

#Use connectionForURI and sqlhub
#All classes will use this connection by default
import os
from sqlobject import *
connectionString = "postgres://postgres@localhost:5432/mintdb"
connection = connectionForURI(connectionString)
sqlhub.processConnection = connection

#Use connection builder and make the connection a member of the class
#import psycopg2
#import sqlobject
#from sqlobject.postgres import builder
#conn = builder()(db='mintdb', user='postgres')
#In the class: _connection = conn

#Connect to maria db, drivers not compatible with sqlObject
#import mysql.connector as mariadb
#connection = mariadb.connect(user='root', password='root', database='mintdb')
#connectionString = "mysql://root:root@locahost:3306/mintdb"



