from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import LoginForm, SignUpForm, EditProfileForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

# Index / Root page
@app.route('/')
def home():
    return render_template('index.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is authenticated already, go to home page instead of login
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        # Query db with username and get first user object or None as a result
        user = User.query.filter_by(username=form.username.data).first()
        # Check if user was not found or password didnt match. If username or
        # password were wrong redirect back to login page.
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # If username and password were correct mark user as logger in and
        # redirect user to home page.
        login_user(user, remember=form.remember_me.data)

        # If login URL doesn't have next argument or next URL isn't relative
        # redirect user to home page.
        # If login URL does have next argument redirect user to that page after login.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', form=form)


# Logout user and redirect to home page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Register user and redirect to login page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Prevent access from already logged in users
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Validate signup form (check SignUpForm from forms.py)
    form = SignUpForm()
    if form.validate_on_submit():
        # If validation was successful add user to db and redirect to login page
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


# Users profile page, where <username> is username for known user
@app.route('/profile/<username>')
@login_required
def profile(username):
    # Check if user exist or return error page
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)


# Edit user profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changes have been saved!')
        return redirect(url_for('edit_profile'))
    # When form is requested, fill in current profile info to the fields
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('profile_edit.html', form=form)
