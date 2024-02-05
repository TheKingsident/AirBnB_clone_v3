#!/usr/bin/python3
"""For Users End point"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)
    
@app_views.route('users', methods=['POST'], strict_slashes=False)
def create_user():
    user_request = request.get_json()
    if not user_request:
        abort(400, description="Not a JSON")
    if 'email' not in user_request:
        abort(400, description="Missing email")
    if 'password' not in user_request:
        abort(400, description="Missing password")
    new_user = User(**user_request)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)
    
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user_request = request.get_json()
    if not user_request:
        abort(400, description="Not a JSON")
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in user_request.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
