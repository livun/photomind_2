from datetime import datetime
from flask import current_app, url_for, redirect, session
from photomind import db, login_manager, admin
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, fresh_login_required
from photomind.config import Config
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    question = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(30), nullable=False)    
    posts = db.relationship('Post', backref='author', lazy=True)
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    active = db.Column(db.Boolean)
    role = db.Column(db.String(10), nullable=False, default='user')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



class MyModelView(ModelView):
    def is_accessible(self):
            return current_user.role == 'admin'
             
        

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login', next=request.url))

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))


