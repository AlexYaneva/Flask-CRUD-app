from threading import Thread
from flask import render_template
from flask_mail import Message
from app_package import app, mail

''' The send_mail() function here is made asynchronous i.e. when this function is called, the task of sending 
    the email is scheduled to happen in the background and the appliaction can continue running 
    at the same time as the email is being sent (rather than wait until the function completes before it can execute any ohter tasks). '''

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
	token = user.get_reset_password_token()
	send_email('[Blog] Reset your password',
				sender=app.config['ADMINS'][0],
				recipients=[user.email],
				text_body=render_template('email/reset_password.txt', user=user, token=token),  # the txt and html templates receive the user and token as arguments
				html_body= render_template('email/reset_password.html', user=user, token=token)) # so that a personalised message can be generated
