from flask import render_template, url_for, redirect, request, flash
from . import blog
from ..models import User, Post, Category
from .. import db
from .forms import UploadForm
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import func

ALLOWED_EXTENSIONS = ['md']
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blog.route('/', methods=["GET"])
def index():
    posts = Post.query.all()
    return render_template('blog.jinja2', posts=posts, title="Blog Home")

@blog.route('/posts', methods=['GET'])
def posts():
    return redirect(url_for('blog.index'))

@blog.route('/posts/<string:postname>', methods=['GET'])
def post(postname):
    post = Post.query.filter(Post.title.ilike(' '.join(postname.split('-')))).first_or_404()
    print(' '.join(postname.split('-')))
    print(post)
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

@blog.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = form.post.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                text = ''.join([line.decode('utf-8') for line in file])
                post = Post(title=form.title.data, body=text, user_id=current_user.id, preview=form.preview.data)
                if 'categories' in request.form.keys():
                    categories = [x.strip().lower() for x in form.categories.data.split(',')]
                    cats_in_db = [x.name for x in Category.query.filter(Category.name.in_(categories))]
                    categories = list(map(lambda x: Category.query.filter_by(name=x).first() if x in cats_in_db else Category(name=x), categories))
                    print(categories)
                    for cat in categories:
                        print(cat)
                    _ = list(map(lambda c: post.categories.append(c), categories))
                db.session.add(post)
                db.session.commit()
                flash('Successfully uploaded post!')
                return redirect(url_for('blog.upload'))
            else:
                flash('Unallowed filetype or no file data')
                return redirect(url_for('blog.upload'))
    return render_template('upload.jinja2', title="Upload New Post", form=form)
