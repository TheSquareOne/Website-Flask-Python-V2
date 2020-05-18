from flask import current_app
from datetime import datetime
from app import db, login
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from time import time
import secrets

# +---------------+--------------+------+-----+-------------------+-----------------------------+
# | Field         | Type         | Null | Key | Default           | Extra                       |
# +---------------+--------------+------+-----+-------------------+-----------------------------+
# | id            | int(11)      | NO   | PRI | NULL              | auto_increment              |
# | username      | varchar(64)  | YES  | UNI | NULL              |                             |
# | email         | varchar(120) | YES  | UNI | NULL              |                             |
# | password_hash | varchar(128) | YES  |     | NULL              |                             |
# | edit_date     | timestamp    | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
# | signup_date   | timestamp    | NO   |     | CURRENT_TIMESTAMP |                             |
# | about_me      | varchar(200) | YES  |     | NULL              |                             |
# | api_token     | varchar(64)  | YES  | UNI | NULL              |                             |
# +---------------+--------------+------+-----+-------------------+-----------------------------+
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    edit_date = db.Column(db.TIMESTAMP, nullable=False,
                            default=text('CURRENT_TIMESTAMP'))
    signup_date = db.Column(db.TIMESTAMP, nullable=False,
                            server_default=text('CURRENT_TIMESTAMP'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(200))
    api_token = db.Column(db.String(64), index=True, unique=True)

    # Set password for user
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check if password is correct. Return True or False
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Generate JWT token for password reset, token expires in 10min
    def get_reset_password_token(self, expires_in=600):
        # jwt.encode returns bytes which is converted to 'utf-8' string
        return jwt.encode(
                        {'reset_password': self.id, 'exp': time() + expires_in},
                        current_app.config['SECRET_KEY'],
                        algorithm='HS256').decode('utf-8')

    # Generate API token for user
    def gen_api_token(self):
        api_token = secrets.token_urlsafe()
        if User.query.filter_by(api_token=api_token).first() is None:
            self.api_token = api_token


    # Static methods can be invoked directly from the class.
    # Try verifying given token. If it's ok return user ID, else return None
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}'.format(self.username)


# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | id        | int(11)      | NO   | PRI | NULL    | auto_increment |
# | content   | varchar(140) | YES  |     | NULL    |                |
# | timestamp | datetime     | YES  | MUL | NULL    |                |
# | user_id   | int(11)      | YES  | MUL | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}'.format(self.content)


# User loader. This will load user from database based on ID
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
