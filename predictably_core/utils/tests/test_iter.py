#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
# Elements of predictably.utils reuse code developed for skbase. These elements
# are copyrighted by the skbase developers, BSD-3-Clause License. For
# conditions see https://github.com/sktime/skbase/blob/main/LICENSE
"""Tests of the functionality for working with iterables.

This tests the module predictably_core.utils._iter.
"""

from __future__ import annotations

import collections

import pytest

from predictably_core.utils._iter import (
    _convert_scalar_seq_type_input_to_tuple,
    format_sequence_to_str,
    scalar_to_sequence,
    single_element_sequence_to_scalar,
)

__author__: list[str] = ["RNKuhns"]


class SomeClass:
    """Test class."""

    def __init__(self, a: int = 7) -> None:
        self.a = a


def test_single_element_sequence_to_scalar() -> None:
    """Test single_element_sequence_to_scalar output is as expected."""
    # Verify that length > 1 sequence not impacted.
    assert single_element_sequence_to_scalar([1, 2, 3]) == [1, 2, 3]

    # Verify single member of sequence is removed as expected
    assert single_element_sequence_to_scalar([1]) == 1


def test_scalar_to_sequence_expected_output() -> None:
    """Test _scalar_to_seq returns expected output."""
    assert scalar_to_sequence(7) == (7,)
    # Verify it works with scalar classes and objects
    assert scalar_to_sequence(int) == (int,)
    assert scalar_to_sequence(SomeClass) == (SomeClass,)
    # Verify things work with class instance
    some_class = SomeClass()
    assert scalar_to_sequence(some_class) == (some_class,)
    # Verify strings treated like scalar not sequence
    assert scalar_to_sequence("some_str") == ("some_str",)
    assert scalar_to_sequence("some_str", sequence_type=list) == ["some_str"]

    # Verify sequences returned unchanged
    assert scalar_to_sequence((1, 2)) == (1, 2)

    # None is treated like empty sequence
    assert scalar_to_sequence(None) == ()
    assert scalar_to_sequence(None, sequence_type=list) == []


def test_scalar_to_sequence_raises() -> None:
    """Test scalar_to_seq raises error when `sequence_type` is unexpected type."""
    with pytest.raises(
        ValueError,
        match="`sequence_type` must be a subclass of collections.abc.Sequence.",
    ):
        scalar_to_sequence(7, sequence_type=int)

    with pytest.raises(
        ValueError,
        match="`sequence_type` must be a subclass of collections.abc.Sequence.",
    ):
        scalar_to_sequence(7, sequence_type=dict)
    with pytest.raises(
        ValueError,
        match="`sequence_type` must be a subclass of collections.abc.Sequence.",
    ):
        scalar_to_sequence(7, sequence_type=11)


def test_format_seq_to_str() -> None:
    """Test format_sequence_to_str returns expected output."""
    # Test basic functionality (including ability to handle str and non-str)
    seq = [1, 2, "3", 4]
    assert format_sequence_to_str(seq) == "1, 2, 3, 4"

    # Test use of last_sep
    assert format_sequence_to_str(seq, last_sep="and") == "1, 2, 3 and 4"
    assert format_sequence_to_str(seq, last_sep="or") == "1, 2, 3 or 4"

    # Test use of different sep argument
    assert format_sequence_to_str(seq, sep=";") == "1;2;3;4"

    # Test using remove_type_text keyword
    assert (
        format_sequence_to_str([list, tuple], exclude_type_text=False)
        == "<class 'list'>, <class 'tuple'>"
    )
    assert (
        format_sequence_to_str([list, tuple], exclude_type_text=True) == "list, tuple"
    )
    assert (
        format_sequence_to_str([list, tuple], last_sep="and", exclude_type_text=True)
        == "list and tuple"
    )

    assert format_sequence_to_str(int) == "<class 'int'>"
    assert format_sequence_to_str(int, exclude_type_text=True) == "int"

    # Test with scalar inputs
    assert format_sequence_to_str(7) == "7"  # int, float, bool primitives cast to str
    assert format_sequence_to_str("some_str") == "some_str"
    # Verify that keywords don't affect output
    assert format_sequence_to_str(7, sep=";") == "7"
    assert format_sequence_to_str(7, last_sep="or") == "7"


def test_format_seq_to_str_raises() -> None:
    """Test format_sequence_to_str raises error when input is unexpected type."""

    class SomeClass:
        def __init__(self, a):
            self.a = a

        def __repr__(self):
            raise TypeError()

    with pytest.raises(ValueError):
        format_sequence_to_str(SomeClass(7))


def test_convert_scalar_seq_type_input_to_tuple() -> None:
    """Test _convert_scalar_seq_type_input_to_tuple outputs expected."""
    output = _convert_scalar_seq_type_input_to_tuple(int)
    assert output == (int,)
    output = _convert_scalar_seq_type_input_to_tuple((int, float))
    assert output == (int, float)
    output = _convert_scalar_seq_type_input_to_tuple(None)
    assert output == (collections.abc.Sequence,)
    output = _convert_scalar_seq_type_input_to_tuple(None, none_default=list)
    assert output == (list,)


def test_convert_scalar_seq_type_input_to_tuple_raises() -> None:
    """Test _convert_scalar_seq_type_input_to_tuple raises on invalid input."""
    # Raises because 7 is not a type
    with pytest.raises(
        TypeError, match=r"`type_input` should be a type or sequence of types."
    ):
        _convert_scalar_seq_type_input_to_tuple(7)

    # Test error message uses input_name
    with pytest.raises(
        TypeError, match=r"`some_input` should be a type or sequence of types."
    ):
        _convert_scalar_seq_type_input_to_tuple(7, type_input_error_name="some_input")

    # Raises error because dict is a type but not a subclass of type_input_subclass
    with pytest.raises(
        TypeError, match=r"`type_input` should be a type or sequence of types."
    ):
        _convert_scalar_seq_type_input_to_tuple(
            dict,
            type_input_subclass=collections.abc.Sequence,
        )
