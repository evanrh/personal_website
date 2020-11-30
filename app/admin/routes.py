from flask import render_template, url_for, redirect, request, flash
from . import admin
from ..models import User, Post, Category
from .. import db
#from .forms import UploadForm
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

@admin.before_request
@login_required
def func():
    pass

@admin.route('/')
def index():
    return render_template('admin/home.jinja2')