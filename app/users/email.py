from flask import render_template, current_app
from flask import url_for
from flask_mail import Message
from app import mail


def send_verify_email(user):
    token = user.get_reset_token()
    msg = Message('Email verification',
                  sender='quantamixsolutions@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To verify your profile please visit following link
{url_for('users.auth2verify', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
