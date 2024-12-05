"""
Schema Class

The code is licensed under the MIT license.
"""

from copy import copy
from typing import List, Union
from pandas import DataFrame, to_numeric

from pulire.column import Column
from pulire.validator import apply_validator
from pulire.formatter import apply_formatter


class Schema:
    """
    DataFrame Schema
    """

    columns: List[Column]

    def __init__(self, columns: List[Column]):
        self.columns = columns

    @property
    def names(self) -> List[str]:
        """
        List of column names
        """
        return [col.name for col in self.columns]

    @property
    def dtypes(self) -> dict:
        """
        Dictionary of data types
        """
        return {col.name: col.dtype for col in self.columns}

    def fit(self, df: DataFrame) -> DataFrame:
        """
        Set data types, apply formatters and remove invalid data from a DataFrame
        """
        temp = copy(df)

        temp = self.purge(temp)
        temp = self.fill(temp)
        temp = self.format(temp)
        temp = self.clean(temp)

        return temp
    
    def purge(self, df: DataFrame) -> DataFrame:
        """
        Remove DataFrame columns which are not in the schema
        """
        columns = [col for col in self.names if col in df.columns]
        return df[columns]
    
    def fill(self, df: DataFrame, value = None) -> DataFrame:
        """
        Add missing schema columns to DataFrame
        """
        temp = copy(df)

        for col in self.names:
            if col not in df:
                temp[col] = value

        return temp

    def format(self, df: DataFrame) -> DataFrame:
        """
        Set data types and apply formatters to a DataFrame
        """
        temp = copy(df)

        # Set data types
        for col, dtype in self.dtypes.items():
            if col in temp:
                if dtype == "Int64":
                    temp[col] = to_numeric(temp[col]).round(0)
                temp[col] = temp[col].astype(dtype, errors="ignore")

        # Apply formatters
        for col in self.columns:
            if col.name in temp.columns:
                for formatter in col.formatters:
                    temp[col.name] = apply_formatter(formatter, temp, col.name)

        return temp

    def clean(self, df: DataFrame, fill=None) -> DataFrame:
        """
        Remove invalid data from a DataFrame
        """
        temp = copy(df)

        for col in self.columns:
            if col.name in temp.columns:
                for validator in col.validators:
                    test = apply_validator(validator, temp, col.name)
                    temp.loc[~test, col.name] = fill

        return temp

    def validate(self, df: DataFrame, lazy=False) -> None:
        """
        Raise error for failing validations
        """
        errors: List[str] = []

        for col in self.columns:
            if col.name in df.columns:
                for validator in col.validators:
                    test = apply_validator(validator, df, col.name)
                    if not test.all():
                        for index in test[~test].index:
                            value = df.loc[index, col.name]
                            error = f'Value "{value}" at index "{index}" in column "{col.name}" did not pass validation'
                            if lazy:
                                errors.append(error)
                            else:
                                raise ValueError(error)

        raise ValueError(*errors)

    def match(self, df: DataFrame) -> bool:
        """
        Check if a DataFrame is valid
        """
        for col in self.columns:
            if col.name in df.columns:
                for validator in col.validators:
                    test = apply_validator(validator, df, col.name)
                    if not test.all():
                        return False
        return True

    def __getitem__(self, key: str | List[str]) -> Union["Schema", Column]:
        """
        Select a subset of columns or a specific Column object by name
        """
        if isinstance(key, str):
            # Return the specific Column object for the given column name
            for col in self.columns:
                if col.name == key:
                    return col
            raise KeyError(f"Column '{key}' not found in schema.")
        elif isinstance(key, list):
            # Return a new Schema with a subset of columns
            cols = [col for col in self.columns if col.name in key]
            return Schema(cols)
        raise TypeError("Key must be a string or a list of strings.")