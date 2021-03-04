from app import db, app
from app.models import Post, datetime, WineStore
from flask import request, jsonify
from app.jwt_manager import *

from json import dumps


# jwt_requrired is a func for 
# checking if the jwt is in the header
@app.route('/posts/get', methods=["GET"])
@jwt_required
def get_all():
    # get current user
    user_id = current_user().id 

    # this user's posts
    user_posts = Post.query.filter_by(user_id=user_id).all()

    # response
    post_responses = []

    # api response
    api_json = {}

    for post in user_posts:
        {
            "owner": post.user_id,
            "my_store": post.my_store,
            "id": post.id,
            "body": post.body,
            "time": datetime.strftime(post.timestamp, "%m/%d/%Y, %H:%M:%S")
        }
    
    # status
    api_json['error'] = 0
    api_json['msg'] = 'Info Gotten Successfully'

    # create posts
    api_json['posts'] = post_responses

    # DUMP
    json = dumps(api_json)
    return json

@app.route('/posts/add', methods=["GET"])
@jwt_required
def add_post():
    # code for adding a post
    # retrieve the cookie once again
    user_id = current_user().id

    # get request params
    post_body = request.args.get("body")
    place_id = request.args.get("place_id", type=int)

    # check for the store
    check_store = WineStore.query.filter_by(id=place_id).first()

    # if this store exists

    if check_store:
        # create the post
        new_post = Post(body=post_body, my_store=place_id, user_id=user_id)

        # add post
        db.session.add(new_post)
        db.session.commit()

        api_json = {
            "error": 0,
            "mes": 'Post Added' 
        }

    if not check_store:
        api_json = {
            "error": 1,
            "mes": "No Parent Store For This Post, Make Store First"
        }

    return jsonify(api_json)

@app.route('/posts/change/<int:post_id>', methods=["GET"])
@jwt_required
def change_post(post_id):
    # request params
    new_body = request.args.get('new_body')

    # change post
    wanted_post = Post.query.filter_by(id=post_id).first()
    
    api_json = {}

    # check if this post belongs to the current user
    # also check if the post even exists
    if wanted_post and wanted_post.user_id == current_user().id:
        # only one post has this unique id, so no .first() is needed
        Post.query.filter_by(id=post_id).update(dict(body=new_body))
        db.session.commit()

        api_json = {
            'error': 0,
            'mes': 'Post Changed'
        }    

    else:
        api_json = {
            'error': 1,
            'mes': 'Post change failed, this post does not belong to you'
        }
    
    return jsonify(api_json)


@app.route('/posts/delete/<int:post_id>', methods=["GET"])
@jwt_required
def delete_post(post_id):
    # code for deleting a post
    delete_id = post_id
    
    delete_post = Post.query.filter_by(id=delete_id).first()

    api_json = {}

    if delete_post and delete_post.user_id == current_user().id:
        db.session.delete(delete_post)
        db.session.commit()
        
        api_json = {
            'error': 0,
            'mes': 'Post Deleted'
        }    

    else:
        api_json = {
            'error': 1,
            'mes': 'Post delete failed, this post does not belong to you'
        }    
    
    return jsonify(api_json)
