from flask import render_template, url_for, redirect, request, flash, jsonify
import json
from . import admin
from ..models import User, Post, Category
from .. import db
#from .forms import UploadForm
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

# Require user to be logged in before any route can be accessed
@admin.before_request
@login_required
def func():
    pass

@admin.route('/')
def index():
    return render_template('admin/home.jinja2')

@admin.route('/posts')
def posts():
    p = Post.query.all()
    return render_template('admin/posts.jinja2', posts=p)

# AJAX Preview Rendering
@admin.route('/_preview', methods=['POST'])
def preview():
    output = {}
    output['message'] = 'failure'

    if request.json:
        data = request.json
        if data["postText"]:
            output['message'] = 'success'
            output['content'] = render_template("admin/post_preview.jinja2", md=data["postText"])
    
    # Bad input or no markdown defined
    return jsonify(output)

# AJAX Content getter for post
@admin.route('_post-content', methods=['POST'])
def content():
    output = {}
    output['content'] = ''

    if request.json:
        data = request.json
        if data['id']:
            post = Post.query.get(int(data['id']))
            output['content'] = post.body
            output['title'] = post.title
            output['preview'] = post.preview
    
    return jsonify(output)

@admin.route('_update-post', methods=['POST'])
def update():
    output = {}
    output['message'] = 'failure'
    print(request.json)
    # Client should send back, id, post title, post body, and any categories
    if request.json:
        data = request.json
        p = Post.query.get(data['id'])
        p.title = data['title']
        p.preview = data['preview']
        p.body = data['body']
        db.session.commit()
        
        output['message'] = 'success'

    return jsonify(output)