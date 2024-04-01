from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

chat = Blueprint('chat', __name__)


@chat.route('/chat')
def customer_chat():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT
            messages.user_message_content, 
            messages.service_message_content, 
            messages.user_sent_time, 
            messages.service_sent_time, 
            users.user_name, 
            customer_service.service_name, 
            messages.user_id, 
            messages.message_id
        FROM
            messages
        INNER JOIN
            users ON messages.user_id = users.user_id
        INNER JOIN
            customer_service ON messages.service_id = customer_service.service_id;
        """
    cursor.execute(sql)
    customer_chats = cursor.fetchall()
    print(customer_chats)
    return render_template('chat.html', customer_chat=customer_chats)