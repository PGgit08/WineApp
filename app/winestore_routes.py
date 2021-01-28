from app import db, app
from app.models import WineStore, Post, User, datetime
from flask import request, jsonify, make_response
from app.jwt_manager import *

# class for turning dict into object for lookup
class DictToObject:
    def __init__(d):
        for key in d:
            setattr(self, key, d[key])

# winestore api routes

"""
The following four routes are for the owners of a store.
These api routes allow them to see their stores posts on their profile page.
They also allow the owner to make new stores, change the stores name, and delete the store.
"""
@app.route('/stores/get', methods=["GET"])
@jwt_required
def get_users_stores():
    users_stores = WineStore.query.filter_by(owner=current_user().id).all()

    json_response = {}
    for store in users_stores:
        json_response[store.id] = {
            "name": store.name,
            "address": store.address,
            "location": {
                "lat": store.lat,
                "lng": store.lng
            }
        }
    
    json_response['error'] = 0 
    json_response['msg'] = 'Store Info Gotten Successfully.'
    
    return jsonify(json_response)    

@app.route('/stores/new')
@jwt_required
def new_store():
    # add a new store
    # params here:
    # name
    # address
    # owner(id)

    owner = current_user().id

    store_name = request.args.get('name')
    address = request.args.get('address')

    lat = request.args.get('lat', type=int)
    lng = request.args.get('lng', type=int)

    # some later on processing of address and location here

    api_response = {
        "error": 0,
        "msg": ""
    }

    
    find_store = WineStore.query.filter_by(name=store_name, 
                                            address=address, 
                                            lat=lat,
                                            lng=lng).first()

    # first check if there is a store like this
    if find_store is None:
        new_store = WineStore(owner=current_user().id, name=store_name, address=address, lat=lat, lng=lat)
        db.session.add(new_store)
        db.session.commit()
        api_response["msg"] = "Store Made Successfully"

    else:
        api_response["error"] = 1
        api_response["msg"] = "This store already exists, try again."
    
    return jsonify(api_response)

@app.route('/stores/change/<int:store_id>')
@jwt_required
def change_store(store_id):
    # still not completly sure how to make this
    user_id = current_user().id

    api_response = {
        'error': 0,
        'msg': ''
    }

    return jsonify(api_response)
    

@app.route('/stores/delete/<int:store_id>')
@jwt_required
def delete_store(store_id):
    # delete the store
    user_id = current_user().id

    store_to_delete = WineStore.query.filter_by(id=store_id).first()

    api_response = {
        'error': 0,
        'msg': ''
    }
    if store_to_delete and store_to_delete.owner == user_id:
        db.session.delete(store_to_delete)
        db.session.commit()

        api_response['msg'] = 'Store Deleted Successfully'
    
    else: 
        api_response['msg'] = 'Error Deleting This Store'
        api_response['error'] = 1

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
        store_response['owner'] = User.query.filter_by(id=store.owner).first().username
        store_response['id'] = store.id
        store_response['name'] = store.name
        store_response['address'] = store.address
        store_response['location'] = {
            'lat': store.lat,
            'lng': store.lng
        }
        api_response['store'] = store_response
        api_response['msg'] = 'Found This Store Successfully'
    
    else: 
        api_response['msg'] = 'Can\t Find this Store'
        api_response['error'] = 1

    return jsonify(api_response)


'''
This next api route is the most important one of WineApp.
A user can search for a store by it's address or id(which can be done by lookup or onholdpress)
and this route will return that stores data if it find the store.
'''
@app.route('/stores/lookup')
def lookup():
    # the description of what this does is 
    # above

    api_response = {
        'error': 0,
        'msg': ''
    }

    '''
    search_string: a string that the user input into the search bar
                   this can be an address or a name
    '''
    # search_string here
    search_string = "%{}%".format(request.args.get('search_string'))
    
    # try to find stores based on this lookup
    name_finds = WineStore.query.filter(WineStore.name.like(search_string)).all()
    address_finds = WineStore.query.filter(WineStore.address.like(search_string)).all()

    packed_finds = []

    # search for name 
    for find in name_finds:
        packed_finds.append(
            {
                "id": find.id,
                "name": find.name,
                "address": find.address,
                "owner": User.query.filter_by(id=find.owner).first().username
            }
        )

    # search for address
    for find in address_finds:
        packed_finds.append(
            {
                "id": find.id,
                "name": find.name,
                "address": find.address,
                "owner": User.query.filter_by(id=find.owner).first().username
            }
        )
    
    # pack
    api_response['finds'] = packed_finds
    api_response['msg'] = 'Store Find Endpoint Success'

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

    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)

    lat_plus = 1 / 69
    lng_plus = 1 / 54.6

    print(WineStore.lat.between(lat, lat + 5))

    return jsonify(api_response)
