#!/usr/bin/env python3
"""replace in a string using regex"""
import re
from typing import List
import logging
import mysql
import os

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """return filtered input message"""
    for field in fields:
        message = re.sub(rf'(?<={field}=)[^{separator}]+',
                         f'{redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """return formated string of loggin.LogRecord"""
        record.msg = filter_datum(
            self.fields, self.REDACTION,
            super().format(record=record), self.SEPARATOR)
        return record.msg


def get_logger() -> logging.Logger:
    """returns the logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connect to myql db using environment variables"""
  
    username: str = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password: str = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host: str = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database: str = os.environ.get("PERSONAL_DATA_DB_NAME")
    conn: mysql.connector.connection.MySQLConnection = connector.connection.MySQLConnection(user=username,
                                                   password=password,
                                                   host=host,
                                                   database=database)
    return conn


def main():
    """retrieve all rows in the users table"""
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM users')
    fields = [field[0] for field in cursor.description]
    logger = get_logger()
    for user in cursor:
        msg = ''.join(f'{field}={str(row)}; ' for row,
                      field in zip(user, fields))
        logger.info(msg=msg)

    cursor.close()
    db_conn.close()


if __name__ == "__main__":
    main()
