'Routes for changing user table(adding users, and changing data)' 
'As well as routes for creating session cookies, and deleting them'

# server routes for this program
from app import db, app
from app.models import User, Post
from flask import request, jsonify, make_response
from app.jwt_manager import * 

@app.route('/')
def home():
    return 'Api for wineapp, route not found'

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    user = User.query.filter_by(username=username).first()

    # this means that the user exists
    if user and user.check_password_hash(password):
        api_response = {
            'jwt': create_jwt(user.id),
            'username': user.username,
            'email': user.email,
            'error': 0,
            'mes': 'Login Successful'
            }
        return jsonify(api_response)
    
    else:
        api_response = {
            'error': 1,
            'mes': 'Login failed, please try again'
        }
        return jsonify(api_response)

@app.route('/register')
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')

    if username is None or password is None or email is None:
        api_response = {
            'error': 1,
            'mes': 'Enter Register Credentials'
        }
        return jsonify(api_response)

    check_user = User.query.filter_by(username=username).first()

    # check if this user exists
    if not check_user: 
        new_user = User(username=username, email=email)
        new_user.hash_password(password)

        # add this to the database
        db.session.add(new_user)
        db.session.commit()
        
        api_response = {
            'error': 0,
            'mes': 'Register Successful'
        }
        return jsonify(api_response)

    # if not send bad stuff
    else:
        api_response = {
            'error': 1,
            'mes': 'This user exists, try again'
        }
        return jsonify(api_response)
