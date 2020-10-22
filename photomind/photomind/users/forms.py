from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from photomind.models import User

avoid = ['#', '$', '%', '/', '(', ')', '=', '{', '}', '[', ']', ':', ';', '\\', '*', '^', '¨', '~', '§']

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=16, max=64)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    question = SelectField('Questions', choices = ["What was the house number and street name you lived in as a child?",
            "What is your oldest cousin’s first name?",
            "What primary school did you attend?", "In what town or city was your first full time job?",
            "What is the middle name of your oldest child?"], validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        for i in avoid:
            if i in username.data:
                raise ValidationError('Special characters is not allowed, try again.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        for i in avoid:
            if i in email.data:
                raise ValidationError('Special characters is not allowed, try again.')

    def validate_password(self, password):
        password = password.data
        for i in avoid:
            if i in password:
                raise ValidationError('Special characters is not allowed, try again.')

    def validate_answer(self, answer):
        answer = answer.data
        for i in avoid:
            if i in answer:
                raise ValidationError('Special characters is not allowed, try again.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        for i in avoid:
            if i in email.data:
                raise ValidationError('Special characters is not allowed, try again.')

    def validate_password(self, password):
        password = password.data
        for i in avoid:
            if i in password:
                raise ValidationError('Special characters is not allowed, try again.')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
        for i in avoid:
            if i in username.data:
                raise ValidationError('Special characters is not allowed, try again.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')




class NewPasswordForm(FlaskForm):
    email = StringField('Email',
                    validators=[DataRequired(), Email()])
    question = SelectField('Questions', choices = ["What was the house number and street name you lived in as a child?",
            "What is your oldest cousin’s first name?",
            "What primary school did you attend?", "In what town or city was your first full time job?",
            "What is the middle name of your oldest child?"], validators=[DataRequired()])
    answer = StringField('Aswer', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=16, max=64)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        for i in avoid:
            if i in email.data:
                raise ValidationError('Special characters is not allowed, try again.')

    def validate_password(self, password):
        password = password.data
        for i in avoid:
            if i in password:
                raise ValidationError('Special characters is not allowed, try again.')

    def validate_answer(self, answer):
        answer = answer.data
        for i in avoid:
            if i in answer:
                raise ValidationError('Special characters is not allowed, try again.')