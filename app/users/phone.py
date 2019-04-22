import os
from twilio.rest import Client
from flask import render_template, current_app
from flask import url_for



def send_verify_msg(user):
    token = user.get_reset_token()
    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_ACCOUNT_TOKEN']
    client = Client(account_sid, auth_token)
    client.messages.create(
        to= "+917014969260",
        from_ =current_app.config['TWILIO_ACCOUNT_NUMBER'],
        body=f'''To verify your profile please visit following link
{url_for('users.auth2verify', token=token, _external=True)}
If you did not make this request then simply ignore this message and no changes will be made.
'''
    )
   
