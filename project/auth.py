# program for logging in, and sign up
from flask import Blueprint, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('uname')
    password = request.form.get('pword')

    user = User.query.filter_by(email=email).first()

    # check if this user exists
    if not user or not check_password_hash(password, user.password):
        return 'false_exist'
    
    return 'login_success'

# signup
@auth.route('/signup', methods=['POST'])
def signup():
    # get user info from client
    email = request.form.get('email')
    username = request.form.get('uname')
    password = request.form.get('pword')

    # get user
    user = User.query.filter_by(email=email).first() # this will return a user if they exist

    # check if this user exists
    if user:
        # return this to app if user exists
        return 'email_exists'

    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    
    db.session.add(new_user)
    db.session.commit()

    # return this to app if user exists
    return 'signup_success'
