from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone
import json

LearningForum = Blueprint('LearningForum', __name__)


@LearningForum.route('/Learning_Forum')
def forum():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT
            questions.*, 
            users.user_img
        FROM
            questions,
            users
        WHERE
            questions.publisher_id = users.user_id
    """
    cursor.execute(sql)
    forum_data = cursor.fetchall()
    return render_template('Learning_Forum.html', forum_data=forum_data)

@LearningForum.route('/forum_detailed')
def forum_detailed():
    question_id = request.args.get("question_id")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT
            questions.*, 
            users.user_img
        FROM
            questions,
            users
        WHERE
            questions.publisher_id = users.user_id AND
            questions.question_id = %s
    """
    
    comments_sql = """
        SELECT
            comments.comment_content, 
            comments.commenter_name, 
            comments.question_id, 
            comments.user_id, 
            users.user_img, 
            questions.publish_date
        FROM
            comments
            INNER JOIN
            questions
            ON 
                comments.question_id = questions.question_id
            INNER JOIN
            users
            ON 
                comments.user_id = users.user_id
        WHERE
            comments.question_id = %s;
    """
    
    quantity_sql = """
        SELECT
            COUNT(question_id) AS quantity
        FROM
            comments
        WHERE
            comments.question_id = %s
    """
    
    cursor.execute(sql, question_id)
    forum_detailed = cursor.fetchall()
    
    cursor.execute(comments_sql, question_id)
    comment_data = cursor.fetchall()
    
    cursor.execute(quantity_sql, question_id)
    quantity_data = cursor.fetchall()
    return render_template('forum_detailed.html', forum_detailed=forum_detailed, comment_data=comment_data, quantity_data=quantity_data)

@LearningForum.route('/comment_data', methods = ['POST'])
def comment_data():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    comment_content = request.form['comment_content'].strip()
    commenter_name = session.get('user_name')
    question_id = request.form['question_id'].strip()
    user_id = session.get('user_id')

    sql = """
    INSERT INTO comments (comment_content, commenter_name, question_id, user_id) VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (comment_content, commenter_name, question_id, user_id))
    mysql.connection.commit()
    
    question_id = request.form['question_id'].strip()
    sql = """
        SELECT
            questions.*, 
            users.user_img
        FROM
            questions,
            users
        WHERE
            questions.publisher_id = users.user_id AND
            questions.question_id = %s
    """
    
    comments_sql = """
        SELECT
            comments.comment_content, 
            comments.commenter_name, 
            comments.question_id, 
            comments.user_id, 
            users.user_img, 
            questions.publish_date
        FROM
            comments
            INNER JOIN
            questions
            ON 
                comments.question_id = questions.question_id
            INNER JOIN
            users
            ON 
                comments.user_id = users.user_id
        WHERE
            comments.question_id = %s;
    """
    quantity_sql = """
        SELECT
            COUNT(question_id) AS quantity
        FROM
            comments
        WHERE
            comments.question_id = %s
    """
    
    cursor.execute(sql, question_id)
    forum_detailed = cursor.fetchall()
    
    cursor.execute(comments_sql, question_id)
    comment_data = cursor.fetchall()
    
    cursor.execute(quantity_sql, question_id)
    quantity_data = cursor.fetchall()
    return render_template('forum_detailed.html', forum_detailed=forum_detailed, comment_data=comment_data, quantity_data=quantity_data)

@LearningForum.route('/manage_forum')
def manage_forum():
    user_id = session.get('user_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT
            questions.*
        FROM
            questions
        JOIN
            users ON questions.publisher_id = users.user_id
        WHERE
            users.user_id = %s
    """
    
    cursor.execute(sql, (user_id, ))
    user_forum = cursor.fetchall()
    return render_template('Manage_community.html', user_forum=user_forum)


@LearningForum.route('/delete_forum')
def delete_forum():
        question_id = request.args.get("question_id")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # delete the account in account table, automatically delete staff with that accountid
        cursor.execute("DELETE questions FROM questions WHERE question_id = %s;", (question_id,))
        mysql.connection.commit()
        flash(f"question - {question_id} is now deleted", "success")
        return redirect(url_for('LearningForum.manage_forum'))
    
@LearningForum.route('/delete_comment')
def delete_comment():
        comment_id = request.args.get("comment_id")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # delete the account in account table, automatically delete staff with that accountid
        cursor.execute("DELETE comments FROM comments WHERE comment_id = %s;", (comment_id,))
        mysql.connection.commit()
        flash(f"comment - {comment_id} is now deleted", "success")
        return redirect(url_for('LearningForum.manage_comment'))
    
@LearningForum.route('/manage_comment')
def manage_comment():
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
    comment = cursor.fetchall()
    return render_template('comment.html', comment_data=comment)
    