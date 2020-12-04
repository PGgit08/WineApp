# file for creating models for the database
# . in this import means this folder, it won't work when u just run this file
from . import db
from flask_login import UserMixin

# class User uses db.Model inheretance so that it has cool functions
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))
