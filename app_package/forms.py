from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	'''user login form, which asks the user 
	for a username and psw and has the 'remember me'
	option'''

	username = StringField('Username', validators=[DataRequired()]) #the datarequired validator checks that the field is not submitted empty
	password = PasswordField('Password',validators=[DataRequired()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Sign in')