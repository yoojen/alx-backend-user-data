#!/usr/bin/env python3
"""replace in a string using regex"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """return filtered input message"""
    for field in fields:
        message = re.sub(rf'(?<={field}=)[^{separator}]+',
                         f'{redaction}', message)
    return message
