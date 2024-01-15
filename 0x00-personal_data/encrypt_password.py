#!/usr/bin/env python3
"""using bcrypt to encrypt password"""

import bcrypt


def hash_password(password: str) -> bytes:
    """return hashed version of the password"""
    password = password.encode()
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check password matches"""
    encoded_version = password.encode()
    if bcrypt.checkpw(encoded_version, hashed_password):
        return True
    return False
