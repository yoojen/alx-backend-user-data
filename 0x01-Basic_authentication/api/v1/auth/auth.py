#!/usr/bin/env python3
"""
Configuration of API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check if user is authorized"""
        return False

    def authorization_header(self, request=None) -> str:
        """check for authorized header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """return the current user"""
        return None
