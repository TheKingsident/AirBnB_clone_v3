#!/usr/bin/python3
"""Defines the methods for the State objects"""
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/', methods=['GET'])
def get_states_w_slash():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get('State', state_id)
    if state:
        return jsonify([state.to_dict()])
    abort(404)


@app_views.route('/states/<state_id>/', methods=['GET'])
def get_state_w_slash(state_id):
    """Retrieves a State object"""
    state = storage.get('State', state_id)
    if state:
        return jsonify([state.to_dict()])
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/', methods=['DELETE'])
def delete_state_w_slash(state_id):
    """Deletes a State object"""
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State"""
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    if 'name' not in request_data:
        abort(400, description="Missing name")
    new_state = State(**request_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/', methods=['POST'])
def create_state_w_slash():
    """Creates a State"""
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    if 'name' not in request_data:
        abort(400, description="Missing name")
    new_state = State(**request_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>/', methods=['PUT'])
def update_state_w_slash(state_id):
    """Updates a State object"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
