from app import db
from app.models import Post, datetime
from flask import request, jsonify, make_response
from flask_login import current_user, login_user, login_required, logout_user
from app import app

# this returns both the user, and the post
# login_required checks if the cookie exists or not
@app.route('/get_all', methods=["GET"])
@login_required
def get_all():
    user_id = current_user.id 

    # this user's posts
    user_posts = Post.query.filter_by(user_id=user_id).all()

    # create json item for react-native
    json_response = {}

    for post in user_posts:
        json_response[post.id] = [
            post.body,
            datetime.strftime(post.timestamp, "%m/%d/%Y, %H:%M:%S")
        ]
    
    
    # so basically the client already has the user_id
    # react-native will store the username and password in App
    # class's this.state, and also user.json
    # therefore this endpoint just needs to return some json
    return jsonify(json_response)

@app.route('/add_post', methods=["GET"])
@login_required
def add_post():
    # code for adding a post
    # retrieve the cookie once again
    user_id = current_user.id

    # get request params
    post_body = request.args.get("body")

    # create row based on model
    new_post = Post(user_id=user_id, body=post_body)

    # add post
    db.session.add(new_post)
    db.session.commit()

    return 'post_added'

@app.route('/change_post', methods=["GET"])
@login_required
def change_post():
    # request params
    new_body = request.args.get('new_body')
    post_id = request.args.get('post_id')

    # change post
    changed_posted = Post.query.filter_by(id=post_id).update(dict(body=new_body))
    db.session.commit()

    return 'changed'


@app.route('/delete_post', methods=["POST"])
@login_required
def delete_post():
    # code for deleting a post
    delete_type = request.args.get('type')

    return 'deleted'
