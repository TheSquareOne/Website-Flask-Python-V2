from flask import render_template, current_app
from app.main.email import send_email

# Send password reset link in user email address
def send_password_reset_email(user):
    # Get token for user password reset
    token = user.get_reset_password_token()
    # Send password reset link 
    send_email('Reset your password',
                sender=current_app.config['ADMINS'][0],
                recipients=[user.email],
                # In both email templates are url_for() used, which generates
                # by default relative URLs, but '_external=True' argument makes
                # it generate full URL like 'https://my-awesome/user/thomas'
                text_body=render_template('email/reset_password.txt',
                                            user=user, token=token),
                html_body=render_template('email/reset_password.html',
                                            user=user, token=token))
