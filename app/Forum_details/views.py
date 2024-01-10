from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

Forumdetails = Blueprint('Forumdetails', __name__)


@Forumdetails.route('/Forum_details')
def etails():
    return render_template('Forum_details.html')