#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
# Elements of predictably.utils reuse code developed for skbase. These elements
# are copyrighted by the skbase developers, BSD-3-Clause License. For
# conditions see https://github.com/sktime/skbase/blob/main/LICENSE
"""Tests of additional utility functionality.

This tests the predictably_core.utils._utils module.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import ForwardRef

import pytest

from predictably_core.utils._utils import (
    compare_mappings,
    remove_type_text,
    update_dict_at,
)

__author__: list[str] = ["RNKuhns"]


def test_remove_type_text() -> None:
    """Test remove_type_text removes <class ... > text as expected."""
    msg = "Not removing type text from type"
    assert remove_type_text(int) == "int", msg
    assert remove_type_text(Sequence) == "collections.abc.Sequence", msg
    msg = "Not removing type text from str"
    assert remove_type_text("<class 'int'>") == "int", msg
    msg = "Not leaving strings without <class ...> text unchanged."
    assert remove_type_text("int") == "int", msg
    assert remove_type_text("<type 'int'>") == "<type 'int'>", msg
    msg = "Not removing ForwardRef"
    assert remove_type_text(ForwardRef("int")) == "int", msg
    assert remove_type_text("ForwardRef('pd.DataFrame')") == "pd.DataFrame", msg


def test_compare_mappings() -> None:
    """Test compare_mappings output matches expectations."""
    some_map = {"a": 1, "b": 2}
    other_map = {"b": 2, "a": 1}

    assert compare_mappings(some_map, other_map, ordered=False)
    assert compare_mappings(some_map, other_map, ordered=True) is False

    some_other_map = {"b": 3, "a": 6}
    assert compare_mappings(some_map, some_other_map, ordered=False) is False
    assert compare_mappings(some_map, some_other_map, ordered=True) is False
    assert compare_mappings(some_map, some_other_map, values=False, ordered=False)
    assert (
        compare_mappings(some_map, some_other_map, values=False, ordered=True) is False
    )


def test_compare_mappings_raises() -> None:
    """Test compare_mappings on invalid input."""
    # Verify function raises if input_dict and new_dict aren't both dicts
    with pytest.raises(ValueError, match="`map_` and `other_map`.*"):
        compare_mappings(7, {"a": 1})
    with pytest.raises(ValueError, match="`map_` and `other_map`.*"):
        compare_mappings({"a": 1}, 7)
    with pytest.raises(ValueError, match="`map_` and `other_map`.*"):
        compare_mappings(11, 7)


def test_update_dict_at() -> None:
    """Test update_dict_at output matches expectations."""
    starting = {"a": 1, "b": 2, "c": 3, "d": 4}
    new = {"e": 5, "f": 6}
    new2 = {"g": 7, "a": -1}
    new3 = {"e": 5, "f": 6, "d": -1}

    updated = update_dict_at(starting, new)
    assert updated == {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6}
    updated = update_dict_at(starting, new2)
    assert updated == {"a": -1, "b": 2, "c": 3, "d": 4, "g": 7}

    # Test use of `at` parameter
    # Positive at updates at index starting from the beginning
    updated = update_dict_at(starting, new, at=2)
    assert updated == {"a": 1, "b": 2, "e": 5, "f": 6, "c": 3, "d": 4}
    # Negative at updates at index starting from the end
    updated = update_dict_at(starting, new, at=-1)
    assert updated == {"a": 1, "b": 2, "c": 3, "e": 5, "f": 6, "d": 4}

    # Verify at larger than length updates at end
    updated = update_dict_at(starting, new, at=99)
    assert updated == {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6}
    # Verify negative at larger in magnitude then length updates at beginning
    updated = update_dict_at(starting, new, at=-99)
    assert updated == {"e": 5, "f": 6, "a": 1, "b": 2, "c": 3, "d": 4}

    updated = update_dict_at(starting, new3, at=2)
    assert updated == {"a": 1, "b": 2, "e": 5, "f": 6, "d": -1, "c": 3}

    # Verify keep_new=False works as expected
    updated = update_dict_at(starting, new3, at=2, keep_new=False)
    assert updated == {"a": 1, "b": 2, "e": 5, "f": 6, "d": 4, "c": 3}


def test_update_dict_at_raises() -> None:
    """Test update_dict_at_raises on invalid input."""
    # Verify function raises if input_dict and new_dict aren't both dicts
    with pytest.raises(ValueError, match="`input_dict` and `new_dict`.*"):
        update_dict_at(7, {"a": 1})
    with pytest.raises(ValueError, match="`input_dict` and `new_dict`.*"):
        update_dict_at(7, {"a": 1}, at=1)
    with pytest.raises(ValueError, match="`input_dict` and `new_dict`.*"):
        update_dict_at({"a": 1}, 7)
    with pytest.raises(ValueError, match="`input_dict` and `new_dict`.*"):
        update_dict_at({"a": 1}, 7, at=1)
    with pytest.raises(ValueError, match="`input_dict` and `new_dict`.*"):
        update_dict_at(11, 7, at=1)

    # Verify invalid at raises
    with pytest.raises(ValueError, match="`at` must be an int.*"):
        update_dict_at({"a": 1}, {"b": 2}, at="7")

    # When input isn't all dicts and at is invalid, the non-dict input raises first
    with pytest.raises(ValueError, match="`input_dict` and `new_dict`.*"):
        update_dict_at(7, {"a": 1}, at="7")
