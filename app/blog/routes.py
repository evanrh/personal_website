from flask import render_template, url_for, redirect, request, flash, make_response
from . import blog
from ..models import User, Post, Category
from .. import db
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import func
from feedgen.feed import FeedGenerator
from datetime import datetime

def title_to_url(title):
    return '-'.join([x.lower() for x in title.split(' ')])
@blog.route('/', methods=["GET"])
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog.jinja2', posts=posts, title="Blog Home")

@blog.route('/posts', methods=['GET'])
def posts():
    return redirect(url_for('blog.index'))

@blog.route('/rss')
def rss():
    fg = FeedGenerator()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    root = request.url_root
    root = root[0: len(root) - 1]
    fg.title("Evan's Blog Feed")
    fg.description('A feed for all posts made on my blog')
    fg.link(href=root)

    for post in posts:
        fe = fg.add_entry()
        fe.title(post.title)
        fe.link(href=root + url_for('blog.post', postname=title_to_url(post.title)))
        fe.description(post.preview)
        fe.author(name='{} {}'.format(post.author.first_name, post.author.last_name))
        fe.pubDate(post.timestamp.astimezone().isoformat())
    
    # Make rss into a renderable string and change content type header
    response = make_response(fg.rss_str(pretty=True))
    response.headers.set('Content-Type', 'application/rss+xml')

    return response
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