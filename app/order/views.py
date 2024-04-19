from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
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
    return render_template('Paypal.html', order_user=order_user, course_data=course_data)

@order.route('/Place_an_order', methods = ['POST'])
def Place_an_order():
    course_id = request.form['course_id'].strip()
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
    username = request.form['username'].strip()
    email = request.form['email'].strip()
    phone = request.form['phone'].strip()
    cc_name = request.form['cc_name'].strip()
    cc_number = request.form['cc_number'].strip()
    cc_cvv = request.form['cc_cvv'].strip()
    current_date = date.today()
    order_date = current_date.strftime('%Y-%m-%d')
    payment_amount = request.form['payment_amount'].strip()
    if len(cc_number) == 16 and cc_number.isdigit():
        if len(cc_cvv) == 3 and cc_cvv.isdigit():
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            write_sql = """
                INSERT INTO orders (username, user_id, email, phone, cc_name, cc_number, cc_cvv, order_date, payment_amount)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            order_data = (username, user_id, email, phone, cc_name, cc_number, cc_cvv, order_date, payment_amount)
            cursor.execute(write_sql, order_data)
            mysql.connection.commit()
            flash("Purchase successful. Thank you for your patronage.", "success")
            return redirect(url_for('Course_order.course_order'))
        else:
            flash("Please enter the 3-digit security code correctly", "danger")
            return render_template('Paypal.html', order_user=order_user, course_data=course_data)
    else:
        flash("Please enter the 16-digit card number", "danger")
        return render_template('Paypal.html', order_user=order_user, course_data=course_data)


    