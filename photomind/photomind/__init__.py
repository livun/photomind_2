from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from photomind.config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
limiter = Limiter(key_func=get_remote_address)


talisman = Talisman()
csp = {
    'default-src': [
        '\'self\'',
        'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'
    ]
}


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)

  

    # The time, in seconds, that the browser should remember that this site is only to be accessed using HTTPS.
    # If this optional parameter is specified, this rule applies to all of the site’s subdomains as well.
    talisman.init_app(
        app, 
        strict_transport_security=31536000,         
        content_security_policy=csp
    )

    from photomind.users.routes import users
    from photomind.posts.routes import posts
    from photomind.main.routes import main
    from photomind.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app