from flask import request, jsonify
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

# static method decorator means that this isn't realated to the class(bruh)
# at all, and it is just doing it's own thing
def current_user():
    auth_header = request.headers.get('Authorization')

    auth_token = auth_header.split(" ")[1]
    payload = jwt.decode(auth_token, app.secret_key)
    return User.query.get(payload['sub'])

# create decorator for function
# also check if the token is valid
def jwt_required(func):
    def wrapper():
        error_json = {
            'error': 1,
            'mes': 'Please send token(be sure it\'s valid) for this endpoint'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(error_json)
        
        if auth_header:
            # now check if the token is valid
            try:
                jwt.decode(auth_header.split(" ")[1], app.secret_key)
            
            except jwt.InvalidTokenError:
                return jsonify(error_json)
            
            # if token is valid the func will be ran
            func()

    # if we dont do this, then there will be multiple 
    # wrapper() funcs, so each wrapper func 
    # is being re-named to the decorated funcs name
    wrapper.__name__ = func.__name__
    return wrapper
