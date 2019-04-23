import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import Config



# Creating an instance for every extension

db = SQLAlchemy() 
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login' # The 'login' value is the function name for the login view i.e. the name you would use in a url_for() call to get the URL.
login.login_message = 'Please log in to access this page.' 
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()




def create_app(config_class=Config):

	''' This function constructs the Flask app instance
	    instead of creating it as a global variable '''

	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)
	mail.init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)

	from app_package.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from app_package.auth import bp as auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')

	from app_package.main import bp as main_bp
	app.register_blueprint(main_bp)


    # Setting up the logger and enabling it only if the app is running without debug mode or testing:

	if not app.debug and not app.testing:

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

	return app


from app_package import models