from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

register = Blueprint('register', __name__)


@register.route('/register')
def Get_register():
    return render_template('cs.html')