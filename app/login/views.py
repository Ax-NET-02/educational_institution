from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def logins():
    if request.method == 'POST':
        # 获取表单中提交的邮箱、密码和用户类型
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        # 在这里可以对表单数据进行进一步处理，例如验证邮箱和密码是否符合要求

        # 简单地将数据打印输出到控制台
        print(f"邮箱：{email}, 密码：{password}, 用户类型：{user_type}")

        # 在这里可以将数据存储到数据库中，或执行其他逻辑操作

        # 返回一个简单的成功页面，或者重定向到其他页面
        return "注册成功！"
    
    return render_template('login.html')