from flask import render_template
from flask_mail import Message
from app import mail, app
from threading import Thread

# Send email and clean thread after
def send_sync_email(app, msg):
    with app.app_context():
        mail.send(msg)


# Send email using one thread for app speed improvement
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    # Depending on the client, either text or HTML body will be seen
    msg.body = text_body
    msg.html = html_body
    # Use thread for sending email
    Thread(target=send_sync_email, args=(app, msg)).start()


# Send password reset link in user email address
def send_password_reset_email(user):
    # Get token for user password reset
    token = user.get_reset_password_token()
    # Send email to user containing password reset link
    send_email('Reset your password',
                sender=app.config['ADMINS'][0],
                recipients=[user.email],
                # In both email templates are url_for() used, which generates
                # by default relative URLs, but '_external=True' argument makes
                # it generate full URL like 'https://my-awesome/user/thomas'
                text_body=render_template('email/reset_password.txt',
                                            user=user, token=token),
                html_body=render_template('email/reset_password.html',
                                            user=user, token=token))
