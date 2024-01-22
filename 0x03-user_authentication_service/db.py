#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from bcrypt import hashpw, gensalt
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Save the user to the database

        Keyword arguments:
        email -- user email
        hashed_password -- hashed version of initial password
        Return: returns the user object
        """
        hashed_password = hashed_password.encode()
        hashed_version = hashpw(hashed_password, gensalt())
        user = User(email=email, hashed_password=hashed_version)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, *args: tuple, **kwargs: dict) -> User:
        """find user in the db

        Keyword arguments:
        args -- arguments with key=value
        Return: returns the first row found in the users table 
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user
