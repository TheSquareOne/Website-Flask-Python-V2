from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize Flask
app = Flask(__name__)
# Get configs
app.config.from_object(Config)
# Database object
db = SQLAlchemy(app)
# Migration engine
migrate = Migrate(app, db)

from app import routes, models


# Shell context
from app.models import User, Post
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
