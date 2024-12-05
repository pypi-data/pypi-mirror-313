"""
Schema Validators

The code is licensed under the MIT license.
"""

from .required import required
from .minimum import minimum
from .maximum import maximum
from .requires import requires
from .greater import greater
from .less import less
from .max_fall import max_fall
from .max_rise import max_rise
from .max_diff import max_diff
from .max_peak import max_peak
from .isin import isin
from .regex import regex

__all__ = [
    "required",
    "minimum",
    "maximum",
    "requires",
    "greater",
    "less",
    "max_fall",
    "max_rise",
    "max_diff",
    "max_peak",
    "isin",
    "regex",
]
