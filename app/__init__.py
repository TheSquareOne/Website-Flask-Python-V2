from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

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
from app.models import User, Post
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
