from app import db
from app.models import Post, datetime
from flask import request, jsonify, make_response
from flask_login import current_user, login_user, login_required, logout_user
from app import app, json

# this returns both the user, and the post
# login_required checks if the cookie exists or not
@app.route('/get', methods=["GET"])
@login_required
def get_all():
    user_id = current_user.id 

    # this user's posts
    user_posts = Post.query.filter_by(user_id=user_id).all()

    # 2 responses
    posts_response = {}
    user_response = {}

    for post in user_posts:
        posts_response[post.id] = [
            post.body,
            datetime.strftime(post.timestamp, "%m/%d/%Y, %H:%M:%S")
        ]
    
    # Password can't be unhashed, so just the username and the email are sent
    user_response['username'] = current_user.username
    user_response['email'] = current_user.email

    # create json item for react-native
    json_response = [user_response, posts_response]

    # so basically the client already has the user_id
    # react-native will store the username and password in App
    # class's this.state, and also user.json
    # therefore this endpoint just needs to return some json
    return jsonify(json_response)

@app.route('/add', methods=["GET"])
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

    return 'Added Post'

@app.route('/change', methods=["GET"])
@login_required
def change_post():
    # request params
    new_body = request.args.get('new_body')
    post_id = request.args.get('post_id')

    # change post
    changed_posted = Post.query.filter_by(id=post_id).first()
    
    # check if this post belongs to the current user
    # also check if the post even exists
    if changed_posted and changed_posted.user_id == current_user.id:
        # only one post has this unique id, so no .first() is needed
        Post.query.filter_by(id=post_id).update(dict(body=new_body))
        db.session.commit()
        return 'Changed Post'
    
    else:
        return 'Post Change Failed'


@app.route('/delete', methods=["GET"])
@login_required
def delete_post():
    # code for deleting a post
    delete_id = int(request.args.get('id'))
    
    delete_post = Post.query.filter_by(id=delete_id).first()

    if delete_post and delete_post.user_id == current_user.id:
        db.session.delete(delete_post)
        db.session.commit()
        return 'Post Deleted'

    else:
        return 'Post Delete Failed'
