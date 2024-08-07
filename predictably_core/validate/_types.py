#!/usr/bin/env python3 -u
# copyright: predictably developers, BSD-3-Clause License (see LICENSE file)
# Elements of predictably.validate._types reuse code developed for skbase. These
# elements are copyrighted by the skbase developers, BSD-3-Clause License. For
# conditions see https://github.com/sktime/skbase/blob/main/LICENSE
"""Tools for general type validation.

For specific functionality to validate the `predictably` data types, see
:mod:`predictably.validate._data_types`.
"""

from __future__ import annotations

import collections
import inspect
import math
import numbers
import pathlib
from typing import TYPE_CHECKING, Any, Sequence, TypeVar, overload

from predictably_core.utils._iter import (
    _convert_scalar_seq_type_input_to_tuple,
    format_sequence_to_str,
    remove_type_text,
    scalar_to_sequence,
)

__author__: list[str] = ["RNKuhns"]
__all__: list[str] = [
    "_is_scalar_nan",
    "check_path",
    "check_sequence",
    "check_type",
    "is_iterable",
    "is_sequence",
]

T = TypeVar("T")


def is_iterable(input_: T) -> bool:
    """Indicate if input is iterable.

    Input is considered iterable if it inherits from `collections.abc.Iterable`,
    otherwise implements the __iter__ dunder, or is a generator.

    Parameters
    ----------
    input_ : Any
        The input to check to see if it is iterable.

    Returns
    -------
    bool
        Whether `input_` is iterable.

    Examples
    --------
    >>> from predictably_core.validate import is_iterable
    >>> is_iterable([1,2, 3])
    True
    >>> is_iterable({"a": 1})
    True
    >>> is_iterable("some_string")
    True

    Generators are also iterable.

    >>> is_iterable(c for c in (1, 2, 3))
    True

    The expected result is returned for non-iterable input.

    >>> is_iterable(17)
    False
    >>> is_iterable(17.0)
    False
    """
    if (
        isinstance(input_, collections.abc.Iterable)
        or (hasattr(input_, "__iter__") and callable(input_.__iter__))
        or inspect.isgenerator(input_)
    ):
        is_iter = True
    else:
        is_iter = False
    return is_iter


@overload
def check_path(
    path_: str, path_error_name: str = "path_"
) -> pathlib.Path:  # numpydoc ignore=GL08
    ...  # pragma: no cover


@overload
def check_path(
    path_: pathlib.Path, path_error_name: str = "path_"
) -> pathlib.Path:  # numpydoc ignore=GL08
    ...  # pragma: no cover


def check_path(
    path_: str | pathlib.Path, path_error_name: str = "path_"
) -> pathlib.Path:
    """Validate `path` is `pathlib.Path` or `str`.

    Input is considered a valid path if it is a pathlib.Path or string that is
    convertible to a pathlib.Path.

    Parameters
    ----------
    path_ : str | pathlib.Path
        The path to validate.
    path_error_name : str, default="path_"
        The name to refer to `path_` as in error messages that are raised. This
        is useful if you are using this to check a path inside other code and
        want to raise a message with the name of the variable being validated.

    Returns
    -------
    pathlib.Path
        The validated path.

    Raises
    ------
    ValueError :
        If the input `path` is not a pathlib.Path or str that is coercible
        to a pathlib.Path.

    Examples
    --------
    >>> import pathlib
    >>> from predictably_core.validate import check_path
    >>> check_path("//some/path")  # doctest: +SKIP
    >>> check_path(pathlib.Path("//some/path"))  # doctest: +SKIP

    An error is raised when the input is not a path or str coercible to a path.

    >>> check_path(1234)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: `path_` must be a pathlib.Path object or a str, but ...
    """
    if isinstance(path_, pathlib.Path):
        return path_
    elif isinstance(path_, str):
        return pathlib.Path(path_)
    else:
        raise ValueError(
            f"`{path_error_name}` must be a pathlib.Path object or a str, but "
            f"input has value {path_} of type {remove_type_text(type(path_))}."
        )


def check_type(
    input_: T,
    expected_type: type | tuple[type, ...],
    allow_none: bool = False,
    use_subclass: bool = False,
    input_error_name: str = "input_",
) -> T:
    """Check the input is the expected type.

    Validates that the input is the type specified in `expected_type`, while optionally
    allowing None values as well (if ``allow_none=True``). For flexibility,
    the check can use ``issubclass`` instead of ``isinstance`` if ``use_subclass=True``.

    Parameters
    ----------
    input_ : Any
        The input to be type checked.
    expected_type : type
        The type that `input_` is expected to be.
    allow_none : bool, default=False
        Whether `input_` can be None in addition to being instance of `expected_type`.
    use_subclass : bool, default=False
        Whether to check the type using issubclass instead of isinstance.

        - If True, then `check_type` uses issubclass.
        - If False (default), then `check_type` uses isinstance.

    input_error_name : str, default="input_"
        The name to refer to `input_` as in any raised error messages. This
        is useful if you are using this to check a variable's type inside other
        code and want to raise a message with the name of the variable being
        validated.

    Returns
    -------
    Any
        The input.

    Raises
    ------
    TypeError
        If input does match expected type using isinstance by default
        or using issubclass in check if ``use_subclass=True``.

    Examples
    --------
    >>> from predictably_core.validate import check_type
    >>> check_type(7, expected_type=int)
    7
    >>> check_type(7.2, expected_type=(int, float))
    7.2

    An error is raised if the input is not the expected type

    >>> check_type(7, expected_type=str)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: `input_` should be type str, but found int.
    """
    # process expected_type parameter
    if not isinstance(expected_type, (type, tuple)):
        msg = " ".join(
            [
                "`expected_type` should be type or tuple of types,"
                f"but found {remove_type_text(expected_type)}."
            ]
        )
        raise TypeError(msg)

    # Check the type of input_
    type_check = issubclass if use_subclass else isinstance
    if not allow_none and input_ is None:
        is_expected_type = False
    elif allow_none and input_ is None:
        is_expected_type = True
    else:
        is_expected_type = type_check(input_, expected_type)

    if not is_expected_type:
        chk_msg = "subclass type" if use_subclass else "be type"
        if isinstance(expected_type, tuple):
            expected_type_str = format_sequence_to_str(
                [remove_type_text(t) for t in expected_type], last_sep="or"
            )
        else:
            expected_type_str = remove_type_text(expected_type)
        input_type_str = remove_type_text(type(input_))
        if allow_none:
            type_msg = f"{expected_type_str} or None"
        else:
            type_msg = f"{expected_type_str}"
        raise TypeError(
            f"`{input_error_name}` should {chk_msg} {type_msg}, but "
            f"found {input_type_str}."
        )
    return input_


def is_sequence(
    input_seq: Any,
    sequence_type: type | tuple[type, ...] | None = None,
    element_type: type | tuple[type, ...] | None = None,
) -> bool:
    """Indicate if an object is a sequence with optional check of element types.

    If `element_type` is supplied all elements are also checked against provided types.

    Parameters
    ----------
    input_seq : Any
        The input sequence to be validated.
    sequence_type : type or tuple[type, ...], default=None
        The allowed sequence type(s) that `input_seq` can be an instance of.

        - If None, then collections.abc.Sequence is used (all sequence types are valid)
        - If `sequence_type` is a type or tuple of types, then only the specified
          types are considered valid.

    element_type : type or tuple[type], default=None
        The allowed type(s) for elements of `input_seq`.

        - If None, then the elements of `input_seq` are not checked when determining
          if `input_seq` is a valid sequence.
        - If `element_type` is a type or tuple of types, then the elements of
          `input_seq` are checked to make sure they are all instances of
          the supplied `element_type`.

    Returns
    -------
    bool
        Whether the input is a valid sequence based on the supplied `sequence_type`
        and `element_type`.

    Examples
    --------
    >>> from predictably_core.validate import is_sequence
    >>> is_sequence([1, 2, 3])
    True
    >>> is_sequence(7)
    False

    Generators are not sequences

    >>> is_sequence((c for c in [1, 2, 3]))
    False

    The expected sequence type can be included in the check

    >>> is_sequence([1, 2, 3, 4], sequence_type=list)
    True
    >>> is_sequence([1, 2, 3, 4], sequence_type=tuple)
    False

    The type of the elements can also be checked

    >>> is_sequence([1, 2, 3], element_type=int)
    True
    >>> is_sequence([1, 2, 3, 4], sequence_type=list, element_type=int)
    True
    >>> is_sequence([1, 2, 3, 4], sequence_type=list, element_type=float)
    False
    >>> is_sequence([1, 2, 3, 4], sequence_type=list, element_type=(int, float))
    True
    """
    sequence_type_ = _convert_scalar_seq_type_input_to_tuple(
        sequence_type,
        type_input_subclass=collections.abc.Sequence,
        type_input_error_name="sequence_type",
    )

    is_valid_sequence = isinstance(input_seq, sequence_type_)

    # Optionally verify elements have correct types
    if element_type is not None:
        element_type_ = _convert_scalar_seq_type_input_to_tuple(
            element_type, type_input_error_name="element_type"
        )
        if not all(isinstance(e, element_type_) for e in input_seq):
            is_valid_sequence = False

    return is_valid_sequence


def check_sequence(
    input_seq: Sequence[Any],
    sequence_type: type | tuple[type, ...] | None = None,
    element_type: type | tuple[type, ...] | None = None,
    coerce_output_type_to: type | None = None,
    coerce_scalar_input: bool = False,
    sequence_name: str | None = None,
) -> Sequence[Any]:
    """Check whether an object is a sequence with optional check of element types.

    If `element_type` is supplied all elements are also checked against provided types.

    Parameters
    ----------
    input_seq : Any
        The input sequence to be validated.
    sequence_type : type or tuple[type], default=None
        The allowed sequence type that `seq` can be an instance of.
    element_type : type or tuple[type], default=None
        The allowed type(s) for elements of `seq`.
    coerce_output_type_to : sequence type, default=None
        The sequence type that the output sequence should be coerced to.

        - If None, then the output sequence is the same as input sequence.
        - If a sequence type (e.g., list, tuple) is provided then the output sequence
          is coerced to that type.

    coerce_scalar_input : bool, default=False
        Whether scalar input should be coerced to a sequence type prior to running
        the check. If True, a scalar input like will be coerced to a tuple containing
        a single scalar. To output a sequence type other than a tuple, set the
        `coerce_output_type_to` keyword to the desired sequence type (e.g., list).
    sequence_name : str, default=None
        Name of `input_seq` to use if error messages are raised.

    Returns
    -------
    Sequence
        The input sequence if has expected type.

    Raises
    ------
    TypeError :
        If `seq` is not instance of `sequence_type` or ``element_type is not None`` and
        all elements are not instances of `element_type`.

    Examples
    --------
    >>> from predictably_core.validate import check_sequence

    >>> check_sequence([1, 2, 3])
    [1, 2, 3]

    Generators are not sequences so an error is raised

    >>> check_sequence((c for c in [1, 2, 3]))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: Invalid sequence: Input sequence expected to be a sequence.

    The check can require a certain type of sequence

    >>> check_sequence([1, 2, 3, 4], sequence_type=list)
    [1, 2, 3, 4]

    Expected to raise and error because the input is not a tuple

    >>> check_sequence([1, 2, 3, 4], sequence_type=tuple)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: Invalid sequence: Input sequence expected to be a tuple.

    It is also possible to check the type of sequence elements

    >>> check_sequence([1, 2, 3], element_type=int)
    [1, 2, 3]
    >>> check_sequence([1, 2, 3, 4], sequence_type=list, element_type=(int, float))
    [1, 2, 3, 4]
    """
    if coerce_scalar_input:
        if sequence_type is None:
            input_seq = scalar_to_sequence(input_seq, sequence_type=tuple)
        elif isinstance(sequence_type, tuple):
            # If multiple sequence types allowed then use first one
            seq_type_ = sequence_type[0] if sequence_type[0] is not None else tuple
            input_seq = scalar_to_sequence(input_seq, sequence_type=seq_type_)
        else:
            input_seq = scalar_to_sequence(input_seq, sequence_type=sequence_type)

    is_valid_seqeunce = is_sequence(
        input_seq,
        sequence_type=sequence_type,
        element_type=element_type,
    )
    # Raise error is format is not expected.
    if not is_valid_seqeunce:
        name_str = "Input sequence" if sequence_name is None else f"`{sequence_name}`"
        if sequence_type is None:
            seq_str = "sequence"
        else:
            sequence_type_ = _convert_scalar_seq_type_input_to_tuple(
                sequence_type,
                type_input_subclass=collections.abc.Sequence,
                type_input_error_name="sequence_type",
            )
            seq_str = format_sequence_to_str(
                sequence_type_, last_sep="or", exclude_type_text=True
            )

        msg = f"Invalid sequence: {name_str} expected to be a {seq_str}."

        if element_type is not None:
            element_type_ = _convert_scalar_seq_type_input_to_tuple(
                element_type, type_input_error_name="element_type"
            )
            element_str = format_sequence_to_str(
                element_type_, last_sep="or", exclude_type_text=True
            )
            msg = msg[:-1] + f" with elements of type {element_str}."

        raise TypeError(msg)

    if coerce_output_type_to is not None:
        output_ = coerce_output_type_to(input_seq)
        if TYPE_CHECKING:  # pragma: no cover
            assert isinstance(output_, collections.abc.Sequence)  # noqa: RUF100, S101
        return output_

    return input_seq


def _is_scalar_nan(x: Any) -> bool:
    """Test if x is NaN.

    This function is meant to overcome the issue that np.isnan does not allow
    non-numerical types as input, and that np.nan is not float('nan').

    Parameters
    ----------
    x : Any
        The item to be checked to determine if it is a scalar nan value.

    Returns
    -------
    bool
        True if `x` is a scalar nan value.

    Notes
    -----
    This code follows scikit-learn's implementation.

    Examples
    --------
    >>> import numpy as np
    >>> from predictably_core.validate._types import _is_scalar_nan
    >>> _is_scalar_nan(np.nan)
    True
    >>> _is_scalar_nan(float("nan"))
    True
    >>> _is_scalar_nan(None)
    False
    >>> _is_scalar_nan("")
    False
    >>> _is_scalar_nan([np.nan])
    False
    """
    return isinstance(x, numbers.Real) and math.isnan(x)
