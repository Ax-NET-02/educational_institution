# 数据库内容导入

import pandas
import bcrypt
import sys
sys.path.insert(0,'..')
import connect
import mysql.connector
import datetime


def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.user, \
    password=connect.dbpw, host=connect.host, \
    database=connect.db, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

# insert data to database
def insert(sql, parameters):
    connection = getCursor()
    connection.execute(sql, parameters)
    return connection.lastrowid

# accounts data
accounts = pandas.read_csv('data_accounts.csv')
# print(accounts)
for index, row in accounts.iterrows():
    sql = """
        INSERT INTO accounts (accountid, username, password, roleid)
        VALUES
        (%s, %s, %s, %s)
    """
    hashed_pw = bcrypt.hashpw(row['password'].encode('utf-8'), bcrypt.gensalt())
    parameters = (row['accountid'], row['username'], hashed_pw, row['roleid'])
    insert(sql, parameters)