#!/usr/bin/env python3
"""Authentication model"""

from db import DB
from bcrypt import hashpw, gensalt, checkpw
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    receive password as string
    arguments -- password: to be converted to hashed version

    returns -- bytes
    """
    password = password.encode()
    hashed_version = hashpw(password, gensalt())

    return hashed_version


def _generate_uuid() -> str:
    """returns random uuid string"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """method to register user in the db"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            registered_user = self._db.add_user(email, hashed_password)
            return registered_user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """locate user from the db storage"""
        try:
            found_user = self._db.find_user_by(email=email)
            if checkpw(password.encode(), found_user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        It takes an email string argument
        returns the session ID as a string.
        """
        try:
            found_user = self._db.find_user_by(email=email)
            user_session_id = _generate_uuid()
            self._db.update_user(
                found_user.id, session_id=user_session_id)
            return found_user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        It takes a single session_id string argument
        returns the corresponding User or None.
        """
        try:
            found_user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return found_user

    def destroy_session(self, user_id: int) -> None:
        """destroys the user session_id in the db storage"""
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """find user associated to the email"""
        try:
            found_user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(found_user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """update the password for the user"""
        try:
            found_user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        password = _hash_password(password)
        self._db.update_user(
            found_user.id, hashed_password=password, reset_token=None)
