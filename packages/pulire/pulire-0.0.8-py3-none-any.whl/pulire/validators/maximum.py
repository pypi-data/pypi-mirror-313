"""
Maximum Validator

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def maximum(value: int | float) -> Series:
    """
    Numeric maximum
    """

    def _func(series: Series) -> Series:
        return series <= value

    return Validator(_func)
