#!/usr/bin/env python3 -u
# copyright: predictably developers, BSD-3-Clause License (see LICENSE file)
# Elements of predictably.validate reuse code developed for skbase. These elements
# are copyrighted by the skbase developers, BSD-3-Clause License. For
# conditions see https://github.com/sktime/skbase/blob/main/LICENSE
"""Tools for validating and comparing predictably objects and collections.

This module contains functions used throughout `predictably` to provide standard
validation of inputs to `predictably` methods and functions.
"""

from __future__ import annotations

from predictably_core.validate._types import (
    check_path,
    check_sequence,
    check_type,
    is_iterable,
    is_sequence,
)

__author__: list[str] = ["RNKuhns"]
__all__: list[str] = [
    "check_path",
    "check_sequence",
    "check_type",
    "is_iterable",
    "is_sequence",
]
