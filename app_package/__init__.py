from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #initialising the extension by creating an object instance
migrate = Migrate(app, db) #doing the same here as above
login = LoginManager(app)
login.login_view = 'login' #The 'login' value above is the function (or endpoint) name for the login view. 
#In other words, the name you would use in a url_for() call to get the URL.


#only enabling the logger if the app is running without debug mode:
if not app.debug:

	#checking if the email server exists for email handling:
	if app.config['MAIL_SERVER']:
		auth = None
		if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
			auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
		secure = None
		if app.config['MAIL_USE_TLS']:
			secure = ()
		mail_handler = SMTPHandler(
			mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
			fromaddr='no-reply@' + app.config['MAIL_SERVER'],
			toaddrs=app.config['ADMINS'], subject='Microblog Failure',
			credentials=auth, secure=secure)

		mail_handler.setLevel(logging.ERROR) #setting the level to report only errors and not warnings
		app.logger.addHandler(mail_handler)

	#setting up a log file:
	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/my_flask_app.log', maxBytes=10240, backupCount=10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)

	app.logger.setLevel(logging.INFO)
	app.logger.info('My flask app startup')

from app_package import routes, models, errors