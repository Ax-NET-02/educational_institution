from app import mysql
from flask import Blueprint, render_template,request, url_for, redirect, session,flash,get_flashed_messages
import MySQLdb.cursors
from datetime import date, datetime, timedelta
import bcrypt
from password_strength import PasswordPolicy
from password_strength import PasswordStats

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def rendering_login():
    return render_template('login.html')

@login.route('/login_data', methods=['GET', 'POST'])
def login_data():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        user_type = request.form['user_type'].strip()
        # 检测是否为管理员
        if user_type == 'administrator':
            admin_email = request.form['email'].strip() 
            admin_password = request.form['password'].strip()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            admin_sql = """
                SELECT
                    admin.admin_name, 
                    admin.admin_mail, 
                    admin.admin_password, 
                    permissions.permission_name,
                    permissions.permission_id
                FROM
                    admin
                INNER JOIN
                    permissions ON admin.permission_id = permissions.permission_id
                WHERE
                    admin_mail = %s;
            """
            cursor.execute(admin_sql, (admin_email,))
            admin_accounts = cursor.fetchone()
            if admin_accounts:
                if bcrypt.checkpw(admin_password.encode('utf-8'), admin_accounts['admin_password'].encode('utf-8')): #check passwords if match
                    session['loggedin'] = True  
                    session['admin_email'] = admin_accounts['admin_mail']
                    session['permission_name'] = admin_accounts['permission_name']
                    flash(f"Login successful, welcome-{admin_accounts['admin_name']}", "success")
                    return redirect(url_for('home.index'))                    
                else:
                    flash("Please enter correct username/password!", "warning")    
                    return redirect(url_for('login.rendering_login'))
            else:   
                flash("Invalid login!", "warning")
                return redirect(url_for('login.rendering_login'))
        # 检测是否为客服    
        elif user_type == 'customer_service':
            service_email = request.form['email'].strip() 
            service_password = request.form['password'].strip()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            service_sql = """
                SELECT
                    service.service_name, 
                    service.service_email, 
                    service.service_password, 
                    permissions.permission_name,
                    permissions.permission_id
                FROM
                    customer_service as service
                INNER JOIN
                    permissions ON service.permission_id = permissions.permission_id
                WHERE
                    service_email = %s;
            """
            cursor.execute(service_sql, (service_email,))
            service_accounts = cursor.fetchone()
            if service_accounts:
                if bcrypt.checkpw(service_password.encode('utf-8'), service_accounts['service_password'].encode('utf-8')): #check passwords if match
                    session['loggedin'] = True 
                    session['permission_name'] = service_accounts['permission_name'] 
                    session['service_email'] = service_accounts['service_email']
                    flash(f"Login successful, welcome-{service_accounts['service_name']}", "success")
                    return redirect(url_for('home.index'))                    
                else:
                    flash("Please enter correct username/password!", "warning")    
                    return redirect(url_for('login.rendering_login'))
            else:   
                flash("Invalid login!", "warning")
                return redirect(url_for('login.rendering_login'))
        else:
            user_mail = request.form['email'].strip() 
            user_password = request.form['password'].strip()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            service_sql = """
                SELECT
                    users.user_name, 
                    users.user_mail, 
                    users.user_password, 
                    permissions.permission_name, 
                    permissions.permission_id
                FROM
                    users
                    INNER JOIN
                    permissions
                    ON 
                        users.permission_id = permissions.permission_id
                WHERE
                    user_mail = %s;
            """
            cursor.execute(service_sql, (user_mail,))
            user_accounts = cursor.fetchone()
            if user_accounts:
                if bcrypt.checkpw(user_password.encode('utf-8'), user_accounts['user_password'].encode('utf-8')): #check passwords if match
                    session['loggedin'] = True 
                    session['permission_name'] = user_accounts['permission_name'] 
                    session['user_mail'] = user_accounts['user_mail']
                    flash(f"Login successful, welcome-{user_accounts['user_name']}", "success")
                    return redirect(url_for('home.index'))                    
                else:
                    flash("Please enter correct username/password!", "warning")    
                    return redirect(url_for('login.rendering_login'))
            else:   
                flash("Invalid login!", "warning")
                return redirect(url_for('login.rendering_login'))
        
        
    return redirect(url_for('login.rendering_login'))