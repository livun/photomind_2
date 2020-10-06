from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from photomind.config import Config
from datetime import timedelta


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    #app.config.from_object(Config)
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from photomind.users.routes import users
    from photomind.posts.routes import posts
    from photomind.main.routes import main
    from photomind.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app