from datetime import datetime
from app import db
from sqlalchemy import text

# +---------------+--------------+------+-----+-------------------+-----------------------------+
# | Field         | Type         | Null | Key | Default           | Extra                       |
# +---------------+--------------+------+-----+-------------------+-----------------------------+
# | id            | int(11)      | NO   | PRI | NULL              | auto_increment              |
# | username      | varchar(64)  | YES  | UNI | NULL              |                             |
# | email         | varchar(120) | YES  | UNI | NULL              |                             |
# | password_hash | varchar(128) | YES  |     | NULL              |                             |
# | edit_date     | timestamp    | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
# | signup_date   | timestamp    | NO   |     | CURRENT_TIMESTAMP |                             |
# +---------------+--------------+------+-----+-------------------+-----------------------------+
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    edit_date = db.Column(db.TIMESTAMP, default=text('CURRENT_TIMESTAMP'), nullable=False)
    signup_date = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

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
