from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

Course_order = Blueprint('Course_order', __name__)


@Course_order.route('/course_order')
def course_order():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = str(session.get('user_id'))
    
    sql = """
        SELECT
            orders.order_id, 
            orders.username, 
            orders.user_id, 
            orders.email, 
            orders.phone, 
            orders.order_date, 
            orders.payment_amount
        FROM
            orders
        WHERE
            orders.user_id = %s
    """
    cursor.execute(sql, user_id)
    order_data = cursor.fetchall()
    return render_template('Course_order.html', order_data=order_data)

@Course_order.route('/Delete_order')
def delete_order():
    order_id = request.args.get("order_id")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE orders FROM orders WHERE order_id = %s;", (order_id,))
    mysql.connection.commit()
    flash(f"order - {order_id} is now deleted", "success")
    return redirect(url_for('Course_order.course_order'))