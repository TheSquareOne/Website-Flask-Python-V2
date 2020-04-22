# Website-Flask-Python-V2

This is my second try of learning python and making my own web-server using flask.
I realized things i could have made better in my first project, but refactoring would have been too hard, so i decided to make whole new project to keep things clean and understandable for myself.

Things to improve: classes, file structure, virtual environment, comments and usage of libraries i found during my first researches.

Versions:
Python:   3.6.9
Flask:    1.1.2
Werkzeug: 1.0.1


Python scripts:
app.py              Base app code
__init__.py         Initialize flask, and configurations
routes.py           URL routes
forms.py            Create secure web forms with Flask-WTF
config.py           Include application configurations


HTML pages:
index.html          Front side of web-server. Maybe add some kind of dashboard features and public stuff (blogs, projects) in future here.
template.html       Template for all pages. Includes basic head information, CSS and code block placements.
login.html          User login page.


migration/          Some files used for database migrations. Made by flask-migrate.
migration/version/  Contains scripts for database migration.


Migrations commands:
    'flask db migrate -m "This is comment"'     Generate migrations script with comment.
    'flask db upgrade'                          Make changes to db.
    'flask db downgrade'                        Revert back last migration.


Problems:
    During migrating edit_date and signup_date in user table, edit_date had to be done first in order to work.
    1. op.add_column('user', sa.Column('edit_date', sa.TIMESTAMP(), nullable=False))
    2. op.add_column('user', sa.Column('signup_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    In case of reverse order following error would be given:
    sqlalchemy.exc.OperationalError: (MySQLdb._exceptions.OperationalError) (1067, "Invalid default value for 'edit_date'")


References:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
