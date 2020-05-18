from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
from app.main.forms import EditProfileForm
from app.models import User
from app.main import bp
from app import db
import urllib.parse, hashlib

# Home / Index / Root route
@bp.route('/')
def home():
    return render_template('main/index.html')


# User profile route, where <username> is username for known user
@bp.route('/profile/<username>')
@login_required
def profile(username):
    # Check if user exist or return error page
    user = User.query.filter_by(username=username).first_or_404()
    # Gravatar size
    gravatar_size = 200
    # Gravatar URL
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(user.email.lower().encode('utf-8')).hexdigest() + "?"
    # Encode parameters at the end of URL. Use identicon as default avatars
    gravatar_url += urllib.parse.urlencode({'d':'identicon', 's':str(gravatar_size)})
    return render_template('main/profile.html',
                            user=user, gravatar_url=gravatar_url)


# Edit profile route
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    # Validate username change
    if form.validate_on_submit():
        # If form is ok, commit
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changes have been saved!')
        return redirect(url_for('main.edit_profile'))
    # When form is requested, fill in current profile info to the fields
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('main/profile_edit.html', form=form)


# Generate new API token
@bp.route('/get_api_token')
@login_required
def get_api_token():
    # Generate new API token
    current_user.gen_api_token()
    db.session.commit()
    # Redirect back to profile
    return redirect(url_for('main.profile', username=current_user.username))
