#!/usr/bin/python3
"""
Routing /status to return the status of the API
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    dic = {"status": "OK"}
    return jsonify(dic)


@app_views.route("/stats", strict_slashes=False)
def stats():
    stats_dict = {}
    stats_dict["amenities"] = storage.count(Amenity)
    stats_dict["cities"] = storage.count(City)
    stats_dict["places"] = storage.count(Place)
    stats_dict["reviews"] = storage.count(Review)
    stats_dict["states"] = storage.count(State)
    stats_dict["users"] = storage.count(User)
    return jsonify(stats_dict)