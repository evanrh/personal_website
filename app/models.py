from flask_login import UserMixin
from flask import request
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from app import db, login

categories = db.Table('categories',
                        db.Column('category_name', db.String(25), db.ForeignKey('category.name'), primary_key=True),
                        db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(128), index=True, unique=True)
    pwd_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text, nullable=False)
    preview = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(timezone=True), index=True, default=datetime.now, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    categories = db.relationship('Category', secondary=categories, lazy='subquery',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Category(db.Model):
    __tablename__ = "category"
    name = db.Column(db.String(25), primary_key=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)

# Site analytics table. Keeps track of site visitors, where they come from, and a little about their browser
class PageView(db.Model):
    __tablename__ = 'page_view'
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.Text)
    url = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, nullable=False, default=datetime.now)
    title = db.Column(db.Text, default='')
    ip = db.Column(db.String(15), default='')
    referrer = db.Column(db.Text, default='')
    headers = db.Column(db.JSON)
    params = db.Column(db.JSON)

    def __repr__(self):
        return '<PageView {}: {}: {}>'.format(self.ip, self.url, self.timestamp)
    # Create a new PageView instance when a request is made
    @classmethod
    def create_from_request(cls):
        parsed = url_parse(request.args['url'])
        params = request.args

        return PageView(
            domain = parsed.netloc,
            url = parsed.path,
            title = request.args.get('t') or '',
            ip = request.headers.get('X-Forwarded-For', request.remote_addr),
            referrer = request.args.get('ref') or '',
            headers = dict(request.headers),
            params = params
        )
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
