from app import db

# structure of database, model
# changes that are not related to model, like creating a table, 
# are made in cmd, using flask migrate, or alembic
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
