'Routes for changing user table(adding users, and changing data)' 
'As well as routes for creating session cookies, and deleting them'

# server routes for this program
from app import db, app
from app.models import User, Post
from flask import request, jsonify, make_response
from app.jwt import *

@app.route('/login')
def test():
    username = request.args.get('username')
    password = request.args.get('password')

    if current_user():
        return 'Logged In Already'

    user = User.query.filter_by(username=username).first()

    # this means that the user exists
    if user and user.check_password_hash(password):
        return create_jwt(user.id)
    
    else:
        return 'Error Logging In, Please Check Credentials'

@app.route('/register')
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')

    if username is None:
        return 'Please Enter Register Credentials'

    check_user = User.query.filter_by(username=username).first()

    # check if this user exists
    if not check_user: 
        new_user = User(username=username, email=email)
        new_user.hash_password(password)

        # add this to the database
        db.session.add(new_user)
        db.session.commit()
        return 'Register Successful'

    # if not send bad stuff
    else:
        return 'Please Try Again'
