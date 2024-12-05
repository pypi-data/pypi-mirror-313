"""
Required Validator

The code is licensed under the MIT license.
"""

from pandas import Series, notna
from ..validator import Validator


def required() -> Series:
    """
    Require the current column not to be null
    """
    return Validator(notna)
