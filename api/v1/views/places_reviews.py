#!/usr/bin/python3
"""
A view for the Place object that handles all default RESTful API actions
"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_of_place(place_id):
    """Retrieves the list of all reviews objects in a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a review object by review_id
    - If the review_id is not linked to any Review object,
    a 404 error will be raised
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)  # Raise a 404 Not Found error if place is not found
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a specific Review object with id (review_id)"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)  # Raise a 404 Not Found error if review is not found
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review_for_place(place_id):
    """Create a new Review object and link it to a Place object
    using place_id key"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    json_data = request.get_json()
    if not json_data:
        return make_response("Not a JSON", 400)

    if 'user_id' not in json_data:
        return make_response("Missing user_id", 400)

    user = storage.get(User, json_data['user_id'])
    if user is None:
        abort(404)

    if 'text' not in json_data:
        return make_response("Missing text", 400)

    json_data['place_id'] = place_id
    new_review = Review(**json_data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a specific Review object with id (review_id)"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)  # Raise a 404 Not Found error if review is not found

    json_data = request.get_json()
    if not json_data:
        return make_response("Not a JSON", 400)

    # Update Place object with key-value pairs from JSON data
    for key, value in json_data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
