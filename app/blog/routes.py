from flask import render_template, url_for, redirect, request
from . import blog
from ..models import User, Post
from .. import db
from .forms import UploadForm
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = ['md']
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blog.route('/', methods=["GET"])
def index():
    posts = Post.query.all()
    return render_template('blogHome.jinja2', posts=posts, title="Blog posts")

@blog.route('/posts/<int:id>', methods=['GET'])
def posts(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('post.html', post=post)

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
                post = Post(title=form.title.data, body=text, user_id=current_user.id)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('blog.upload'))
    return render_template('upload.html', title="Upload New Post", form=form)