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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout the use by destroying session id"""
    cur_user_session_id = request.cookies.get('session_id', None)
    if cur_user_session_id is None:
        abort(403)
    found_user = AUTH.get_user_from_session_id(cur_user_session_id)
    if found_user is None:
        abort(403)
    AUTH.destroy_session(found_user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """respond to GET /profile"""
    user_session_id = request.cookies.get('session_id', None)
    if user_session_id is None:
        abort(403)
    found_user = AUTH.get_user_from_session_id(user_session_id)

    if found_user is None:
        abort(403)
    return jsonify({"email": found_user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """handle reset password POST request"""
    email = request.form.get('email', None)
    if email:
        try:
            reset_token = AUTH.get_reset_password_token(email)
        except ValueError:
            abort(403)
    else:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """update the password for the user found"""
    email, reset_token, new_password = request.form.get('email', None), \
        request.form.get('reset_token', None), \
        request.form.get('new_password', None)
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email,
                    "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
