from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app_package.models import User



class LoginForm(FlaskForm):
	'''user login form, which asks the user 
	for a username and psw and has the 'remember me'
	option'''
	username = StringField('Username', validators=[DataRequired()]) #the DataRequired() validator checks that the field is not submitted empty
	password = PasswordField('Password',validators=[DataRequired()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Sign in')




class RegistrationForm(FlaskForm):
	''' somewhat self-explanatory registration form
	following similar logic as the LoginForm '''
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')


	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')




class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request PasswordReset')



class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Request Password Reset')



class EditProfileForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired()])
	about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
	submit = SubmitField('Submit')

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')




class PostForm(FlaskForm):

	post = TextAreaField('Share your thoughts', validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField('Submit')

	