#!/usr/bin/python3
"""
Routing /status to return the status of the API
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status", strict_slashes=False)
def status():
    dic = {"status": "OK"}
    return jsonify(dic)
