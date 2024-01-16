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
        if path is None or excluded_paths is None:
            return True
        filtered_paths = excluded_paths[:]
        if path:
            if path[-1] != '/':
                path = path + '/'
            for excluded in excluded_paths:
                if excluded[-1] != '/':
                    filtered_paths.append(excluded + '/')
            if path not in filtered_paths:
                return True
            else:
                return False

    def authorization_header(self, request=None) -> str:
        """check for authorized header"""
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """return the current user"""
        return None
