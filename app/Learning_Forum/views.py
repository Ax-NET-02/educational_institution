from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

LearningForum = Blueprint('LearningForum', __name__)


@LearningForum.route('/Learning_Forum')
def forum():
    return render_template('Learning_Forum.html')