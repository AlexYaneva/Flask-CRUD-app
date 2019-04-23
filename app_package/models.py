from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app_package import db
from flask_login import UserMixin
from app_package import db, login
from hashlib import md5
from time import time
import jwt

''' Defining models for the database tables, 
	the fields and the data types (varchar, integer etc.). 
	So far, there are 3 tables in the db - User, Post and followers 
'''


# This is an auxiliary table and has no data other than foreign keys, so no need for a model class for it:

followers = db.Table('followers', 
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))



class User(UserMixin, db.Model): 
 
	'''	db.Model is a base class for all models from flask-sqlalchemy.
    	The UserMixin class includes generic implementations that are appropriate 
    	for most user model classes( is_authenticated, is_active etc.)
    '''

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	# This field is defined only here for the one-to-many relationship (one user, multiple posts):
	posts = db.relationship('Post', backref='author', lazy='dynamic') 

	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)

	# Defining the followers table relationship; the .c. refers to the 'column' in the table:
	followed = db.relationship('User', secondary=followers, 
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
		)


	def __repr__(self):
		return f'<User {self.username}>'

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)



	def avatar(self, size):

		# Encoding the string as bytes and then passing it to the hash function
		digest = md5(self.email.lower().encode('utf-8')).hexdigest() 

		# The 'identicon' part is added to generate a default avatar for users who don't have one
		return f'https://gravatar.com/avatar/{digest}?d=identicon&s={size}' 




	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_posts(self):
		followed = Post.query.join(
			followers, followers.c.followed_id == Post.user_id).filter(
				followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id=self.id) # User's own posts
		return followed.union(own).order_by(Post.timestamp.desc())

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},
			current_app.config['SECRET_KEY'], algorithm = 'HS256').decode('utf-8')

	@staticmethod 
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)




class Post(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # The 'user' referenced here is the name of the table for the model

	def __repr__(self):
		return f'<Post {self.body}>'


# The flask-login extension expects that the application will configure a user loader function, 
# which can be called to load a user given the ID:
@login.user_loader
def load_user(id):
	return User.query.get(int(id))





