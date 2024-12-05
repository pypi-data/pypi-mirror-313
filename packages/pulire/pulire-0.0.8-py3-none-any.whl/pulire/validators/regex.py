"""
Regular Expression Validator

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def regex(pattern: str) -> Series:
    """
    Check if column values match regex pattern
    """

    def _func(series: Series) -> Series:
        return series.str.contains(pattern)

    return Validator(_func, ignore_na=True)
