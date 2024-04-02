from flask import Flask
from flask_mysqldb import MySQL
from app import connect

# 数据库配置
app = Flask(__name__)
app.config['SECRET_KEY'] = 'moviemagicsecretkey'

app.config['MYSQL_HOST'] = connect.host
app.config['MYSQL_USER'] = connect.user
app.config['MYSQL_PASSWORD'] = connect.dbpw
app.config['MYSQL_DB'] = connect.db
app.config['MYSQL_PORT'] = connect.port


# 初始化MySQL
mysql = MySQL(app)


# 从app包中导入蓝图
from app.home.views import home
from app.login.views import login
from app.register.views import register
from app.user.views import user
from app.course.views import course
from app.order.views import order
from app.chat.views import chat
from app.Course_details.views import Course_details


# 蓝图注册
app.register_blueprint(home)
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(user)
app.register_blueprint(course)
app.register_blueprint(order)
app.register_blueprint(chat)
app.register_blueprint(Course_details)