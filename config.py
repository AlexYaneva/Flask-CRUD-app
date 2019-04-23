import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():

	# This is an important config variable, useful to generate tokens or signatures. Flask uses is to protect agains CSRF.
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'what-a-time-to-be-alive' 

	# This config varible provides the location of the app's database
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') 

	# This signals the app everytime a change is made in the database, do not need it atm
	SQLALCHEMY_TRACK_MODIFICATIONS = False 

	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)

	# A boolean flag to enable encrypted connections
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None 
	
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['sasha.raecontacts@yahoo.co.uk']
	POSTS_PER_PAGE = 25
	