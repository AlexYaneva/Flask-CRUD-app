from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #initialising the extension by creating an object instance
migrate = Migrate(app, db) #doing the same here as above

from app_package import routes, models