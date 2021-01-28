from app import db, app
from app.models import WineStore, Post, User, datetime
from flask import request, jsonify, make_response
from app.jwt_manager import *

# for google api
from requests import get

# winestore api routes

'''
This api route creates a new store in the WineStores table.
This is called when the app sees a post being made to a store.
That doesn't have a WineApp id.
'''
@app.route('/stores/new')
def new_store():
    api_response = {
        'error': 0,
        'msg': 'Api in progress'
    }

    return jsonify(api_response)

'''
This api route is used after the lookup.
Once the user selects their store after the lookup.
WineApp makes a call to this route with the id of the store.
This route returns the stores info(including posts).
'''
@app.route('/stores/get_by_id/<int:store_id>')
def get_by_id(store_id):
    api_response = {
        'error': 0,
        'msg': ''
    }

    store = WineStore.query.filter_by(id=store_id).first()

    if store:
        posts = Post.query.filter_by(my_store=store_id).all()
        packed_posts = []
        # make this json readable
        for post in posts:
            packed_posts.append({
                "id": post.id,
                "owner": User.query.filter_by(id=post.user_id).first().username,
                "body": post.body,
                "date_made": datetime.strftime(post.timestamp, "%m/%d/%Y, %H:%M:%S")
            })

        store_response = {
            'posts': packed_posts
        }

        # fill up store response
        store_response['id'] = store.id
        store_response['name'] = store.name
        store_response['address'] = store.address
        store_response['location'] = {
            'lat': store.lat,
            'lng': store.lng
        }
        store_response['g_id'] = store.google_id

        api_response['store'] = store_response
        api_response['msg'] = 'Found This Store Successfully'
    
    else: 
        api_response['msg'] = 'Can\t Find this Store'
        api_response['error'] = 1

    return jsonify(api_response)


'''
This next api route is the most important one of WineApp.
A user can search for a store by it's address, name, etc.(which can be done by lookup or onholdpress)
and this route will return that stores data if it find the store.
'''
@app.route('/stores/lookup')
def lookup():
    # the description of what this does is 
    # above

    # google request here
    lookup_url = 'https://'
    params = {

    }

    response = get(lookup_url, params).json()

    api_response = {
        'error': 0,
        'msg': ''
    }

    return jsonify(api_response)

@app.route('/stores/near_me')
def near_me():
    '''
    This api is here to show the user
    what stores are near them.
    '''

    # google request here
    near-me_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        "location": request.args.get('loc'),
        "radius": request.args.get('rad'),
        "type": "liquor_store",
        "key": 'AIzaSyDddVDWwqLQWv0lnZbEAD6Up9SF2EYH-6I'
    }

    response = get(near-me_url, params).json()

    api_response = {
        'error': 0,
        'msg': ''
    }

    return jsonify(api_response)
