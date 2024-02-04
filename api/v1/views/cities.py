#!/usr/bin/python3
"""Defines the methods for the City objects"""
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """Retrieves the list of all City objects"""
    cities = storage.all(City).values()
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get('City', city_id)
    if city:
        return jsonify([city.to_dict()])
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def create_city():
    """Creates a City"""
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    if 'name' not in request_data:
        abort(400, description="Missing name")
    new_city = City(**request_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at', 'state_id']
    for key, value in request_data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
