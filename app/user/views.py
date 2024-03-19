from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

user = Blueprint('user', __name__)


@user.route('/user')
def users():
    return '用户'