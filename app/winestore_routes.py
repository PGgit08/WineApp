from app import db, app
from app.models import WineStore
from flask import request, jsonify, make_response
from app.jwt_manager import *

# winestore api routes

"""
The following four routes are for the owners of a store.
These api routes allow them to see their stores posts on their profile page.
They also allow the owner to make new stores, change the stores name, and delete the store.
"""
@app.route('/stores/get')
@jwt_required
def get_users_stores():
    users_stores = WineStore.query.filter_by(owner=current_user().id).all()
    
    json_response = {}
    for store in users_stores:
        json_response[store.id] = {
            "name": store.name,
            "address": store.address,
            "location": store.location,
            "posts": store.posts
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

    store_name = request.args.get('store_name')
    address = request.args.get('address')
    owner = current_user().id
    location = request.args.get('location')
    

@app.route('/stores/change/<int:store_id>')
@jwt_required
def change_store(store_id):
    # change name of store
    pass

@app.route('/stores/delete/<int:store_id>')
@jwt_required
def delete_store(store_id):
    # delete the store
    pass

'''
This next api route is the most important one of WineApp.
A user can search for a store by it's address or id(which can be done by lookup or onholdpress)
and this route will return that stores data if it find the store.
'''
@app.route('/stores/deliver_data')
def deliver_store_data():
    pass
