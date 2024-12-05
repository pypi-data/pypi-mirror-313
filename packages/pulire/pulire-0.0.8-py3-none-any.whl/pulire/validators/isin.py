"""
Is-In Validator

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def isin(values: list) -> Series:
    """
    Require column value to be in a list of values
    """

    def _func(series: Series) -> Series:
        return series.isin(values)

    return Validator(_func, ignore_na=True)
