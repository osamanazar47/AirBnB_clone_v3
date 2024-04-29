#!/usr/bin/python3
"""
A view for the Amenity object that handles all default RESTful API actions
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves an Amenity object by amenity_id
    - If the amenity_id is not linked to any Amenity object,
    a 404 error will be raised
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)  # Raise a 404 Not Found error if amenity is not found
    return jsonify(amenity.to_dict())


d = 'DELETE'


@app_views.route('/amenities/<amenity_id>', methods=[d],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a specific Amenity object with id (amenity_id)"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)  # Raise a 404 Not Found error if amenity is not found
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    json_data = request.get_json()
    if not json_data:
        return make_response("Not a JSON", 400)
    if 'name' not in json_data:
        return make_response("Missing name", 400)

    new_amenity = Amenity(**json_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a specific Amenity object with id (amenity_id)"""
    amenity = storage.get(State, amenity_id)
    if  not amenity:
        abort(404)  # Raise a 404 Not Found error if amenity is not found

    if not request.get_json():
        abort(400, description="Not a JSON")

    json_data = request.get_json()
    # Update State object with key-value pairs from JSON data
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
