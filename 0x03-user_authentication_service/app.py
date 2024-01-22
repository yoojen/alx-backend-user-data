#!/usr/bin/env python3
"""Basic flask application"""

from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """home path"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """method to post user in the db"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
    except KeyError:
        abort(400)
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def update_user_session():
    """method to post user session in the db"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
    except KeyError:
        abort(401)
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            res = jsonify({"email": email, "message": "logged in"})
            res.set_cookie('session_id', session_id)
            return res
        else:
            abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
