#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Authentication Class """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 authentication header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:
        """return decoded authorization header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            convertable_bytes = base64_authorization_header.encode('utf-8')
            converted_bytes = b64decode(convertable_bytes)
            decoded_string = converted_bytes.decode('utf-8')
        except BaseException:
            return None
        return decoded_string

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """get user credentials from decoded base64"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        usr_name, pwd = decoded_base64_authorization_header.split(
            ":")[0], decoded_base64_authorization_header.split(":")[1]
        return usr_name, pwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
