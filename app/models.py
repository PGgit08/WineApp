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
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer)

    # store that this post belongs to
    my_store = db.Column(db.Integer)

class WineStore(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary key

    # google maps related info
    google_id = db.Column(db.String(180)) # google place id
    name = db.Column(db.String(200))


    # google maps id can change, so location info should also exist
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    address = db.Column(db.String(200))
