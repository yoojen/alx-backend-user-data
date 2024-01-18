#!/usr/bin/env python3
""" view that deals with authantication
"""

from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from os import getenv


@app_views.route('POST /auth_session/login', methods=['POST'],
                 strict_slashes=False)
def handles_session():
    """view that handles all routes for the Session authentication."""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].get(user.id))
    res = jsonify(user[0].to_json())
    res.set_cookie(getenv('SESSION_NAME'), session_id)
    return res
