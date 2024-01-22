#!/usr/bin/env python3
"""module that defines the user model in the db"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column

Base = declarative_base()


class User(Base):
    """User model definition"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(256), nullable=False)
    hashed_password = Column(String(256), nullable=False)
    session_id = Column(String(256))
    reset_token = Column(String(256))
