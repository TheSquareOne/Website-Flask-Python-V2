from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField
from wtforms.validators import InputRequired
import os

# Form used for multiple file uploading
class UploadForm(FlaskForm):
    files = MultipleFileField('Browse',
                              validators=[InputRequired('File is required')])
    submit = SubmitField('Upload')
