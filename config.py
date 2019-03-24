import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'what-a-time-to-be-alive' #this is an important config variable, useful to generate tokens or signatures. Flask uses is to protect agains CSRF.
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') #this config varible provides the location of the app's database
	SQLALCHEMY_TRACK_MODIFICATIONS = False #this signals the app everytime a change is made in the database, do not need it atm