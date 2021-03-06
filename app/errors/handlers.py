from flask import render_template
from app import db
from app.errors import bp

# Unknown page or file
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# Database error
@bp.app_errorhandler(500)
def internal_error(error):
    # Issue database rollback, to reset session in clean state
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Too large file
@bp.app_errorhandler(413)
def request_entity_too_large(error):
    return render_template('errors/413.html'), 413

# Method not allowed
@bp.app_errorhandler(405)
def method_not_allowed(error):
    return render_template('errors/405.html'), 405
