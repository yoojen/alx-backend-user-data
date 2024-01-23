#!/usr/bin/env python3
"""Basic flask application"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """home path"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
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
def login():
    """method to post user session in the db"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
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


@app.route('/session', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout the use by destroying session id"""
    cur_user_session_id = request.cookies.get('session_id', None)
    found_user = AUTH.get_user_from_session_id(cur_user_session_id)
    if not found_user:
        abort(403)
    AUTH.destroy_session(found_user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """respond to GET /profile"""
    user_session_id = request.form.get('session_id', None)
    print(user_session_id)
    found_user = AUTH.get_user_from_session_id(user_session_id)
    print(found_user.email)
    print(found_user.session_id)
    if found_user and found_user.session_id:
        return jsonify({"email": found_user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
