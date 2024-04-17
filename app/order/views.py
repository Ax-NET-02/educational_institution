from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

order = Blueprint('order', __name__)


@order.route('/order')
def orders():
    course_id = request.args.get("course_id")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = str(session.get('user_id'))
      
    user_sql = """
        SELECT
            users.user_name, 
            users.user_mail, 
            users.user_number
        FROM
            users
        WHERE
            users.user_id = %s
    """
    
    cursor.execute(user_sql, user_id)
    order_user = cursor.fetchone()
    
    course_sql = """
        SELECT
            courses.*
        FROM
            courses
        WHERE
            courses.course_id = %s
    """
    
    cursor.execute(course_sql, course_id)
    course_data = cursor.fetchone()
    print(course_data)
    return render_template('Paypal.html', order_user=order_user, course_data=course_data)