from flask import request
from app.models import User
import jwt
from app import app

# create jwt using current users id
# this will be used in log in
def create_jwt(user_id):
    try:
        payload = {
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.secret_key,
            algorithm='HS256'
        )

    except Exception as e:
        return e

# static method decorator means that this isn't realated to the class
# at all, and it is just doing it's own thing
def current_user():
    auth_header = request.headers.get('Authorization')

    # check if the header even exists
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(auth_token, app.secret_key)
            return User.query.get(payload['sub'])
        
        except jwt.InvalidTokenError:
            return False
    
    else:
        return False