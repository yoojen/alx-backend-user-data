#!/usr/bin/env python3
"""Hash method"""

from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
    receive password as string
    arguments -- password: to be converted to hashed version

    returns -- bytes
    """
    password = password.encode()
    hashed_version = hashpw(password, gensalt())

    return hashed_version
