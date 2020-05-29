# Website-Flask-Python-V2

This is my second try of learning python and making my own web-server using flask.
I realized things i could have made better in my first project, but refactoring would have been too hard, so i decided to make whole new project to keep things clean and understandable for myself.

Things to improve: classes, file structure, virtual environment, comments and usage of libraries i found during my first researches.

#### Versions:
  - Python:   3.6.9
  - Flask:    1.1.2
  - Werkzeug: 1.0.1

#### Remember:
  - git pull
  - Stop supervisorctl
  - Change config.py alternate SECRET_KEY
  - Download requirements.txt
  - Migrate DB
  - Set environment variables
  - Check FLASK_APP
  - Start supervisor

#### Virtual environment variables
```
SECRET_KEY
MAIL_SERVER
MAIL_PORT
MAIL_USE_TLS
MAIL_USERNAME
MAIL_PASSWORD
UPLOAD_PATH
ALLOWED_FILES
CRYPTO_KEY
CRYPTO_IV
MAGIC_WORD
```


```
app/models.py           - Database models
app/template.html       - Base template

app/auth/               - Authentication routes
app/errors/             - Error handlers
app/main/               - Basic routes
app/upload/             - Upload features
app/templates/          - Templates
app/templates/auth/     - Authentication html pages
app/templates/email/    - Email support emails
app/templates/errors/   - Error pages
app/templates/main/     - Basic html pages
app/templates/upload/   - Upload page
migration/version/      - Database migration scripts
```

#### Migrations commands:
>'flask db migrate -m "This is comment"'     - Generate migrations script with comment.

>'flask db upgrade'                          - Make changes to db.

>'flask db downgrade'                        - Revert back last migration.


#### Problems:
During migrating edit_date and signup_date in user table, edit_date had to be done first in order to work.
1. op.add_column('user', sa.Column('edit_date', sa.TIMESTAMP(), nullable=False))
2. op.add_column('user', sa.Column('signup_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
In case of reverse order following error would be given:
>sqlalchemy.exc.OperationalError: (MySQLdb._exceptions.OperationalError) (1067, "Invalid default value for 'edit_date'")


#### References:
* [Flask Mega-Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [Great MySQL Timezone cheatsheet by Timo Huovinen](https://stackoverflow.com/questions/19023978/should-mysql-have-its-timezone-set-to-utc/19075291#19075291)
