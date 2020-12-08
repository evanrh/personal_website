from flask import render_template, url_for, redirect, request, flash, jsonify
import json
from . import admin
from .forms import NewPostForm, EditPostForm
from ..models import User, Post, Category
from .. import db
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
    print(current_user.id)
    p = Post.query.order_by(Post.timestamp.desc()).all()
    form = NewPostForm()
    editForm = EditPostForm()
    return render_template('admin/posts.jinja2', posts=p, form=form, editForm=editForm)

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
            output['categories'] = [x.name.capitalize() for x in post.categories]
    
    return jsonify(output)

# AJAX route for a new post submission
@admin.route('_post-edit', methods=['POST'])
def postEdit():
    form = NewPostForm()
    editForm = EditPostForm()
    
    # Case for edit form being submitted
    if editForm.validate_on_submit():

        formCats = [cat.data.lower() for cat in form.categories.entries]
        post = Post.query.get(editForm.id.data)

        added = list(set(formCats) - set([x.name for x in post.categories]))
        deleted = list(set([x.name for x in post.categories]) - set(formCats))
        indexes = []
        for i,x in enumerate(post.categories):
            if x.name in deleted:
                indexes.append(i)
        for i in indexes:
            del post.categories[i]
        
        categories = []
        for name in added:
            cat = Category.query.get(name)
            # cat == None if the category is not in the table
            if not cat:
                cat = Category(name=name)
            categories.append(cat)
        
        post.title = form.title.data
        post.preview = form.preview.data
        post.body = form.body.data

        for cat in categories:
            post.categories.append(cat)
        db.session.commit()

        return jsonify({'message': 'success'})
    
    if request.method == 'POST':

        # Case for if submitted for is the new post form
        if form.validate_on_submit():

            # Create category objects
            categories = []
            for entry in form.categories.entries:
                name = entry.data.lower()
                cat = Category.query.get(name)
                # cat == None if the category is not in the table
                if not cat:
                    cat = Category(name=name)
                categories.append(cat)
            
            post = Post()
            post.user_id = current_user.id
            post.title = form.title.data
            post.preview = form.preview.data
            post.body  = form.body.data

            for cat in categories:
                post.categories.append(cat)
            
            db.session.add(post)
            db.session.commit()

            return jsonify({'message': 'success'})

        return jsonify({'message': 'no validate'})
    
    return jsonify({'message': 'failure'})

# AJAX route for a updating a post
@admin.route('_new-post', methods=['POST'])
def editPost():
    form = EditPostForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():

            # Create category objects
            categories = []
            for entry in form.categories.entries:
                name = entry.data.lower()
                cat = Category.query.get(name)
                # cat == None if the category is not in the table
                if not cat:
                    cat = Category(name=name)
                categories.append(cat)
            
            post = Post()
            post.title = form.title.data
            post.preview = form.preview.data
            post.body  = form.body.data

            for cat in categories:
                post.categories.append(cat)
            
            db.session.add(post)
            db.session.commit()

            return jsonify({'message': 'success'})
        return jsonify({'message': 'no validate'})
    
    return jsonify({'message': 'failure'})

# AJAX route for updating post content, or creating a new post
@admin.route('_update-post', methods=['POST'])
def update():
    output = {}
    output['message'] = 'failure'
    print(request.json)
    # Client should send back, id, post title, post body, and any categories
    if request.json:
        data = request.json
        # Conditional determines if it is a new post or an updated one based off of id existing
        post = Post.query.get(data['id']) if 'id' in data else Post()
        post.title = data['title']
        post.preview = data['preview']
        post.body = data['body']
        
        # Add new post to database session
        if 'id' not in data:
            db.session.add(post)
        db.session.commit()
            
        output['message'] = 'success'

    return jsonify(output)