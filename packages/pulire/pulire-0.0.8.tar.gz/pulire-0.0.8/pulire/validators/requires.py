"""
Requires Validator

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def requires(column: str) -> Series:
    """
    Require another column not to be null
    """

    def _func(series: Series) -> Series:
        return series[column].notna()

    return Validator(_func)
