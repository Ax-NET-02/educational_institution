from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from password_strength import PasswordPolicy
from password_strength import PasswordStats
from pytz import timezone
import MySQLdb.cursors
import re
import bcrypt
import json
import requests

register = Blueprint('register', __name__)

policy = PasswordPolicy.from_names(
    length=8,      # minimum length: 8 characters
    uppercase=1,   # require at least 1 uppercase letter
)


@register.route('/register')
def user_register():
    return render_template('register.html')


@register.route('/register_data', methods = ['POST'])
def register_data():
        # 在这里处理表单提交的数据
    if request.method == 'POST':
        # 获取表单数据
        user_name = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()
        telephone_number = request.form['telephone_number'].strip()
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
                if password != confirm_password:
                    flash("Passwords do not match. Please try again", "warning")
                else:
                    if checkpolicy and stats.strength() < 0.2:
                        flash("Password not strong enough.Avoid consecutive characters and easily guessed words.","warning")
                        return render_template('register.html')
                    else:
                        url = 'https://www.wudada.online/Api/SjTx'
                        response = requests.get(url)
                        res = json.loads(response.text)
                        user_img = res['data']
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute('INSERT INTO users (user_name, user_mail, user_number, user_password, permission_id, user_img) VALUES (%s, %s, %s, %s, %s, %s)',
                                        (user_name, email, telephone_number, hashed_password, permission_id, user_img))
                        mysql.connection.commit()
                        flash("You have successfully registered!", "success")
                        return redirect(url_for('login.rendering_login'))
        except Exception as e:
        # Handle exceptions (e.g., database errors)
            print(f"Error: {e}")
            flash("An error occurred. Please try again later.", "warning")
        finally:
            cursor.close()
    return render_template('register.html')