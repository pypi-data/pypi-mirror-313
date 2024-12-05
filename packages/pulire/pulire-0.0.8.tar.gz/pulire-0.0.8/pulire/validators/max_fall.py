"""
Maximum Decrease Validator

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def max_fall(value: int | float) -> Series:
    """
    Maximum decrease compared to previous value
    """

    def _func(series: Series) -> Series:
        result = Series(data=0, index=series.index)
        result.update(series.iloc[1:].diff().notnull())
        return result >= value * -1

    return Validator(_func)
