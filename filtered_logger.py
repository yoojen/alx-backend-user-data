#!/usr/bin/env python3
"""replace in a string using regex"""
import re


def filter_datum(fields, redaction, message: str, separator):
    """return filtered input message"""
    for field in fields:
        message = re.sub(rf'(?<={field}=)[^{separator}]+',
                         f'{redaction}', message)
    return message
