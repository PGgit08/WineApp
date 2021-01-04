from app import db, app
from app.models import Post, datetime
from flask import request, jsonify, make_response
from app.jwt_manager import *

from json import dumps

# jwt_requrired is a func for 
# checking if the jwt is in the header
@app.route('/get', methods=["GET"])
@jwt_required
def get_all():
    # get current user
    user_id = current_user().id 

    # this user's posts
    user_posts = Post.query.filter_by(user_id=user_id).all()

    # response
    posts_response = {}

    for post in user_posts:
        posts_response[post.id] = {
            "body": post.body,
            "time": datetime.strftime(post.timestamp, "%m/%d/%Y, %H:%M:%S")
        }
    
    posts_response['error'] = 0
    posts_response['msg'] = 'Info Gotten Successfully'

    print(posts_response)

    json = dumps(posts_response)
    return json

@app.route('/add', methods=["GET"])
@jwt_required
def add_post():
    # code for adding a post
    # retrieve the cookie once again
    user_id = current_user().id

    # get request params
    post_body = request.args.get("body")

    # create row based on model
    new_post = Post(user_id=user_id, body=post_body)

    # add post
    db.session.add(new_post)
    db.session.commit()

    api_json = {
        "error": 0,
        "mes": 'Post Added' 
    }

    return jsonify(api_json)

@app.route('/change', methods=["GET"])
@jwt_required
def change_post():
    # request params
    new_body = request.args.get('new_body')
    post_id = request.args.get('post_id')

    # change post
    changed_posted = Post.query.filter_by(id=post_id).first()
    
    # check if this post belongs to the current user
    # also check if the post even exists
    if changed_posted and changed_posted.user_id == current_user().id:
        # only one post has this unique id, so no .first() is needed
        Post.query.filter_by(id=post_id).update(dict(body=new_body))
        db.session.commit()

        api_json = {
            'error': 0,
            'mes': 'Post Changed'
        }    
        return jsonify(api_json)

    else:
        api_json = {
            'error': 1,
            'mes': 'Post change failed, this post does not belong to you'
        }


@app.route('/delete', methods=["GET"])
@jwt_required
def delete_post():
    # code for deleting a post
    delete_id = int(request.args.get('id'))
    
    delete_post = Post.query.filter_by(id=delete_id).first()

    if delete_post and delete_post.user_id == current_user().id:
        db.session.delete(delete_post)
        db.session.commit()
        
        api_json = {
            'error': 0,
            'mes': 'Post Deleted'
        }    
        return jsonify(api_json)

    else:
        api_json = {
            'error': 1,
            'mes': 'Post delete failed, this post does not belong to you'
        }    
        return jsonify(api_json)
