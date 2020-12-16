from ..models import User, Post, PageView
from flask import render_template, redirect, url_for, flash, abort
from flask import request, jsonify, Response
from flask import send_from_directory
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from base64 import b64decode
from datetime import timedelta
from .forms import LoginForm
from . import home
from .. import db

@home.route('/')
def index():
    return render_template('index.html', title='Home')

@home.route('/resume')
def resume():
    print(url_for('home.static', filename='css/resume.css'))
    return render_template('resume.html', title='Resume')

@home.route('/login', methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('home.login'))
        # Set user remember me good for 1 day
        login_user(user, remember=form.remember_me.data, duration=timedelta(days=1))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@home.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))

"""
@home.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
"""

@home.route('/site-info')
def site():
    return render_template('site-info.html', title='Site Info')

@home.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title='Portfolio')

@home.route("/robots.txt")
def robots_txt():
    return send_from_directory(home.static_folder, request.path[1:])

@home.route('/static/a.gif')
def analyze():
    if not request.args.get('url'):
        abort(404)
    
    beacon = b64decode('R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')

    # Create page view and add to database
    page = PageView.create_from_request()
    db.session.add(page)
    db.session.commit()

    response = Response(beacon, mimetype='image/gif')
    response.headers['Cache-Control'] = 'private, no-cache'
    return response

@home.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@home.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
