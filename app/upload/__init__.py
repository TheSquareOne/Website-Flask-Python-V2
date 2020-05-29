from flask import Blueprint
import os

# Blueprint for upload feature
# Set static_folder for uploads where images can be retrievet
# Set static_url_path for URL to serve static files from
bp = Blueprint('upload', __name__,
               static_folder='uploads',
               static_url_path='/uploads',
              )

# Check if folder for uploads exists, if not create it
basedir = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(basedir):
    try:
        print(os.path.dirname(__file__))
        os.mkdir(basedir)
        print("Created folder for uploads at: " + basedir)
    except Exception:
        print("Couldn't create folder for uploads")


from app.upload import routes
