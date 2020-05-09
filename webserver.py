from app import create_app, db
from app.models import User

app = create_app()

# Shell context
# This is used with 'flask shell' for debugging and testing
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
