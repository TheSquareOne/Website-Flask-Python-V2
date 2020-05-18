from flask import render_template, url_for, request, redirect, flash, current_app
from flask_login import login_required
from app.upload import bp
from werkzeug.utils import secure_filename
from app.upload.forms import UploadForm
from app.models import User
import os

# File uploading route
@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            # If there is no files in request, redirect to home
            if 'files' not in request.files:
                flash('Missing file in request')
                redirect(url_for('main.home'))
            # Get list of files
            files = request.files.getlist('files')
            # Go through every file
            for file in files:
                if file:
                    # Make filename secure
                    filename = secure_filename(file.filename)
                    # Save file
                    file.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
            flash('Upload complete!')
            redirect(url_for('upload.upload_file'))
    return render_template('upload/upload.html', form=form)


# File uploading route for API (e.g. ShareX)
@bp.route('/api/upload', methods=['POST'])
def api_upload_file():
    # Check if there is any files in request
    if 'files' not in request.files:
        return 'Missing files from request.'
    # Check if there is authentication token
    if 'Auth' not in request.headers:
        return 'Missing authentication token'
    user = User.query.filter_by(api_token=request.headers.get('Auth')).first()
    # Check is user with authentication token exist
    if user is not None:
        # Get list of files
        files = request.files.getlist('files')
        # Go through every file
        for file in files:
            if file:
                # Make filename secure
                filename = secure_filename(file.filename)
                # Save file
                file.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
        return 'Upload complete'
    return 'Wrong authentication token'
