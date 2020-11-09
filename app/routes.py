from app import app
from flask import render_template, redirect, url_for, flash
from flask import request, jsonify
from flask import send_from_directory
from flask_login import current_user, login_user
from app.forms import LoginForm
from .db_connect import DB_Connection

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Resume')

@app.route('/ip-api', methods=['GET'])
def get_ip():
    ip = request.headers.get('X-Forwarded-For')
    if request.args.get('json'):
        return jsonify({'ip': ip}), 200
    else:
        return render_template('ip-api.html', title='Get Your IP', 
                user_ip=ip)

@app.route('/signup', methods=["POST"])
def signup():
    return 

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
    
@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/site-info')
def site():
    return render_template('site-info.html', title='Site Info')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title='Portfolio')

@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(app.static_folder, request.path[1:])

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
