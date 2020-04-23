import os

# Configuration variables
class Config(object):
    # Secret key used by Flask-WTF extension to protect webforms from CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5up3r#s3cret_key!'

    # Read database URL from file config.txt
    with open('config.txt', 'r') as f:
        # Read all lines, take index 0 and remove '/n' from end
        SQLALCHEMY_DATABASE_URI = f.readlines()[0][:-1]

    # Unused feature disabled
    SQLALCHEMY_TRACK_MODIFICATIONS = False
