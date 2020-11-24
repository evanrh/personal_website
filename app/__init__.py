from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'home.login'
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config())

    with app.app_context():

        # Initialize database, login manager, migration, and assets with app
        db.init_app(app)
        migrate.init_app(app, db)
        login.init_app(app)
        Markdown(app)

        from .blog import blog
        from .home import home
        from .asset import compile_static_assets

        # Register blueprints
        app.register_blueprint(home)
        app.register_blueprint(blog)

        # Compile static assets

        return app