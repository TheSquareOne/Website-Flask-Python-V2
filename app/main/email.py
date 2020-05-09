from app import mail
from flask import current_app
from flask_mail import Message
from threading import Thread

# Send email and clean thread after
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# Send email using one thread for app speed improvement
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    # Depending on the client, either text or HTML body will be seen
    msg.body = text_body
    msg.html = html_body
    # Use thread for sending email
    # Extract actual application instance from proxy object and
    # pass it as argument to thread
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
