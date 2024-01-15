#!/usr/bin/env python3
"""replace in a string using regex"""
import re
from typing import List
import logging


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
