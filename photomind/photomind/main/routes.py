from flask import render_template, request, Blueprint, session
from photomind.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    session['attempt'] = 5
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

