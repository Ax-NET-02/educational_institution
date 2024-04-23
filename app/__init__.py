from flask import Flask
from flask_mysqldb import MySQL
from app import connect

# 数据库配置
app = Flask(__name__)
app.config['SECRET_KEY'] = 'educational_institutionkey'

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
from app.Course_order.views import Course_order
from app.Learning_Forum.views import LearningForum
from app.Manage_forum.views import Manage_forum
from app.public_question.views import Publicquestion
from app.logout.views import logout
from app.Manage_users.views import Manage_users
from app.Manage_course.views import Manages_course
from app.Dashboard.views import Dashboard

# 蓝图注册
app.register_blueprint(home)
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(user)
app.register_blueprint(course)
app.register_blueprint(order)
app.register_blueprint(Course_order)
app.register_blueprint(LearningForum)
app.register_blueprint(Manage_forum)
app.register_blueprint(Publicquestion)
app.register_blueprint(logout)
app.register_blueprint(Manage_users)
app.register_blueprint(Manages_course)
app.register_blueprint(Dashboard)