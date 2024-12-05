"""
Column Class

The code is licensed under the MIT license.
"""

from typing import List

from pulire.formatter import Formatter
from pulire.validator import Validator


class Column:
    """
    Schema Column
    """

    name: str
    dtype: str
    annotations: List[Validator | Formatter]

    def __init__(
        self, name: str, dtype: str, annotations: List[Validator | Formatter] = []
    ):
        self.name = name
        self.dtype = dtype
        self.annotations = annotations

    @property
    def validators(self) -> List[Validator]:
        """
        List of validators
        """
        return [
            annotation
            for annotation in self.annotations
            if isinstance(annotation, Validator)
        ]

    @property
    def formatters(self) -> List[Formatter]:
        """
        List of formatters
        """
        return [
            annotation
            for annotation in self.annotations
            if isinstance(annotation, Formatter)
        ]
