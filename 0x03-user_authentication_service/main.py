#!/usr/bin/env python3
"""test module for api"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """test register user model from auth module"""
    data = {"email": email, "password": password}
    res = requests.post(f"{BASE_URL}/users", data=data)

    res_msg = {"email": email, "message": "user created"}
    assert res.status_code == 200
    assert res.json() == res_msg


def log_in_wrong_password(email: str, password: str) -> None:
    """test login user model with incorrect credentials"""
    data = {"email": email, "password": password}
    res = requests.post(f"{BASE_URL}/sessions", data=data)

    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """test login user model with correct credentials"""
    data = {"email": email, "password": password}
    res = requests.post(f"{BASE_URL}/sessions", data=data)

    res_msg = {"email": email, "message": "logged in"}
    assert res.status_code == 200
    assert res.json() == res_msg
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """test profile of user model with incorrect credentials"""

    data = {"session_id": None}
    res = requests.get(f"{BASE_URL}/profile", data=data)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """test profile of user model with correct credentials"""

    data = {"session_id": session_id}
    res = requests.get(f"{BASE_URL}/profile", data=data)
    assert res.status_code == 200
    assert res.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """test logout  with correct credentials"""

    data = {"session_id": session_id}
    res = requests.delete(f"{BASE_URL}/sessions", data=data)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """test reset password token and generate token"""

    data = {"email": email}
    res = requests.post(f"{BASE_URL}/reset_password", data=data)
    assert res.status_code == 200
    msg = {"email": email, "reset_token": res.json().get('reset_token')}
    assert res.json() == msg
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update the password for  user"""
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    res = requests.put(f"{BASE_URL}/reset_password", data=data)
    assert res.status_code == 200
    msg = {"email": email,
           "message": "Password updated"}
    assert res.json() == msg


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
