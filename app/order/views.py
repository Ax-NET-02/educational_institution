from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

order = Blueprint('order', __name__)


@order.route('/order')
def orders():
    return render_template('Paypal.html')