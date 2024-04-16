from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

course = Blueprint('course', __name__)


@course.route('/course')
def courses():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT
            courses.*
        FROM
            courses
    """
    cursor.execute(sql)
    course_data = cursor.fetchall()
    return render_template('course.html', course_data=course_data)

@course.route('/course_detailed')
def courses_detailed():
    course_id = request.args.get("course_id")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT
            courses.*
        FROM
            courses
        WHERE
            courses.course_id = %s
    """
    cursor.execute(sql, course_id)
    course_data = cursor.fetchall()
    print(course_data)
    return render_template('Course_details.html', course_data=course_data)
