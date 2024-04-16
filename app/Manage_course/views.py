from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

Manages_course = Blueprint('Manages_course', __name__)


@Manages_course.route('/Manages_course')
def manages_course():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT
                courses.course_id, 
                courses.course_title, 
                courses.course_description, 
                courses.course_price, 
                courses.course_duration, 
                courses.course_rating, 
                courses.course_image, 
                courses.course_publish_date, 
                courses.publisher_name
            FROM
                courses
        """
        cursor.execute(sql)
        course_data = cursor.fetchall()
        print(course_data)
        return render_template('manage_course.html', course_data=course_data)
    else:
        flash("Plase login as service or admin to edit user", "warning")
        return redirect(url_for('login.rendering_login'))

@Manages_course.route('/edit_course')
def edit_course():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        course_id = request.args.get("course_id")
        sql = """
            SELECT
                courses.course_id, 
                courses.course_title, 
                courses.course_description, 
                courses.course_price, 
                courses.course_duration, 
                courses.course_rating, 
                courses.course_image, 
                courses.course_publish_date, 
                courses.publisher_name
            FROM
                courses
            WHERE
                courses.course_id = %s
        """
        cursor.execute(sql, course_id)
        course_data = cursor.fetchall()
        return render_template('edit_course.html', course_data=course_data)
    else:
        flash("Plase login as service or admin to edit user", "warning")
        return redirect(url_for('login.rendering_login'))

@Manages_course.route('/updata_course', methods = ['POST'])
def updata_course():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        course_id = request.form['course_id'].strip()
        course_title = request.form['course_title'].strip()
        course_description = request.form['course_description'].strip()
        course_price = request.form['course_price'].strip()
        RuntimeHours = request.form['RuntimeHours'].strip()
        RuntimeMinutes = request.form['RuntimeMinutes'].strip()
        hours = int(RuntimeHours)
        minutes = int(RuntimeMinutes)
        course_duration = hours * 60 + minutes
        course_image = request.form['course_image'].strip()
        course_publish_date = request.form['course_publish_date'].strip()
        if session['permission_name'] == 'admin':
            publisher_name = session.get('admin_name')
        elif session['permission_name'] == 'service':
            publisher_name = session.get('service_name')
        
        parameters_course = (course_title, course_description, course_price, course_duration, course_image, course_publish_date, publisher_name, course_id)
        sql = """
            UPDATE courses
                SET course_title = %s, course_description = %s, course_price = %s, course_duration = %s, course_image = %s, course_publish_date= %s, publisher_name = %s
            WHERE 
                course_id = %s;
        """
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, parameters_course)
        mysql.connection.commit()
        flash(f"Course {course_title} has been modified", "success")
        return redirect(url_for('Manages_course.manages_course'))
    else:
        flash("Plase login as service or admin to edit user", "warning")
        return redirect(url_for('login.rendering_login'))

@Manages_course.route('/add_course')
def add_course():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        return render_template('add_course.html')
    else:
        flash("Plase login as service or admin to edit user", "warning")
        return redirect(url_for('login.rendering_login'))
    
@Manages_course.route('/add_course_data', methods = ['POST'])
def add_course_data():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        course_title = request.form['course_title'].strip()
        course_description = request.form['course_description'].strip()
        course_price = request.form['course_price'].strip()
        RuntimeHours = request.form['RuntimeHours'].strip()
        RuntimeMinutes = request.form['RuntimeMinutes'].strip()
        hours = int(RuntimeHours)
        minutes = int(RuntimeMinutes)
        course_duration = hours * 60 + minutes
        course_image = request.form['course_image'].strip()
        course_publish_date = request.form['course_publish_date'].strip()
        if session['permission_name'] == 'admin':
            publisher_name = session.get('admin_name')
        elif session['permission_name'] == 'service':
            publisher_name = session.get('service_name')
            
        sql = """
        INSERT INTO courses (course_title, course_description, course_price, course_duration, course_image, course_publish_date, publisher_name) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (course_title, course_description, course_price, course_duration, course_image, course_publish_date, publisher_name, ))
        mysql.connection.commit()
        flash(f"Course {course_title} is now added", "success")
        return redirect(url_for('Manages_course.manages_course'))
    else:
        flash("Plase login as service or admin to edit user", "warning")
        return redirect(url_for('login.rendering_login'))

@Manages_course.route('/delete_course')
def delete_course():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        course_id = request.args.get("course_id")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # delete the account in account table, automatically delete staff with that accountid
        cursor.execute("DELETE courses FROM courses WHERE course_id = %s;", (course_id,))
        mysql.connection.commit()
        flash(f"course - {course_id} is now deleted", "success")
        return redirect(url_for('Manages_course.manages_course'))
    else:
        flash("Plase login as service or admin to edit user", "warning")
        return redirect(url_for('login.rendering_login'))