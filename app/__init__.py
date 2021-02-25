from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

import os

# base dir for creation uri for database
basedir = os.path.abspath(os.path.dirname(__file__))

# create uri
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

# create app
app = Flask(__name__)

# cors for app
cors = CORS(app)

# set config for app 
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['PORT'] = 80

# secret key for cookies which decodes cookies
app.secret_key = '01jokjd01pj;kdj;aouskd'

# error handler
@app.errorhandler(500)
def internal_error(error):
        return jsonify({
                'error': 1,
                'msg': 'Server Error(500), Try Again Later'
        }), 200

@app.errorhandler(404)
def page_not_found(error):
        return jsonify({
                'error': 1,
                'msg': 'Server Error(404), Try Again Later'
        }), 200

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, user_routes, post_routes, winestore_routes
