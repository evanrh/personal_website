from flask import Flask
from flask_login import LoginManager
from config import Config

app = Flask(__name__, static_folder='static')
login = LoginManager()

app.config.from_object(Config())

from app import routes, models, hooks
from app.models import db, migrate

db.init_app(app)
migrate.init_app(app)
hooks.webhook.init_app(app)