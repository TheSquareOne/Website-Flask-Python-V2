from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

# Initialize Flask
app = Flask(__name__)
# Get configs
app.config.from_object(Config)
# Database object
db = SQLAlchemy(app)
# Initialize login manager
login = LoginManager(app)
login.login_view = 'login'
# Migration engine
migrate = Migrate(app, db)

from app import routes, models


# Shell context
# This is used with 'flask shell' for debugging and testing
from app.models import User, Post
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'admins': app.config['ADMINS']}


# Logging categories: DEBUG, INFO, WARNING, ERROR, CRITICAL

# If debug mode is on, dont use logging features
if not app.debug:
    # Email logging
    # If mail server is set, send email to authorized personels about occurred error
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
                    mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                    fromaddr = 'no-reply@' + app.config['MAIL_SERVER'],
                    toaddrs = app.config['ADMINS'],
                    subject = 'Server Error',
                    credentials = auth,
                    secure = secure)
        # Set logging category
        mail_handler.setLevel(logging.ERROR)
        # Attach to app.logger
        app.logger.addHandler(mail_handler)

    # File logging
    # If directory 'logs' doesn't exist, create it
    if not os.path.exists('logs'):
        os.mkdir('logs')
    # Set log file name, maximum file size to 10kB and save 10 last log files
    file_handler = RotatingFileHandler('logs/WebServer.log', maxBytes=10240, backupCount=10)
    # Format: timestamp logging level, message, source file and line number
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # Set logging category
    file_handler.setLevel(logging.INFO)
    # Attach to app.logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('WebServer startup')
