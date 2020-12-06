from flask import render_template, url_for, redirect, request, flash
from . import blog
from ..models import User, Post, Category
from .. import db
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import func

ALLOWED_EXTENSIONS = ['md']
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blog.route('/', methods=["GET"])
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog.jinja2', posts=posts, title="Blog Home")

@blog.route('/posts', methods=['GET'])
def posts():
    return redirect(url_for('blog.index'))

@blog.route('/posts/<string:postname>', methods=['GET'])
def post(postname):

    # Query to get the post name if it matches the url postname. ilike is an insensitive regex of sorts
    post = Post.query.filter(Post.title.ilike(' '.join(postname.split('-')))).first_or_404()
    categories = [cat.name for cat in post.categories if cat.name != '']
    return render_template('post.jinja2', post=post, title=post.title, categories=categories)

@blog.route('/posts/category/<string:category>')
def postsCategory(category):
    posts = Category.query.get_or_404(category)

    if posts:
        return render_template('post_list.jinja2', posts=posts.posts, title="Category: {}".format(category.capitalize()))
    else:
        flash('No such category')
        return redirect(url_for('blog.index'))