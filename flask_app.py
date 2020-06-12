from datetime import datetime
from pytz import timezone

fr_tz = timezone('Europe/Paris') # French time zone
from functools import wraps

from flask import Flask, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

def _Message(*args, **kwargs):
    return Message(*args, sender=app.config['MAIL_SENDER'], **kwargs)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail(app)

################################################################################
# Definition of the database
# Definition of load_user
################################################################################
from module_database import Student, Teacher, Classroom, Activity, Question, HelpingHand, HelpingHandLog, load_user

from module_email import send_confirmation_email, EMAIL_CONFIRMATION_SALT, RESET_PASSWORD_SALT, send_reset_password_email


################################################################################
# Definition of administration tools
# Each app.route should use a login + admin verification
################################################################################

from module_admin import (
    admin, create_classroom, delete_classroom, add_student_to_classroom,
    remove_student_from_classroom, _remove_student_from_classroom,
    create_helping_hand, view_activity_logs,
    link_student, _remove_activity_from_classroom, remove_activity_from_classroom,
    add_activity_to_classroom, delete_activity, add_multi_students_to_classroom
)

################################################################################
# Definition of student accesses to helping-hands
# Each app.route should use a login verification
################################################################################

from module_student import student, access_activity, show_helping_hand, link_to_teacher

################################################################################
# Definition of account parameters (password, email, etc)
# Definition of login page
################################################################################

from module_account import login, logout, account, create_account, reset_password, reset_password_token

################################################################################
# Definition of 'semi-static' posts (e.g. about, faq, etc)
# Each post is a markdown file in posts/ directory
################################################################################

from module_posts import post, list_posts

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/privacy/")
def privacy():
    return render_template("privacy.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("main_page.html")

@app.route("/stats/")
def stats():
    if current_user.is_authenticated:
        if current_user.username == app.config['ADMIN_USERNAME']:
            return render_template("stats.html", Teacher=Teacher, Student=Student, fr_tz=fr_tz)
    else:
        return redirect('/')