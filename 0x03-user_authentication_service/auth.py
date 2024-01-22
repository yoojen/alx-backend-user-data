#!/usr/bin/env python3
"""Hash method"""

from db import DB
from bcrypt import hashpw, gensalt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """
    receive password as string
    arguments -- password: to be converted to hashed version

    returns -- bytes
    """
    password = password.encode()
    hashed_version = hashpw(password, gensalt())

    return hashed_version


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password) -> User:
        """method to register user in the db"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            if hashed_password:
                registered_user = self._db.add_user(email, hashed_password)
            return registered_user
        else:
            raise ValueError(f"User {email} already exists")
