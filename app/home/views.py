from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

home = Blueprint('home', __name__)

@home.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT
            articles.content, 
            articles.img, 
            articles.expression, 
            users.userid, 
            users.username, 
            users.avatar, 
            articles.articleid
        FROM
            articles
            INNER JOIN
            users
            ON 
                articles.userid = users.userid
        """
    cursor.execute(sql)
    content = cursor.fetchall()
    return render_template('home.html', content=content)