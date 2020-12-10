from app import db
from app.models import Post
from flask import request, jsonify, make_response
from flask_login import current_user, login_user, login_required, logout_user
from app import app

# this returns both the user, and the post
@app.route('/get_all', methods=["GET"])
def get_all():
    user_id = current_user.id 

    # this user's posts
    user_posts = Post.query.filter_by(user_id=user_id).all()
    
    # create json item for react-native
    json_response = {}

    for post in user_posts:
        json_response[post.id] = {
            post.body,
            post.timestamp
        }
    
    return jsonify(json_response)

@app.route('/add_post', methods=["GET"])
def add_post():
    # code for adding a post
    user_id = current_user.id
    return 'got user'

@app.route('/change_post', methods=["POST"])
def change_post():
    # code for changing a post
    pass

@app.route('/delete_post', methods=["POST"])
def delete_post():
    # code for deleting a post
    pass 
