
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app_package import app, db
from app_package.forms import LoginForm, RegistrationForm
from app_package.models import User
from werkzeug.urls import url_parse


''' All of these functions are called view functions - they are mapped to one or more URL routes.
    This is how Flask knows which locig to execute. '''

@app.route('/')

@app.route('/index')
@login_required #this means the /index page won't be displayed unless the user logs in first
def index():
	posts = [
	{
	'author':{'username':'John'}, 
	'body': 'Beautiful day in Edinburgh!'
	},
	{
	'author':{'username':'Susan'},
	'body':'The Avengers movie was great!'}]

	return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated: #current_user variable can be used at any time to obtain the user object that represents the request 
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next') #obtaining the value of 'next' i.e. which page the user wanted to see but was prompted to log in
		if not next_page or url_parse(next_page).netloc != '': #the parse and netloc are security checks
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

	
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now regisTURD!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)