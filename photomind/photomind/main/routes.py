from flask import render_template, request, Blueprint
from photomind.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

<<<<<<< HEAD
@main.route("/admin")
@basic_auth.required
def admin_view():
    return render_template('admin.html')


#if __name__ == "__main__":
#    main.run(ssl_context='adhoc')

# flask run --cert=adhoc
=======
>>>>>>> 5cf015f31d82db9e6d9eae130e999943b4460f54
