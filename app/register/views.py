from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from password_strength import PasswordPolicy
from password_strength import PasswordStats
from datetime import date, datetime, timedelta
from pytz import timezone
import MySQLdb.cursors

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
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()
        telephone_number = request.form['telephone_number'].strip()
        
        stats = PasswordStats(password)
        checkpolicy = policy.test(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            # Check if the email already exists
            cursor.execute('SELECT * FROM accounts WHERE LOWER(username) = LOWER(%s)', (username_email,))
            account = cursor.fetchone()

            if account:
                flash("Username already exists!", "warning")

            elif not re.match(r'[^@]+@[^@]+\.[^@]+', username_email):
                flash("Invalid email address!", "warning")

            else:
                if username_email != username_email2:
                    flash("Emails do not match. Please try again.", "warning")

                elif password1 != password2:
                    flash("Passwords do not match. Please try again", "warning")
                else:
                    if checkpolicy and stats.strength() < 0.5:
                        flash("Password not strong enough.Avoid consecutive characters and easily guessed words.","warning")
                        return render_template('Register.html')
                    else:
                        hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute('INSERT INTO accounts (username, password, roleid) VALUES (%s, %s, %s)',
                                        (username_email, hashed_password, roleid,))
                        new_account_id = cursor.lastrowid
                        now = datetime.now(timezone('Pacific/Auckland'))
                        localdate = now.strftime("%Y-%m-%d")
                        cursor.execute('INSERT INTO customers (firstname, lastname, email, phone, accountid, join_date) VALUES (%s, %s, %s, %s, %s, %s)',
                                        (firstname, lastname, username_email, phone, new_account_id, localdate))
                        # commit changes if both are successful
                        mysql.connection.commit()
                    
                        flash("You have successfully registered!", "success")
                        return redirect(url_for('registration.register'))
        except Exception as e:
        # Handle exceptions (e.g., database errors)
            print(f"Error: {e}")
            flash("An error occurred. Please try again later.", "warning")
        finally:
            cursor.close()
        return f'Registration successful! {username}, {email}, {password}, {confirm_password}, {telephone_number}, {stats}, {checkpolicy}'