from flask import render_template, url_for, request, redirect, flash, current_app, send_from_directory, Markup
from flask_login import login_required, current_user
from app.upload import bp
from werkzeug.utils import secure_filename
from app.upload.forms import UploadForm
from app.upload.manage import get_upload_path, verify_files, rename_duplicate
from app.upload.crypto import encrypt_data
import os

# File uploading route, from website
@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # If there is no files in request, redirect back with message
            if 'files' not in request.files:
                flash('Missing files part in request')
                return redirect(url_for('upload.upload_file'))
            # Get list of files
            files = request.files.getlist('files')
            # Verify that files are allowed
            if verify_files(files):
                for file in files:
                    # Make filename secure
                    filename = secure_filename(file.filename)
                    # Get upload path
                    path = get_upload_path(current_user)
                    # If same filename already exist, add 6 random characters
                    # at the end of file name
                    if os.path.exists(os.path.join(path, filename)):
                        filename = rename_duplicate(filename)
                    # Save file
                    file.save(os.path.join(path, filename))
                    # URL for uploaded file
                    url = url_for('upload.view_file', id=path.rsplit('/', 1)[1],
                                                       filename=filename,
                                                       _external=True)
                    # Link for uploaded file
                    flash(Markup('<a href="{0}">{1}</a>'.format(url, filename)))
                flash('Upload complete!')
                return redirect(url_for('upload.upload_file'))
            else:
                return redirect(url_for('upload.upload_file'))
    return render_template('upload/upload.html', form=form)


# File uploading route for API (e.g. ShareX)
# Login is required through user API token
@bp.route('/api/upload', methods=['POST'])
@login_required
def api_upload_file():
    # Return error message, if there was no files in request
    if 'files' not in request.files:
        return 'No files in request.'
    # Get list of files
    files = request.files.getlist('files')
    # Verify each file
    if verify_files(files):
        # Go through every file
        for file in files:
            # Make filename secure
            filename = secure_filename(file.filename)
            # Get upload path for user
            path = get_upload_path(current_user)
            # If same filename already exist, add 6 random characters
            # at the end of file name
            if os.path.exists(os.path.join(path, filename)):
                filename = rename_duplicate(filename)
            # Save file
            file.save(os.path.join(path, filename))
        # Return URL for uploaded picture
        return url_for('upload.view_file', id=path.rsplit('/', 1)[1],
                                           filename=filename,
                                           _external=True)
    else:
        return 'File format not allowed!'


# View route for viewing uploaded images
@bp.route('/<id>/<filename>')
def view_file(id, filename):
    path = url_for('upload.static', filename=id, _external=False)
    # Check if file exists
    if not os.path.exists(os.path.dirname(__file__) + os.path.join(path, filename)):
        return 'File not found'
    # Send file
    return send_from_directory(os.path.dirname(__file__) + path, filename)
