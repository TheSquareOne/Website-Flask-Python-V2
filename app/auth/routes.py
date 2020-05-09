from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, SignUpForm, PasswordResetRequestForm, PasswordResetForm
from app.auth.email import send_password_reset_email
from app.models import User
from app.auth import bp
from app import db

# Login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is authenticated already, go to home page instead of login
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        # Query db with username and get first user object or None as a result
        user = User.query.filter_by(username=form.username.data).first()
        # Check if user was not found or password didnt match. If username or
        # password were wrong redirect back to login page.
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        # If username and password were correct mark user as logger in and
        # redirect user to home page.
        login_user(user, remember=form.remember_me.data)

        # If login URL doesn't have next argument or next URL isn't relative
        # redirect user to home page.
        # If login URL does have next argument,
        # redirect user to that page after login.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


# Logout user and redirect to home page
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Register user and redirect to login page
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # Prevent access from already logged in users
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # Validate signup form (check SignUpForm from forms.py)
    form = SignUpForm()
    if form.validate_on_submit():
        # If validation was successful, add user to db
        # and redirect to login page
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


# Password reset request
# User can request password reset link with email
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # Prevent already logged in users requesting password reset
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        # Check if user exist and return first User object
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for password reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset_request.html', form=form)


# When user presses password reset link, present password reset page.
# Token will expire in 10 minutes.
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Prevent already logged in users resetting password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # Verify token and on success get user object
    user = User.verify_reset_password_token(token)
    # If token is wrong redirect to home page
    if not user:
        return redirect(url_for('main.home'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        # If form is ok, set new password and redirect to login page
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset.html', form=form)
