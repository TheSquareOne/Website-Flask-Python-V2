from flask import Flask

# Initialize Flask
app = Flask(__name__)

from app import routes
