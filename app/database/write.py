# 数据库内容导入
import pandas
import bcrypt
import sys
sys.path.insert(0,'..')
import connect
import mysql.connector
import datetime
import numpy as np
from API.get_img_api import get_img


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

admin = pandas.read_csv('admin.csv')
for index, row in admin.iterrows():
    sql = """
        INSERT INTO admin (admin_id, admin_name, admin_mail, admin_password, permission_id, admin_img)
        VALUES
        (%s, %s, %s, %s, %s, %s)
    """
    hashed_pw = bcrypt.hashpw(row['admin_password'].encode('utf-8'), bcrypt.gensalt())
    admin_img = get_img()
    parameters = (row['admin_id'], row['admin_name'], row['admin_mail'], hashed_pw, row['permission_id'], admin_img)
    insert(sql, parameters)
    
customer_service = pandas.read_csv('customer_service.csv')
for index, row in customer_service.iterrows():
    sql = """
        INSERT INTO customer_service (service_id, service_name, service_password, service_email, service_number, permission_id, service_img)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
    """
    hashed_pw = bcrypt.hashpw(row['service_password'].encode('utf-8'), bcrypt.gensalt())
    service_img = get_img()
    parameters = (row['service_id'], row['service_name'], hashed_pw, row['service_email'], row['service_number'], row['permission_id'], service_img)
    insert(sql, parameters)
    

permissions = pandas.read_csv('permissions.csv')
for index, row in permissions.iterrows():
    sql = """
        INSERT INTO permissions (permission_id, permission_name)
        VALUES
        (%s, %s)
    """
    parameters = (row['permission_id'], row['permission_name'])
    insert(sql, parameters)
    
     
users = pandas.read_csv('users.csv')
for index, row in users.iterrows():
    sql = """
        INSERT INTO users (user_id, user_name, user_mail, user_number,user_password, permission_id, user_img)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
    """
    hashed_pw = bcrypt.hashpw(row['user_password'].encode('utf-8'), bcrypt.gensalt())
    user_img = get_img()
    parameters = (row['user_id'], row['user_name'], row['user_mail'], row['user_number'],hashed_pw, row['permission_id'], user_img)
    insert(sql, parameters)
    
    
courses = pandas.read_csv('courses.csv')
for index, row in courses.iterrows():
    sql = """
        INSERT INTO courses (course_title , course_description, course_price, course_duration, course_rating, course_image, course_publish_date, publisher_name)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    parameters = (row['course_title'], row['course_description'], row['course_price'], row['course_duration'], row['course_rating'], row['course_image'], row['course_publish_date'], row['publisher_name'])
    insert(sql, parameters)
 
