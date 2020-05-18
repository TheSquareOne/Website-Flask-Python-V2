from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import MultipleFileField, SubmitField, FileField
from wtforms.validators import ValidationError, InputRequired
import os

# Form used for multiple file uploading
class UploadForm(FlaskForm):
    files = MultipleFileField('Browse',
                              validators=[InputRequired('File is required')])
    remove_file = SubmitField('Remove')
    submit = SubmitField('Upload')

    # Validate that file type is allowed
    # File must have dot and allowed extension at the end
    def validate_files(self, files):
        # Check every file
        for file in files.data:
            # Use try to catch exceptions
            try:
                if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in os.environ.get('ALLOWED_FILES'):
                    raise ValidationError('Wrong file type')
            # rsplit() raises IndexError if file without extension is submitted
            except IndexError:
                    raise ValidationError('Wrong file type')
