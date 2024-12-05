"""
Maximum Peak Prominence Validator

The code is licensed under the MIT license.
"""

from pandas import Series
from pulire.utils import calculate_peak_prominence
from ..validator import Validator


def max_peak(value: int | float) -> Series:
    """
    Maximum peak prominence of a values in a time series
    """

    def _func(series: Series) -> Series:
        prominence = calculate_peak_prominence(series)
        return prominence < value

    return Validator(_func)
