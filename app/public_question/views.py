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