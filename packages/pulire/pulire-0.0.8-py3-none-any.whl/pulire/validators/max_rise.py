"""
Maximum Increase Validator

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def max_rise(value: int | float) -> Series:
    """
    Maximum increase compared to previous value
    """

    def _func(series: Series) -> Series:
        result = Series(data=0, index=series.index)
        result.update(series.iloc[1:].diff().notnull())
        return result <= value

    return Validator(_func)
