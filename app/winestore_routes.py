from app import db, app
from app.models import WineStore, Post, User, datetime
from flask import request, jsonify, make_response
from app.jwt_manager import *
from sqlalchemy import or_

# for google api
from requests import get

# winestore api routes

'''
This api route creates a new store in the WineStores table.
This is called when the app sees a post being made to a store.
That doesn't have a WineApp id.
'''
@app.route('/stores/new')
@jwt_required
def new_store():
    api_response = {
        'error': 0,
        'msg': 'Api in progress'
    }

    google_id = request.args.get('g_id')
    
    # first check if this place even exists
    check_finds = WineStore.query.filter_by(google_id=google_id).first()
    if check_finds:
        api_response['error'] = 1
        api_response['msg'] = 'This place already exists'
        return jsonify(api_response)

    # request to google api to
    # get the place's info and save
    # the place based on the info

    store = details_request(google_id)
    if not store:
        # if nothing was found
        api_response['error'] = 1
        api_response['msg'] = 'Can\'t find this store incorrect g_id.'
        return api_response

    # make the new store
    new_winestore = WineStore(
        name=store['name'],
        google_id=store['place_id'],
        lat=store['lat'],
        lng=store['lng'],
        address=store['formatted_address'],
        vicinity=store['vicinity']
    )
    db.session.add(new_winestore)
    db.session.commit()
    api_response['msg'] = 'Store Made Successfully'

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
        store_response['vicinity'] = store.vicinity
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


# function for google details api
def details_request(place_id):
    details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'key': "AIzaSyDddVDWwqLQWv0lnZbEAD6Up9SF2EYH-6I",
        'place_id': place_id,
        'fields': "formatted_address,geometry,place_id,name,vicinity"
    } 

    response = get(details_url, params).json()
    if response['status'] != 'OK':
        return False
    
    store = response['result']

    # set lat and lng settings
    store['lat'] = float(store['geometry']['location']['lat'])
    store['lng'] = float(store['geometry']['location']['lng'])

    # delete unused geometry after lat,lng set
    del store['geometry']

    return store

# this function is for 
# dealing with big amounts of json
# like the google api
def json_handler(json):
    stores = json['results']

    for store in stores:
        name = store['name']
        place_id = store['place_id']

        lat = float(store['geometry']['location']['lat'])
        lng = float(store['geometry']['location']['lng'])

        # right here find a store with these params
        # set it's wineapp_id in the store dict
        check = or_(WineStore.google_id == place_id, 
                    WineStore.name == name,
                    WineStore.lat == lat,
                    WineStore.lng == lng)

        find = WineStore.query.filter(check)
        store['winestore_id'] = find.first().id 
        # here update the place
        # use the details_request to update this places info
        # and then based on returned dict
        # do update

        # change attribute name for update
        updated = details_request(store['place_id'])
        updated['address'] = updated.pop("formatted_address")
        updated['google_id'] = updated.pop("place_id")

        find.update(updated)
        db.session.commit()

    return stores

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
    lookup_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        "query": request.args.get("input"),
        "key": "AIzaSyDddVDWwqLQWv0lnZbEAD6Up9SF2EYH-6I",
        "type": "liquor_store"
    }

    response = get(lookup_url, params)

    # remake for debug
    response = response.json()

    # incase an api error
    if response['status'] != 'OK':
        api_response['error'] = 1
        api_response['msg'] = 'Google Api Request Error, Try Again and Check Params'
        return jsonify(api_response)

    # json handler find places
    finds = json_handler(response)

    api_response = {
        'error': 0,
        'msg': ''
    }

    api_response['finds'] = finds

    return jsonify(api_response)

@app.route('/stores/near_me')
def near_me():
    '''
    This api is here to show the user
    what stores are near them.
    '''

    api_response = {
        'error': 0,
        'msg': ''
    }


    # google request here
    near_me_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        "location": request.args.get('loc'),
        "radius": request.args.get('rad'),
        "type": "liquor_store",
        "key": 'AIzaSyDddVDWwqLQWv0lnZbEAD6Up9SF2EYH-6I'
    }

    response = get(near_me_url, params)
    
    # remake for debugging
    response = response.json()

    # incase an api error
    if response['status'] != 'OK':
        api_response['error'] = 1
        api_response['msg'] = 'Google Api Request Error, Try Again and Check Params'
        return jsonify(api_response)
    
    # find places
    finds = json_handler(response)

    # set api_response
    api_response['finds'] = finds

    # now parsing through this data, if this place exists in the database
    # add it's id to the server response
    return jsonify(api_response)
