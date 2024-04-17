from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

Dashboard = Blueprint('Dashboard', __name__)


@Dashboard.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin.html')

@Dashboard.route('/service_dashboard')
def service_dashboard():
    return render_template('service.html')

@Dashboard.route('/user_dashboard')
def user_dashboard():
    return render_template('user.html')