# server routes for this program
from app import db
from app.models import User, Post
from flask import request, jsonify, make_response, redirect
from flask_login import current_user, login_user, login_required, logout_user
from app import app

@app.route('/login', methods=['GET'])
def login():
    # get params
    username = request.args.get('username')
    password = request.args.get('password')

    # print(current_user)

    if current_user.is_authenticated:
        return 'user_auth'

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password_hash(password):
        return 'session_fail'

    # this is not needed but i stil added it(if statement)
    if user and user.check_password_hash(password):
        login_user(user, remember=False)

    return 'session_created'

@app.route('/register')
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')

    check_user = User.query.filter_by(username=username).first()

    # check if this user exists
    if not check_user: 
        new_user = User(username=username, email=email)
        new_user.hash_password(password)

        # add this to the database
        db.session.add(new_user)
        db.session.commit()
        return 'create_made'

    # if not send bad shit
    else:
        return 'create_fail'

@app.route('/logout')
def logout():
    logout_user()
    return 'logout_success'

@app.route('/')
def dicks():
    return 'dicks'
