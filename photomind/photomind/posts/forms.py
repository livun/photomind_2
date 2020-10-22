from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from photomind.models import Post

avoid = ['#', '$', '%', '/', '(', ')', '=', '{', '}', '[', ']', ':', ';', '\\', '*', '@', '^', '¨', '~', '§']

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_content(self, content):
        content = content.data
        for i in avoid:
            if i in content:
                raise ValidationError('Special characters is not allowed, try again.')

    def validate_title(self, title):
        title = title.data
        for i in avoid:
            if i in title:
                raise ValidationError('Special characters is not allowed, try again.')