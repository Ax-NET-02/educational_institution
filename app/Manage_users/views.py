from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

Manage_users = Blueprint('Manage_users', __name__)

@Manage_users.route('/Manage_users')
def manage_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT
            users.user_id AS id,
            users.user_name AS name,  
            users.user_mail AS mail, 
            users.user_number AS phone
        FROM
            users
    """
    cursor.execute(sql)
    user_data = cursor.fetchall()
    return render_template('Manage_users.html', user_data=user_data)

@Manage_users.route('/Edit_users')
def edit_users():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        userid = request.args.get("user_id")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT
                u.user_id AS id, 
                u.user_name AS `name`, 
                u.user_mail AS mail, 
                u.user_number AS phone
            FROM
                users AS u
            WHERE
                u.user_id = %s
        """
        cursor.execute(sql, (userid, ))
        User_data = cursor.fetchall()
        print(User_data)
        return render_template("user_edit.html", User_data=User_data)
    else:
        flash("Plase login as manager or admin to edit staff", "warning")
        return redirect(url_for('login.rendering_login'))
    
@Manage_users.route('/Update_users')
def update_users():
    pass

@Manage_users.route('/Delete_users')
def delete_users():
    pass

@Manage_users.route('/Add_users')
def add_users():
    pass