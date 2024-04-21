from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

LearningForum = Blueprint('LearningForum', __name__)


@LearningForum.route('/Learning_Forum')
def forum():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT
            questions.*
        FROM
            questions
    """
    cursor.execute(sql)
    forum_data = cursor.fetchall()
    print(forum_data)
    return render_template('Learning_Forum.html', forum_data=forum_data)

@LearningForum.route('/forum_detailed')
def forum_detailed():
    return render_template('forum_detailed.html')