from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def Get_login():
    if request.method == 'POST':
        # 获取表单中提交的邮箱、密码和用户类型
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        print(f"邮箱：{email}, 密码：{password}, 用户类型：{user_type}")

        return redirect(url_for('home.index'))
    
    return render_template('login.html')