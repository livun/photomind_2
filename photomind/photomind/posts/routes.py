
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, escape)
from flask_login import current_user, login_required
from photomind import db
from photomind.models import Post
from photomind.posts.forms import PostForm
from photomind.nocache import nocache



posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
@nocache
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=escape(form.title.data), content=escape(form.content.data), author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
@login_required
@nocache
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
@nocache
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = escape(form.title.data)
        post.content = escape(form.content.data)
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['GET'])
@login_required
@nocache
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.after_request
def headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self' https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '0'
    response.headers['X-Permitted-Cross-Domain-Policies']='none'
    response.headers['Referrer-Policy']='strict-origin-when-cross-origin'
    return response

