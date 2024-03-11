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

# admin = pandas.read_csv('admin.csv')
# for index, row in admin.iterrows():
#     sql = """
#         INSERT INTO admin (admin_id, admin_name, mail, password, permission_id)
#         VALUES
#         (%s, %s, %s, %s, %s)
#     """
#     hashed_pw = bcrypt.hashpw(row['password'].encode('utf-8'), bcrypt.gensalt())
#     parameters = (row['admin_id'], row['admin_name'], row['mail'], hashed_pw, row['permission_id'])
#     insert(sql, parameters)

permissions = pandas.read_csv('permissions.csv')
for index, row in permissions.iterrows():
    sql = """
        INSERT INTO permissions (permission_id, permission_name)
        VALUES
        (%s, %s)
    """
    parameters = (row['permission_id'], row['permission_name'])
    insert(sql, parameters)
    
messages = pandas.read_csv('messages.csv')
for index, row in messages.iterrows():
    sql = """
        INSERT INTO messages (message_id, user_id, service_id, user_message_content, service_message_content, user_sent_time, service_sent_time)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
    """
    parameters = (row['message_id'], row['user_id'], row['service_id'], row['user_message_content'], row['service_message_content'], row['user_sent_time'], row['service_sent_time'])
    insert(sql, parameters)
