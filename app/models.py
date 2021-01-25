from app import db, app
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

# structure of database, model
# changes that are not related to model, like creating a table, 
# are made in cmd, using flask migrate, or alembic

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer)

    # store that this post belongs to
    my_store = db.Column(db.Integer)

class WineStore(db.Model):
    owner = db.Column(db.Integer) # user id of the owner of this store

    id = db.Column(db.Integer, primary_key=True) # primary key
    name = db.Column(db.String)
    address = db.Column(db.String) # example: 111 jordan street
    location = db.Column(db.String) # example: lat 10, long 20


