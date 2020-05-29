from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

# Profile editing form
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=200)])
    submit = SubmitField('Submit')

    # This is needed for username change to work!
    # Not exactly sure what this does,
    # but it invokes the class constructor in the parent class.
    # Super is used as a shortcut to access a parent class.
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    # Validate new username
    def validate_username(self, username):
        # Compare if username is different from previous one
        if username.data != self.original_username:
            # Query with new username, return user obj or None
            user = User.query.filter_by(username=self.username.data).first()
            # If returned user obj username is already in use
            if user is not None:
                raise ValidationError('Username already in use.')
