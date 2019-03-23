import os

class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'what-a-time-to-be-alive' #this is an important config variable, useful to generate tokens or signatures. Flask uses is to protect agains CSRF.