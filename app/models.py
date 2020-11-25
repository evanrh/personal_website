from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

categories = db.Table('categories',
                        db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
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
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    categories = db.relationship('Category', secondary=categories, lazy='subquery',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), index=True, unique=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))