from flask import render_template, current_app
from app_package.email import send_email

def send_password_reset_email(user):
	token = user.get_reset_password_token()
	send_email('[Blog] Reset your password',
				sender=current_app.config['ADMINS'][0],
				recipients=[user.email],
				text_body=render_template('email/reset_password.txt', user=user, token=token),  # the txt and html templates receive the user and token as arguments
				html_body= render_template('email/reset_password.html', user=user, token=token)) # so that a personalised message can be generated