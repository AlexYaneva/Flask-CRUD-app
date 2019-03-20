#Home page route
from flask import render_template
from app_package import app

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Sasha'}
	posts = [
	{
	'author':{'username':'John'}, 
	'body': 'Beautiful day in Edinburgh!'
	},
	{
	'author':{'username':'Susan'},
	'body':'The Avengers movie was great!'}]

	return render_template('index.html', user=user, title='Home', posts=posts)



	
