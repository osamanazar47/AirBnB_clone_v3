#!/usr/bin/python3
"""
A view for the State object that handles all default RESTful API actions
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request, make_response

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by state_id
    - If the state_id is not linked to any State object, a 404 error will be raised
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)  # Raise a 404 Not Found error if state is not found
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a specific State object with id (state_id)"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)  # Raise a 404 Not Found error if state is not found
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    json_data = request.get_json()
    if not json_data:
        return make_response("Not a JSON", 400)
    if 'name' not in json_data:
        return make_response("Missing name", 400)

    new_state = State(**json_data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a specific State object with id (state_id)"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)  # Raise a 404 Not Found error if state is not found

    json_data = request.get_json()
    if not json_data:
        return make_response("Not a JSON", 400)

    # Update State object with key-value pairs from JSON data
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)