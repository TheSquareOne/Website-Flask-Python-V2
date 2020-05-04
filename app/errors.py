from flask import render_template
from app import app, db

# Unknown page or file
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Database error
@app.errorhandler(500)
def internal_error(error):
    # Issue database rollback, to reset session in clean state
    db.session.rollback()
    return render_template('500.html'), 500
