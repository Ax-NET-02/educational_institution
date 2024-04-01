from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

course = Blueprint('course', __name__)


@course.route('/course')
def courses():
    return render_template('course.html')