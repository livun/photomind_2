from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

avoid = ["=", "/", "<", ">", "&", '"', "#", "-", ";", "(", ")", "@", "\\", "|"]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_content(self, content):
        for char in content.data:
            for i in range(len(avoid)):
                if avoid[i] == char:
                    raise ValidationError('Special characters in post is not allowed')

    def validate_title(self, title):
        for char in title.data:
            for i in range(len(avoid)):
                if avoid[i] == char:
                    raise ValidationError('Special characters in title is not allowed')

                                    