"""
Less Validator

The code is licensed under the MIT license.
"""

from pandas import Series, DataFrame
from ..validator import Validator


def less(column: str) -> Series:
    """
    Require column to be less than another one
    """

    def _func(series: Series, df: DataFrame, name: str) -> Series:
        result = Series(data=True, index=series.index)
        df = df[df[name].notnull() & df[column].notnull()]
        result.update(df[name] < df[column])
        return result.astype(bool)

    return Validator(_func)
