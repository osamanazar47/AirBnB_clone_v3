#!/usr/bin/python3
"""
A view for the city object that handles all default RESTful API actions
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """Retrieves the list of all City objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object by city_id
    - If the city_id is not linked to any City object,
    a 404 error will be raised
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)  # Raise a 404 Not Found error if state is not found
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a specific City object with id (city_id)"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)  # Raise a 404 Not Found error if state is not found
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city_in_state(state_id):
    """Create a new City object and link it to a State object
    using state_id key"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return make_response("Not a JSON", 400)
    if 'name' not in json_data:
        return make_response("Missing name", 400)

    new_city = City(**json_data)
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a specific City object with id (city_id)"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)  # Raise a 404 Not Found error if state is not found

    json_data = request.get_json()
    if not json_data:
        return make_response("Not a JSON", 400)

    # Update State object with key-value pairs from JSON data
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
