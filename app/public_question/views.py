from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

Publicquestion = Blueprint('Publicquestion', __name__)


@Publicquestion.route('/public_question')
def question():
    if 'loggedin' in session:
        return render_template('public_question.html')
    else:
        flash("Please log in to post community content", "danger")
        return redirect(url_for('login.rendering_login'))
    
@Publicquestion.route('/publisher', methods = ['POST'])
def publisher():
    if 'loggedin' in session and session['permission_name'] == 'user':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        publisher_name = session.get('user_name')
        publisher_id = session.get('user_id')
        current_date = date.today()
        publish_date = current_date.strftime('%Y-%m-%d')
        
        public_data = (title, content, publisher_name, publisher_id, publish_date)
        sql = """
            INSERT INTO questions (title, content, publisher_name, publisher_id, publish_date)
            VALUES
                (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, public_data)
        mysql.connection.commit()
        flash("Posted successfully!", "success")
        return redirect(url_for('LearningForum.forum'))
    else:
        flash("Only users can post questions", "warning")
        return redirect(url_for('login.rendering_login'))