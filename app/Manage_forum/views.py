from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

Manage_forum = Blueprint('Manage_forum', __name__)


@Manage_forum.route('/admin_service_forum')
def admin_service_forum():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT
                questions.*
            FROM
                questions
        """
        cursor.execute(sql)
        manage_forum = cursor.fetchall()
        return render_template('Manage_forum.html', manage_forum=manage_forum)
    else:
        flash("Plase login as service or admin to edit Forum", "warning")
        return redirect(url_for('login.rendering_login'))
    
@Manage_forum.route('/admin_service_comment')
def admin_service_comment():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        question_id = request.args.get("question_id")

        comment_sql = """
            SELECT
                comments.comment_id,
                comments.comment_content,
                comments.commenter_name,
                comments.comment_date 
            FROM
                comments 
            WHERE
                comments.question_id = %s
        """
        cursor.execute(comment_sql, (question_id, ))
        admin_service_comment = cursor.fetchall()
        return render_template('admin_service_comment.html', admin_service_comment=admin_service_comment)
    else:
        flash("Plase login as service or admin to edit Forum", "warning")
        return redirect(url_for('login.rendering_login'))
    
@Manage_forum.route('/admin_service_delete_forum')
def delete_forum():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        question_id = request.args.get("question_id")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # delete the account in account table, automatically delete staff with that accountid
        cursor.execute("DELETE questions FROM questions WHERE question_id = %s;", (question_id,))
        mysql.connection.commit()
        flash(f"question - {question_id} is now deleted", "success")
        return redirect(url_for('Manage_forum.admin_service_forum'))
    else:
        flash("Plase login as service or admin to edit Forum", "warning")
        return redirect(url_for('login.rendering_login'))
    
@Manage_forum.route('/admin_service_delete_comment')
def delete_comment():
    if 'loggedin' in session and session['permission_name'] in ('service', 'admin'):
        comment_id = request.args.get("comment_id")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # delete the account in account table, automatically delete staff with that accountid
        cursor.execute("DELETE comments FROM comments WHERE comment_id = %s;", (comment_id,))
        mysql.connection.commit()
        flash(f"comment - {comment_id} is now deleted", "success")
        return redirect(url_for('Manage_forum.admin_service_forum'))
    else:
        flash("Plase login as service or admin to edit Forum", "warning")
        return redirect(url_for('login.rendering_login'))