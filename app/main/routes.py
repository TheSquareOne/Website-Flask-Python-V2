from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
from app.main.forms import EditProfileForm
from app.models import User
from app.main import bp
from app import db

# Index / Root page
@bp.route('/')
def home():
    return render_template('main/index.html')


# Users profile page, where <username> is username for known user
@bp.route('/profile/<username>')
@login_required
def profile(username):
    # Check if user exist or return error page
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/profile.html', user=user)


# Edit user profile
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
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
