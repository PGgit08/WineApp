'Routes for changing user table(adding users, and changing data)' 
'As well as routes for creating session cookies, and deleting them'

# server routes for this program
from app import db
from app.models import User, Post
from flask import request, jsonify, make_response
from app import app
from jwt import identity

@app.route('/login', methods=['GET'])
def login():
    # get params
    username = request.args.get('username')
    password = request.args.get('password')

    # current_user = user loaded from user_id in session cookie

    if current_user.is_authenticated:
        return 'Logged In Already'

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password_hash(password):
        return 'Can\'t Log In, Make Sure Your Username and Password Is Correct'

    # this is not needed but i stil added it(if statement)
    if user and user.check_password_hash(password):
        # send cookie to client with user_id
        # remember is true, because we do not want
        # react-native app to lose cookie
        login_user(user, remember=True)
        'Log In Successful'

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
        return 'Register Successful'

    # if not send bad stuff
    else:
        return 'Please Try Again'

@app.route('/logout')
def logout():
    # delete cookies on client with user_id
    logout_user()
    return 'Logged Out'

