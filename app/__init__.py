from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import json

import os

# base dir for creation uri for database
basedir = os.path.abspath(os.path.dirname(__file__))

# create uri
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

# create app
app = Flask(__name__)

# set config for app 
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# secret key for cookies which decodes cookies
app.secret_key = '01jokjd01pj;kdj;aouskd'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import models, user_routes, post_routes
