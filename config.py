import os

# Configuration variables
class Config(object):
    # Secret key used by Flask-WTF extension to protect webforms from CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5up3r#s3cret_key!'
