"""
Validator Class

The code is licensed under the MIT license.
"""

from inspect import isfunction, signature
from typing import Callable, Optional
from pandas import DataFrame, Series


class Validator:
    """
    Schema Column Validator
    """

    func: Optional[Callable] = None
    ignore_na = False

    def __init__(self, func: Callable, ignore_na=False):
        self.func = func
        self.ignore_na = ignore_na

    def run(self, series: Series, df: DataFrame, column: str) -> bool | Series:
        """
        Run validator

        Returns a bool series:
        True -> Check passed
        False -> Check failed
        """
        arg_count = len((signature(self.func)).parameters)
        args = [series, df, column]
        return self.func(*args[0:arg_count])


def apply_validator(validator: Validator, df: DataFrame, column: str) -> Series:
    """
    Validate a DataFrame's column using a validator
    """
    validator = validator() if isfunction(validator) else validator
    if validator.ignore_na:
        result = Series(data=True, index=df.index, dtype=bool)
        result.update(
            validator.run(
                df.loc[df[column].notnull()][column],
                df.loc[df[column].notnull()],
                column,
            )
        )
        return result.astype(bool)
    return validator.run(df[column], df, column)
