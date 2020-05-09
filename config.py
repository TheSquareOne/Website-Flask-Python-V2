import os
from dotenv import load_dotenv

# Create .env path, which should be in root directory.
basedir = os.path.abspath(os.path.dirname(__file__))
# Load environment variables from .env for config.
load_dotenv(os.path.join(basedir, '.env'))

# Configuration variables
class Config(object):
    # Secret key used by Flask-WTF extension to protect webforms from CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5up3r#s3cret_key_Yu0_w1Ll-N3v3R#GUE55!!'

    # Read database URL from file config.txt
    with open('config.txt', 'r') as f:
        # Read all lines, take index 0 and remove '/n' from end
        SQLALCHEMY_DATABASE_URI = f.readlines()[0][:-1]

    # Disable unused feature
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Email logging configurations
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # Enable encrypted connection
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # Read authorized personel emails from file
    with open('emails.txt', 'r') as f:
        ADMINS = []
        emails = f.readlines()
        for e in emails:
            ADMINS.append(e[:-1])
