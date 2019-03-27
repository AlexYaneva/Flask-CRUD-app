from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app_package import db
from flask_login import UserMixin
from app_package import login

#Here, i am basically defining my models for my database tables, the data fields and the data types (varchar, integer etc.)

class User(UserMixin, db.Model): #db.Model is a base class for all models from flask-sqlalchemy
    #UserMixin class includes generic implementations that are appropriate for most user model classes.
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic') #only need to define this field here for the one-to-many relationship (one user, multiple posts)

	def __repr__(self):
		return f'<User {self.username}>'

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #the 'user' part here is the name of the table for the model

	def __repr__(self):
		return f'<Post {self.body}>'


# The flask-login extension expects that the application will configure a user loader function, 
# that can be called to load a user given the ID:
@login.user_loader
def load_user(id):
	return User.query.get(int(id))