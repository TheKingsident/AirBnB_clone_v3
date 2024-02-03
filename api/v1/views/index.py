#!/usr/bin/python3
"""Returns the API status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON response"""
    return jsonify(
        {
            "status": "OK"
        }
    )


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieves the number of each object by type."""
    obj_counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(obj_counts)
