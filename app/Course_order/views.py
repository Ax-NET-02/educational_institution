from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

Course_order = Blueprint('Course_order', __name__)


@Course_order.route('/course_order')
def course_order():
    return render_template('Course_order.html')