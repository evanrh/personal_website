from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    pwd_hash = db.Column(db.String(128))


    def __repr__(self):
        return '<User {}>'.format(self.username)
