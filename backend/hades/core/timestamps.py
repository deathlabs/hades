"""Defines utility functions."""

# Standard library imports.
from datetime import datetime


def get_timestamp() -> str:
    """
    Returns the current date/time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
