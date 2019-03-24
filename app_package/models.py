from datetime import datetime
from app_package import db

#Here i am basically defining my models for my database tables, the data fields and the data types (varchar, integer etc.)

class User(db.Model): #db.Model is a base class for all models from flask-sqlalchemy
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic') #only need to define this field here for the one-to-many relationship (one user, multiple posts)

	def __repr__(self):
		return f'<User {self.username}>'

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #the 'user' part here is the name of the table for the model

	def __repr__(self):
		return f'<Post {self.body}>'
