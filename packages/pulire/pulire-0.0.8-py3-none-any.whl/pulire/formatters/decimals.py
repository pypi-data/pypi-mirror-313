"""
Decimals Formatter

The code is licensed under the MIT license.
"""

from pandas import Series
from ..formatter import Formatter


def decimals(digits: int) -> Series:
    """
    Round a series to the specified number of fractional digits
    """

    def _func(series: Series) -> Series:
        return series.round(digits)

    return Formatter(_func)
