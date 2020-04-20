from app import app

# Index / Root page
@app.route('/')
def index():
    return 'Hello World!'
