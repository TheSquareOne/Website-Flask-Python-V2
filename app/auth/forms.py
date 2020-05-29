from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User

# Form for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


# Form for signup
class SignUpForm(FlaskForm):
    # Requirements:
    # Password min 10 characters
    # Username 2-15 characters and atleast 1 letter
    username = StringField('Username',
                validators=[DataRequired(),
                            Length(min=2, max=15,
                                message='Must be between 2-15 characters.')])
    password = PasswordField('Password',
                validators=[DataRequired(),
                            Length(min=10,
                                message='Minimum length %(min)d characters.')])
    password_2 = PasswordField('Confirm Password',
                validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Signup')

    # Validate username
    def validate_username(self, username):
        # Check if username has atleast one letter
        for char in username.data:
            if char.isalpha():
                break
        else:
            raise ValidationError('Must have one letter.')

        # Check if username already exist in db
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already in use.')

    # Validate email
    def validate_email(self, email):
        # Check if email already exist in db
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already in use.')


# Password reset request form
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


# Password reset form
class PasswordResetForm(FlaskForm):
    # Requirements
    # Password min 10 characters
    password = PasswordField('Password',
                validators=[DataRequired(),
                            Length(min=10,
                                message='Minimum length %(min)d characters.')])
    password_2 = PasswordField('Confirm password',
                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request password reset')
