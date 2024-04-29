#!/usr/bin/python3
"""
A view for the Amenity object that handles all default RESTful API actions
"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>/', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object by user_id
    - If the user_id is not linked to any User object,
    a 404 error will be raised
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)  # Raise a 404 Not Found error if user is not found
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a specific User object with id (user_id)"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)  # Raise a 404 Not Found error if user is not found
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a user object"""
    json_data = request.get_json()
    if not json_data:
        return make_response("Not a JSON", 400)
    if 'name' not in json_data:
        return make_response("Missing name", 400)

    new_user = User(**json_data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a specific User object with id (user_id)"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    user = storage.get(User, user_id)
    if not user:
        abort(404)  # Raise a 404 Not Found error if amenity is not found

    json_data = request.get_json()
    # Update State object with key-value pairs from JSON data
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
