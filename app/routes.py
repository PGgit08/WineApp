# server routes for this program
from app import db
from app.models import User, Post
from flask import request, session, jsonify
from app import app


@app.route('/')
def home():
    return 'API FOR WINEAPP, DOWLOAD AT PLAYSTORE, API COPYRIGHT PETER GUTKOVICH'

@app.route('/api/create_session', methods=['POST'])
def create_session():
    session['username'] = request.form['username']
    session['password'] = request.form['password']
    session['email'] = request.form['email']

    find_user = User.query.filter_by(username=session['username']).first()
    
    # find the user and get their id and put it into session file
    if find_user:
        session['user_id'] = find_user.id
        return 'session_created'

    if find_user is None:
        return 'session_fail'

@app.route('/api/register', methods=['POST'])
def register():
    # get info from POST request
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # check if this user already exists(i know it is checked in the flow but JUST DO IT)
    check_user = User.query.filter_by(username=username).first()
    if check_user:
        # tell app that user exists
        return 'user_exist'
    
    if check_user is None:
        # create the user
        new_user = User(username=username, email=email)
        new_user.hash_password(password)
        
        # add user
        db.session.add(new_user)
        db.session.commit()
        
        # tell app that it was a success
        return 'user_made'


@app.route('/api/get_user')
def get_user():
    username = session.get('username')
    password = session.get('password')
    email = session.get('email')
    user_id = session.get('user_id')

    posted = Post.query.filter_by(user_id=user_id).all()
    user = User.query.filter_by(username=username).first()

    # packed_user = [user.email, user.password, user.username]
    # packed_data = [posted, packed_user]

    print(username)
    return 'y'
