import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from flask import render_template, url_for, flash, redirect, request, Blueprint, Flask, session, send_from_directory, current_app
from wtforms import Form
from flask_login import login_user, current_user, logout_user, login_required, fresh_login_required
from photomind import db, bcrypt, limiter
from photomind.models import User, Post
from photomind.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, NewPasswordForm)
from photomind.users.utils import allowed_file
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from photomind.config import Config
from flask_limiter.util import get_remote_address
from photomind.nocache import nocache


from flask import escape

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
@limiter.limit('5/day') # Only get to access the register-page from you IP 5 times a day, which means that yuou cannot making several account
def register(): 
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(escape(form.password.data)).decode('utf-8')
        hashed_answer = bcrypt.generate_password_hash(escape(form.answer.data)).decode('utf-8')
        user = User(username=escape(form.username.data), email=form.email.data, password=hashed_password, question=form.question.data, answer=hashed_answer)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
@limiter.limit('50/day; 20/hour; 5/minute')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, escape(form.password.data)):
            login_user(user, remember=form.remember.data, duration=timedelta(days=30))
            user.last_login_at = datetime.now()
            user.last_login_ip = get_remote_address()
            user.active = True 
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password.','error')
        session.permanent = True
    return render_template('login.html', title='Login', form=form)


@users.route("/newpassword", methods=['GET', 'POST'])
@limiter.limit('1/day')
def newpassword():
    form = NewPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if bcrypt.check_password_hash(user.answer, escape(form.answer.data)) and user.question == form.question.data:
            hashed_password = bcrypt.generate_password_hash(escape(form.password.data)).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('users.login'))
        else:
            flash('New password unsuccesful. Please check you email, question and answer.', 'error')
            return redirect(url_for('users.newpassword'))
    return render_template('newpassword.html', title="New Password", form=form)

@users.route("/logout")
def logout():
    user = current_user
    user.active = False
    db.session.commit()
    logout_user()
    return redirect(url_for('main.home'))



def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))



@users.route("/account", methods=['GET', 'POST'])
@fresh_login_required
@nocache
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            file = form.picture.data
            if file.filename == '':
                flash('No filename')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                picture_path = os.path.join(current_app.root_path, 'static/profile_pics', filename)
                file.save(picture_path)
                current_user.image_file = filename
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)



@users.route("/user/<string:username>")
@login_required
@nocache
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

    



