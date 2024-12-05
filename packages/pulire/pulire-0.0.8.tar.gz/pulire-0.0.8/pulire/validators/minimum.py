"""
Minimum Validator

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def minimum(value: int | float) -> Series:
    """
    Numeric minimum
    """

    def _func(series: Series) -> Series:
        return series >= value

    return Validator(_func)
