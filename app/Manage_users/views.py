from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from password_strength import PasswordPolicy
from password_strength import PasswordStats
import bcrypt
import re

Manage_users = Blueprint('Manage_users', __name__)

policy = PasswordPolicy.from_names(
    length=8,      # minimum length: 8 characters
    uppercase=1,   # require at least 1 uppercase letter
)

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
        flash("Plase login as service or admin to edit user", "warning")
        return redirect(url_for('login.rendering_login'))
    
@Manage_users.route('/Update_users', methods = ['POST'])
def update_users():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        user_id = request.form['user_id']
        user_name = request.form['user_name']
        user_mail = request.form['email']
        user_number = request.form['phone']      

        parameters_user = (user_name, user_mail, user_number, user_id)
        sql_user = """
            UPDATE users
            SET user_name = %s, user_mail = %s, user_number = %s
            WHERE user_id = %s;
            """
        # update user table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql_user, parameters_user)
        mysql.connection.commit()
        flash(f"User - id {user_id} - {user_name} is now updated", "success")
        return redirect(url_for('Manage_users.manage_users'))
    else:
        flash("Plase login as service or admin to edit user", "warning")
        return redirect(url_for('login.rendering_login'))

@Manage_users.route('/Delete_users')
def delete_users():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        user_id = request.args.get("user_id")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # delete the account in account table, automatically delete staff with that accountid
        cursor.execute("DELETE users FROM users WHERE user_id = %s;", (user_id,))
        mysql.connection.commit()
        flash(f"userid - {user_id} is now deleted", "success")
        return redirect(url_for('Manage_users.manage_users'))
    else:
        flash("Plase login as service or admin to edit user", "warning")
        return redirect(url_for('login.rendering_login'))


@Manage_users.route('/Add_users')
def add_users():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        return render_template('add_user.html')
    else:
        flash("Plase login as service or admin to edit user", "warning")
        return redirect(url_for('login.rendering_login'))

@Manage_users.route('/Add_users_data', methods = ['POST'])
def add_users_data():
    # 在这里处理表单提交的数据
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        if request.method == 'POST':
            # 获取表单数据
            user_name = request.form['username'].strip()
            email_data = request.form['email'].strip()
            email = email_data + '@educational.com'
            password = request.form['password'].strip()
            phone = request.form['phone'].strip()
            permission_id = 3
            
            stats = PasswordStats(password)
            checkpolicy = policy.test(password)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            try:
                # Check if the email already exists
                cursor.execute('SELECT * FROM users WHERE LOWER(user_mail) = LOWER(%s)', (email,))
                user_email_row = cursor.fetchone()
                
                cursor.execute('SELECT * FROM users WHERE LOWER(user_name) = LOWER(%s)', (user_name,))
                user_name_row = cursor.fetchone()

                if user_email_row:
                    flash("Useremail already exists!", "warning")
                elif user_name_row:
                    flash("Username already exists!", "warning")

                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    flash("Invalid email address!", "warning")

                else:
                    if checkpolicy and stats.strength() < 0.2:
                        flash("Password not strong enough.Avoid consecutive characters and easily guessed words.","warning")
                        return render_template('add_user.html')
                    else:
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute('INSERT INTO users (user_name, user_mail, user_number, user_password, permission_id) VALUES (%s, %s, %s, %s, %s)',
                                        (user_name, email, phone, hashed_password, permission_id, ))
                        mysql.connection.commit()
                        flash(f"You have successfully added user-{user_name}!", "success")
                        return redirect(url_for('Manage_users.manage_users'))
            except Exception as e:
            # Handle exceptions (e.g., database errors)
                print(f"Error: {e}")
                flash("An error occurred. Please try again later.", "warning")
            finally:
                cursor.close()
        return render_template('add_user.html')
    else:
        return redirect(url_for('login.rendering_login'))