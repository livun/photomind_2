from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from photomind.config import Config
from flask_limiter import Limiter


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
limiter = Limiter()


def create_app(config_class=Config):
    app = Flask(__name__)
<<<<<<< HEAD
    app.config.from_object(Config)
    
=======
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    #app.config.from_object(Config)
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB max-limit

>>>>>>> 3694e24b251c646fe7eae11f22b1042f3cef7a53
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)

    from photomind.users.routes import users
    from photomind.posts.routes import posts
    from photomind.main.routes import main
    from photomind.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app