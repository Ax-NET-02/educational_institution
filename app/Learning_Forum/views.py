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
    question_id = request.args.get("question_id")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT
            questions.*
        FROM
            questions
        WHERE
            questions.question_id = %s
    """
    cursor.execute(sql, question_id)
    forum_detailed = cursor.fetchall()
    print(forum_detailed)
    return render_template('forum_detailed.html', forum_detailed=forum_detailed)

@LearningForum.route('/comment')
def comment():
    pass