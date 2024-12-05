"""
Maximum Difference Validator

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def max_diff(value: int | float) -> Series:
    """
    Maximum difference compared to previous value
    """

    def _func(series: Series) -> Series:
        result = Series(data=0, index=series.index)
        result.update(series.iloc[1:].diff().notnull().abs())
        return result <= value

    return Validator(_func)
