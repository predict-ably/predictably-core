#!/usr/bin/env python3 -u
# copyright: predictably developers, BSD-3-Clause License (see LICENSE file)
# Elements of predictably.validate reuse code developed for skbase. These elements
# are copyrighted by the skbase developers, BSD-3-Clause License. For
# conditions see https://github.com/sktime/skbase/blob/main/LICENSE
"""Tests of the functionality for validating iterables of named objects.

tests in this module test the functionality of:

- check_path
- check_type
- check_sequence
- is_iterable
- is_sequence
"""

from __future__ import annotations

import pathlib
from collections import defaultdict

import numpy as np
import pytest

from predictably_core.core._base import BaseEstimator, BaseObject
from predictably_core.validate import (
    check_mapping,
    check_path,
    check_sequence,
    check_type,
    is_iterable,
    is_mapping,
    is_sequence,
)
from predictably_core.validate._types import _is_scalar_nan

__author__: list[str] = ["RNKuhns"]

_mapping_test_cases = [
    {"case": {"something": 1, "something_else": 2}, "params": {}, "valid": True},
    {
        "case": {"something": 1, "something_else": 2},
        "params": {"key_type": str},
        "valid": True,
    },
    {
        "case": {"something": 1, "something_else": 2},
        "params": {"key_type": str, "value_type": int},
        "valid": True,
    },
    {
        "case": {"something": 1, "something_else": 2},
        "params": {"key_type": str, "value_type": float},
        "valid": False,
    },
    {
        "case": {"something": 1, "something_else": 2},
        "params": {"key_type": float, "value_type": str},
        "valid": False,
    },
    {
        "case": {"something": 1, "something_else": 2},
        "params": {"key_type": float},
        "valid": False,
    },
    {
        "case": {"something": 1, "something_else": 2},
        "params": {"value_type": str},
        "valid": False,
    },
    {
        "case": {"something": 1, "something_else": 2},
        "params": {"map_type": defaultdict},
        "valid": False,
    },
    {
        "case": defaultdict(lambda: 0, {"something": 1, "something_else": 2}),
        "params": {"map_type": dict},
        "valid": True,
    },
]


@pytest.fixture
def fixture_object_instance():
    """Pytest fixture of BaseObject instance."""
    return BaseObject()


@pytest.fixture
def fixture_estimator_instance():
    """Pytest fixture of BaseObject instance."""
    return BaseEstimator()


@pytest.mark.parametrize("mapping_cases", _mapping_test_cases)
def test_is_mapping(mapping_cases) -> None:
    """Test is_mapping works as expected."""
    is_valid = is_mapping(mapping_cases["case"], **mapping_cases["params"])
    assert is_valid == mapping_cases["valid"]


@pytest.mark.parametrize("mapping_cases", _mapping_test_cases)
def test_check_mapping(mapping_cases) -> None:
    """Test check_mapping works as expected."""
    if mapping_cases["valid"]:
        mapping = check_mapping(mapping_cases["case"], **mapping_cases["params"])
        assert mapping == mapping_cases["case"]
    else:
        with pytest.raises(ValueError, match=r"The mapping `input_` is invalid\..*"):
            check_mapping(mapping_cases["case"], **mapping_cases["params"])


def test_is_iterable() -> None:
    """Test is_iterable works as expected."""
    assert is_iterable([1, 2, 3])
    assert is_iterable({"a": 1})
    assert is_iterable("some_string")
    assert is_iterable(c for c in (1, 2, 3))
    assert is_iterable(17) is False
    assert is_iterable(17.0) is False


@pytest.mark.parametrize(
    "path_input",
    ("c:/some/path/", "c:/", "a:/something", "//a/b/c/", pathlib.Path("c:/")),
)
def test_check_path(path_input) -> None:
    """Test check_path returns expected output."""
    assert isinstance(check_path(path_input), pathlib.Path)


@pytest.mark.parametrize("path_input", (8, 11.0, int))
def test_check_path_raises_on_invalid_input(path_input) -> None:
    """Test check_path raises on invalid input."""
    with pytest.raises(ValueError, match="`path_` must be a pathlib.Path.*"):
        check_path(path_input)
    with pytest.raises(ValueError, match="`something_else` must be a pathlib.Path.*"):
        check_path(path_input, path_error_name="something_else")


def test_check_type_output(fixture_estimator_instance, fixture_object_instance):
    """Test check type returns expected output."""
    assert check_type(7, expected_type=int) == 7
    assert check_type(7.2, expected_type=float) == 7.2
    assert check_type(7.2, expected_type=(float, int)) == 7.2
    assert check_type("something", expected_type=str) == "something"
    assert check_type(None, expected_type=str, allow_none=True) is None
    assert check_type(["a", 7, fixture_object_instance], expected_type=list) == [
        "a",
        7,
        fixture_object_instance,
    ]
    assert (
        check_type(fixture_estimator_instance, expected_type=BaseObject)
        == fixture_estimator_instance
    )
    assert check_type(None, expected_type=int, allow_none=True) is None

    with pytest.raises(TypeError, match=r"`input_` should be type.*"):
        check_type(7.2, expected_type=int)

    with pytest.raises(TypeError, match=r"`input_` should be type.*"):
        check_type("something", expected_type=(int, float))

    with pytest.raises(TypeError, match=r"`input_` should be type.*"):
        check_type(BaseEstimator, expected_type=BaseObject)

    with pytest.raises(TypeError, match=r"^`input_` should be.*"):
        check_type("something", expected_type=int, allow_none=True)

    # Verify optional use of issubclass instead of isinstance
    assert (
        check_type(BaseEstimator, expected_type=BaseObject, use_subclass=True)
        == BaseEstimator
    )
    with pytest.raises(TypeError, match=r"^`input_` should subclass.*"):
        check_type(BaseObject, expected_type=BaseEstimator, use_subclass=True)
    with pytest.raises(TypeError, match="^`input_` should be.*"):
        check_type(None, expected_type=str)


def test_check_type_raises_error_if_expected_type_is_wrong_format():
    """Test check_type raises an error if expected_type wrong format.

    `expected_type` should be a type or tuple of types.
    """
    with pytest.raises(TypeError, match="^`expected_type` should be.*"):
        check_type(7, expected_type=11)

    with pytest.raises(TypeError, match="^`expected_type` should be.*"):
        check_type(7, expected_type=[int])

    with pytest.raises(TypeError, match="^`expected_type` should be.*"):
        check_type(None, expected_type=[int])


def test_is_sequence_output():
    """Test is_sequence returns expected output.

    This excludes test of class and class instance usage, which is included in
    test_is_sequence_with_seq_of_class_and_instance_input.
    """
    import numpy as np

    # Test simple example with no constraints on sequence_type or element_type
    # True for any sequence
    assert is_sequence([1, 2, 3]) is True
    # But false for generators, since they are iterable but not sequences
    assert is_sequence(c for c in [1, 2, 3]) is False

    # Test use of sequence_type restriction
    assert is_sequence([1, 2, 3, 4], sequence_type=list) is True
    assert is_sequence([1, 2, 3, 4], sequence_type=tuple) is False
    assert is_sequence((1, 2, 3, 4), sequence_type=list) is False
    assert is_sequence((1, 2, 3, 4), sequence_type=tuple) is True

    # Test use of element_type restriction
    assert is_sequence([1, 2, 3], element_type=int) is True
    assert is_sequence([1, 2, 3], element_type=float) is False
    assert is_sequence([1, 2, 3, 4], sequence_type=list, element_type=int) is True
    assert is_sequence([1, 2, 3, 4], sequence_type=tuple, element_type=int) is False
    assert is_sequence([1, 2, 3, 4], sequence_type=list, element_type=float) is False
    assert is_sequence([1, 2, 3, 4], sequence_type=tuple, element_type=float) is False

    # Tests using different types
    assert is_sequence("abc") is True  # strings are iterable and sequences in Python
    assert is_sequence([1, "something", 4.5]) is True
    assert is_sequence([1, "something", 4.5], element_type=float) is False
    assert (
        is_sequence(
            ("a string", "or another string"), sequence_type=tuple, element_type=str
        )
        is True
    )

    # Test with 3rd party types works in default way via exact type
    assert is_sequence([1.2, 4.7], element_type=np.float64) is False
    assert (
        is_sequence([np.float64(1.2), np.float64(4.7)], element_type=np.float64) is True
    )

    # np.nan is float, not int or np.float64
    assert is_sequence([np.nan, 4.8], element_type=float) is True
    assert is_sequence([np.nan, 4], element_type=int) is False


def test_is_sequence_with_seq_of_class_and_instance_input(
    fixture_estimator_instance, fixture_object_instance
):
    """Test is_sequence returns expected value with sequence of classes as input."""
    # Verify we can identify sequences of a given class type as valid sequences
    input_seq = (fixture_estimator_instance, fixture_object_instance)
    assert is_sequence(input_seq, element_type=BaseObject) is True
    assert (
        is_sequence(list(input_seq), sequence_type=list, element_type=BaseObject)
        is True
    )
    # Verify we detect when list elements are not instances of valid class type
    assert is_sequence([1, 2, 3], element_type=BaseObject) is False

    # Verify we can identify sequences of class types as valid sequences of types
    input_seq = (BaseObject, BaseEstimator)
    assert is_sequence(input_seq, element_type=type) is True
    assert is_sequence(list(input_seq), sequence_type=list, element_type=type) is True
    # Verify we detect when list elements are not instances of valid types
    assert is_sequence([1, 2, 3], element_type=BaseObject) is False


def test_check_sequence_output():
    """Test check_sequence returns expected output.

    This excludes test of class and class instance usage, which is included in
    test_check_sequence_with_seq_of_class_and_instance_input.
    """
    import numpy as np

    # Test simple example with no constraints on sequence_type or element_type
    # True for any sequence
    assert check_sequence([1, 2, 3]) == [1, 2, 3]
    assert check_sequence([1, "a", 3.4, False]) == [1, "a", 3.4, False]
    # But false for generators, since they are iterable but not sequences
    with pytest.raises(
        TypeError,
        match="Invalid sequence: Input sequence expected to be a sequence.",
    ):
        assert check_sequence(c for c in [1, 2, 3])

    # Test use of sequence_type restriction
    assert check_sequence([1, 2, 3, 4], sequence_type=list) == [1, 2, 3, 4]
    with pytest.raises(
        TypeError,
        match="Invalid sequence: Input sequence expected to be a tuple.",
    ):
        check_sequence([1, 2, 3, 4], sequence_type=tuple)
    with pytest.raises(
        TypeError,
        match="Invalid sequence: Input sequence expected to be a list.",
    ):
        check_sequence((1, 2, 3, 4), sequence_type=list)
    assert check_sequence((1, 2, 3, 4), sequence_type=tuple) == (1, 2, 3, 4)
    assert check_sequence((1, 2, 3, 4), sequence_type=(list, tuple)) == (1, 2, 3, 4)

    # Test use of element_type restriction
    assert check_sequence([1, 2, 3], element_type=int) == [1, 2, 3]
    assert check_sequence([1, 2, 3], element_type=(float, int)) == [1, 2, 3]
    assert check_sequence([1, 2, False, "a", 3], element_type=(bool, str, int)) == [
        1,
        2,
        False,
        "a",
        3,
    ]

    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        check_sequence([1, 2, 3], element_type=float)
    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        check_sequence([1, 2, 3, 4], sequence_type=tuple, element_type=int)
    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        check_sequence([1, 2, 3, 4], sequence_type=list, element_type=float)
    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        check_sequence([1, 2, 3, 4], sequence_type=tuple, element_type=float)

    input_seq = [1, 2, 3, 4]
    assert check_sequence(input_seq, sequence_type=list, element_type=int) == input_seq

    # Tests using different types
    # strings are iterable and sequences in Python
    assert check_sequence("abc") == "abc"
    assert check_sequence([1, "something", 4.5]) == [1, "something", 4.5]
    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        check_sequence([1, "something", 4.5], element_type=float)

    assert check_sequence(
        ("a string", "or another string"), sequence_type=tuple, element_type=str
    ) == ("a string", "or another string")

    # Test with 3rd party types works in default way via exact type
    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        check_sequence([1.2, 4.7], element_type=np.float64)
    input_seq = [np.float64(1.2), np.float64(4.7)]
    assert check_sequence(input_seq, element_type=np.float64) == input_seq

    # np.nan is float, not int or np.float64
    assert check_sequence([np.nan, 4.8], element_type=float) == [np.nan, 4.8]
    assert check_sequence([np.nan, 4.8, 7], element_type=(float, int)) == [
        np.nan,
        4.8,
        7,
    ]
    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        check_sequence([np.nan, 4], element_type=int)

    # Check return type coercion to specified sequence type
    input_seq = [1, 2, 3, 4]
    assert check_sequence(
        input_seq, sequence_type=list, element_type=int, coerce_output_type_to=tuple
    ) == tuple(input_seq)


def test_check_sequence_scalar_input_coercion():
    """Test check_sequence coerces scalar inputs to sequences as expected."""
    assert check_sequence(7, element_type=int, coerce_scalar_input=True) == (7,)
    assert check_sequence(
        7, element_type=int, coerce_output_type_to=list, coerce_scalar_input=True
    ) == [7]

    # Note that single strings treated as scalars for this purpose
    assert check_sequence(
        "some string", element_type=str, coerce_scalar_input=True
    ) == ("some string",)

    # coercion takes into account allowed sequence_types
    assert check_sequence(
        7, element_type=int, sequence_type=list, coerce_scalar_input=True
    ) == [7]
    # If more than one sequence_type allowed then the first is used for coercion
    assert check_sequence(
        7, element_type=int, sequence_type=(list, tuple), coerce_scalar_input=True
    ) == [7]
    # Output type conversion overrides input type coercion to specified sequence_type
    assert check_sequence(
        7,
        element_type=int,
        sequence_type=list,
        coerce_output_type_to=tuple,
        coerce_scalar_input=True,
    ) == (7,)

    # Still raise an error if element type is not expected
    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        check_sequence(
            7,
            sequence_type=list,
            element_type=float,
            coerce_scalar_input=True,
        )


def test_check_sequence_with_seq_of_class_and_instance_input(
    fixture_estimator_instance, fixture_object_instance
):
    """Test check_sequence returns expected value with sequence of classes as input."""
    # Verify we can identify sequences of a given class type as valid sequences
    input_seq = (fixture_estimator_instance, fixture_object_instance)
    assert check_sequence(input_seq, element_type=BaseObject) == input_seq
    assert check_sequence(
        list(input_seq), sequence_type=list, element_type=BaseObject
    ) == list(input_seq)

    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        check_sequence(list(input_seq), sequence_type=tuple, element_type=BaseObject)
    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        # Verify we detect when list elements are not instances of valid class type
        check_sequence([1, 2, 3], element_type=BaseObject)

    # Verify we can identify sequences of class types as valid sequences of types
    input_seq = (BaseObject, BaseEstimator)
    assert check_sequence(input_seq, element_type=type) == input_seq
    assert check_sequence(
        list(input_seq), sequence_type=list, element_type=type
    ) == list(input_seq)
    with pytest.raises(
        TypeError,
        match="Invalid sequence: .*",
    ):
        # Verify we detect when list elements are not instances of valid types
        check_sequence([1, 2, 3], element_type=BaseObject)


def test_is_scalar_nan() -> None:
    """Test _is_scalar_nan work as expected."""
    assert _is_scalar_nan(np.nan)
    assert _is_scalar_nan(float("nan"))
    assert _is_scalar_nan(None) is False
    assert _is_scalar_nan("") is False
    assert _is_scalar_nan([np.nan]) is False
