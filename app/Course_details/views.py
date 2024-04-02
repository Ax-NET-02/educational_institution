from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

Course_details = Blueprint('Course_details', __name__)


@Course_details.route('/course_details')
def course_details():
    return render_template('Course_details.html')