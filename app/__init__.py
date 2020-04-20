from flask import Flask
from config import Config

# Initialize Flask
app = Flask(__name__)
# Get configs
app.config.from_object(Config)

from app import routes
