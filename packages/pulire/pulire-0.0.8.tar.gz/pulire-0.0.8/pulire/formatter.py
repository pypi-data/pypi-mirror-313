"""
Formatter Class

The code is licensed under the MIT license.
"""

from inspect import isfunction, signature
from typing import Callable, Optional
from pandas import DataFrame, Series


class Formatter:
    """
    Schema Column Formatter
    """

    func: Optional[Callable] = None

    def __init__(self, func: Callable):
        self.func = func

    def run(self, series: Series, df: DataFrame, column: str) -> Series:
        """
        Format all values in a series
        """
        arg_count = len((signature(self.func)).parameters)
        args = [series, df, column]
        return self.func(*args[0:arg_count])


def apply_formatter(formatter: Formatter, df: DataFrame, column: str) -> Series:
    """
    Format a DataFrame's column using a formatter
    """
    formatter = formatter() if isfunction(formatter) else formatter
    return formatter.run(df[column], df, column)
