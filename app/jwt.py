from flask_jwt import JWT
from app import app
from app.models import User

# functions for jwt
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password_hash(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

# create jwt
jwt = JWT(app, authenticate, identity)