#!/usr/bin/python3
"""
A view for the city object that handles all default RESTful API actions
"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places_in_city(city_id):
    """Retrieves the list of all places objects in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(place_id):
    """
    Retrieves a Place object by place_id
    - If the place_id is not linked to any Place object,
    a 404 error will be raised
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)  # Raise a 404 Not Found error if state is not found
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(place_id):
    """Deletes a specific Place object with id (place_id)"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)  # Raise a 404 Not Found error if state is not found
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place_in_city(city_id):
    """Create a new Place object and link it to a City object
    using city_id key"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return make_response("Not a JSON", 400)
    if 'user_id' not in json_data:
        return make_response("Missing user_id", 400)
    user = storage.get(User, json_data.user_id)
    if user is None:
        abort(404)
    if 'name' not in json_data:
        return make_response("Missing name", 400)
    new_place = Place(**json_data)
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a specific Place object with id (place_id)"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)  # Raise a 404 Not Found error if state is not found

    json_data = request.get_json()
    if not json_data:
        return make_response("Not a JSON", 400)

    # Update State object with key-value pairs from JSON data
    for key, value in json_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
