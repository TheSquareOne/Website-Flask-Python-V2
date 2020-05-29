from flask import flash, current_app
from app.upload.crypto import encrypt_data
import os
import secrets

# Return user specific upload path
def get_upload_path(user):
    # Use MAGIC_WORD as a secret padding
    padding = os.environ.get('MAGIC_WORD')
    # Add some padding to user ID to make encrypted string longer
    # Hide user ID in URLs by encrypting it
    user_id = encrypt_data(str(user.id) + padding)
    # Get user upload path
    full_path = os.path.join(current_app.config['UPLOAD_PATH'], user_id)
    # If user doesn't have own upload folder, create it
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    # Return upload path
    return full_path


# Check if file is allowed
# Return True or False
def allowed_file(file):
    # Check if there is not dot in filename
    if '.' not in file.filename:
        return False
    # Check if file extension is not allowed
    if file.filename.rsplit('.', 1)[1].lower() not in current_app.config['ALLOWED_FILES']:
        return False
    return True


# Verify that all files are valid
# Return True or False
def verify_files(files):
    for file in files:
        if file:
            # Check there is name for file
            if file.filename == '':
                flash('Missing filename')
                return False
            # Check file is allowed
            if not allowed_file(file):
                flash('File format not allowed')
                return False
        else:
            flash('Missing file')
            return False
    return True


# Add 6 random characters at the end of duplicate filename
def rename_duplicate(filename):
    # Split filename into name and extension
    filename = filename.rsplit('.', 1)
    # Add '_' and 4+2 random characters before extension
    filename = filename[0] + '_' + secrets.token_urlsafe(4) + '.' + filename[1]
    return filename
