#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
# Elements of predictably.utils reuse code developed for skbase. These elements
# are copyrighted by the skbase developers, BSD-3-Clause License. For
# conditions see https://github.com/sktime/skbase/blob/main/LICENSE
"""Utility functionality for working with sequences."""  # numpydoc ignore=ES01

from __future__ import annotations

import collections
import inspect
from typing import Any, Optional, Sequence, TypeVar, Union

from predictably_core.utils._utils import remove_type_text

__author__: list[str] = ["RNKuhns"]
__all__: list[str] = [
    "_convert_scalar_seq_type_input_to_tuple",
    "format_sequence_to_str",
    "scalar_to_sequence",
    "single_element_sequence_to_scalar",
]

T = TypeVar("T")


def single_element_sequence_to_scalar(x: Sequence[T]) -> Union[T, Sequence[T]]:
    """Remove tuple wrapping from singleton.

    If the input has length 1, then the single value is extracted from the input.
    Otherwise, the input is returned unchanged.

    Parameters
    ----------
    x : Sequence[Any]
        The sequence to remove a singleton value from.

    Returns
    -------
    Any
        The singleton value of x if x[0] is a singleton, otherwise x.

    Examples
    --------
    >>> from predictably_core.utils._iter import single_element_sequence_to_scalar
    >>> single_element_sequence_to_scalar([1])
    1
    >>> single_element_sequence_to_scalar([1, 2, 3])
    [1, 2, 3]
    """
    if len(x) == 1:
        return x[0]
    else:
        return x


def scalar_to_sequence(
    scalar: Union[T, Sequence[T], None], sequence_type: type = tuple
) -> Sequence[T]:
    """Convert a scalar input to a sequence.

    If the input is already a sequence it is returned unchanged. Unlike standard
    Python, a string is treated as a scalar instead of a sequence. None is also
    treated like an empty sequence.

    Parameters
    ----------
    scalar : Any | Sequence[Any] | None
        A scalar input to be converted to a sequence.
    sequence_type : type
        A sequence type (e.g., list, tuple) that is used to set the return type. This
        is ignored if `scalar` is already a sequence other than a str (which is
        treated like a scalar type for this function instead of sequence of
        characters).

        - If None, then the returned sequence will be a tuple containing a single
          scalar element.
        - If `sequence_type` is a valid sequence type then the returned
          sequence will be a sequence of that type containing the single scalar
          value.

    Returns
    -------
    Sequence[Any]
        A sequence of the specified `sequence_type` that contains just the single
        scalar value.

    Examples
    --------
    >>> from predictably_core.utils._iter import scalar_to_sequence
    >>> scalar_to_sequence(7)
    (7,)
    >>> scalar_to_sequence("some_str")
    ('some_str',)
    >>> scalar_to_sequence("some_str", sequence_type=list)
    ['some_str']
    >>> scalar_to_sequence((1, 2))
    (1, 2)

    None is treated like an empty sequence.

    >>> scalar_to_sequence(None)
    ()
    >>> scalar_to_sequence(None, sequence_type=list)
    []
    """
    error_msg = "`sequence_type` must be a subclass of collections.abc.Sequence.\n"
    error_msg += (
        f"But `sequence_type` was {sequence_type} of type {type(sequence_type)}."
    )
    if not (isinstance(sequence_type, type) and callable(sequence_type)):
        raise ValueError(error_msg)

    if scalar is None:
        return sequence_type()
    # We'll treat str like regular scalar and not a sequence
    elif isinstance(scalar, collections.abc.Sequence) and not isinstance(scalar, str):
        return scalar
    elif (
        issubclass(sequence_type, collections.abc.Sequence)
        and sequence_type != Sequence
    ):
        # Note calling (scalar,) is done to avoid str unpacking
        return sequence_type((scalar,))  # type: ignore
    else:
        raise ValueError(error_msg)


def format_sequence_to_str(
    seq: Union[Any, Sequence[Any]],
    sep: str = ", ",
    last_sep: Optional[str] = None,
    exclude_type_text: bool = False,
) -> str:
    """Format a sequence to a string of delimited elements.

    This is useful to format sequences into a pretty printing format for
    creating error messages or warnings.

    Parameters
    ----------
    seq : Any | Sequence[Any]
        The input sequence to convert to a str of the elements separated by `sep`.
    sep : str
        The separator to use when creating the str output.
    last_sep : str  None, default=None
        The separator to use prior to last element.

        - If None, then `sep` is used. So (7, 9, 11) return "7", "9", "11" for
          ``sep=", "``.
        - If last_sep is a str, then it is used prior to last element. So
          (7, 9, 11) would be "7", "9" and "11" if ``last_sep="and"``.

    exclude_type_text : bool, default=False
        Whether to remove the <class > text wrapping the class type name, when
        formatting types.

        - If True, then input sequence [list, tuple] returns "list, tuple"
        - If False, then input sequence [list, tuple] returns
          "<class 'list'>, <class 'tuple'>".

    Returns
    -------
    str
        The sequence of inputs converted to a string. For example, if `seq`
        is (7, 9, "cart") and ``last_sep is None`` then the output is "7", "9", "cart".

    Examples
    --------
    >>> from predictably_core.utils._iter import format_sequence_to_str
    >>> seq = [1, 2, 3, 4]
    >>> format_sequence_to_str(seq)
    '1, 2, 3, 4'
    >>> format_sequence_to_str(seq, last_sep="and")
    '1, 2, 3 and 4'
    >>> format_sequence_to_str(seq, last_sep="or")
    '1, 2, 3 or 4'
    """
    from predictably_core.validate._types import is_iterable

    if isinstance(seq, str):
        output_str = seq
    elif isinstance(seq, type):
        output_str = remove_type_text(str(seq)) if exclude_type_text else str(seq)
    elif isinstance(seq, collections.abc.Sequence) or is_iterable(seq):
        seq_str = [
            remove_type_text(str(e)) if exclude_type_text else str(e) for e in seq
        ]
        if last_sep is None:
            output_str = sep.join(seq_str)
        else:
            if len(seq_str) == 1:
                output_str = single_element_sequence_to_scalar(seq_str)
            else:
                output_str = sep.join(seq_str[:-1])
                output_str = output_str + f" {last_sep} " + seq_str[-1]
    # Allow casting of scalars to strings
    else:
        try:
            output_str = str(seq)
        except Exception as e:
            msg = "`seq` must be a sequence or scalar that can be converted to a str."
            raise ValueError(msg) from e

    return output_str


def _convert_scalar_seq_type_input_to_tuple(
    type_input: Union[type, Sequence[type]],
    none_default: Optional[type] = None,
    type_input_subclass: Optional[type] = None,
    type_input_error_name: str = "type_input",
) -> tuple[type, ...]:
    """Convert input that is scalar or sequence of types to always be a tuple.

    Scalar types are converted to a tuple with a single element, while sequences of
    types are converted to a tuple of types.

    Parameters
    ----------
    type_input : type | sequence[type]
        The input type(s) to convert to a tuple of types as output.
    none_default : type, default=collections.abc.Sequence
        Default type to output for None.
    type_input_subclass : type, default=None
        Subclass that input type(s) must be.

        - If None (default), then no check of subtyping is applied.
        - Otherwise, all the input types are checked to see if they are a sub class
          of `type_input_subclass`.

    type_input_error_name : str, default="type_input"
        Name to use when referring to `type_input` in any raised error messages.

    Returns
    -------
    tuple[type, ...]
        Tuple of types. If a single type was input, then a tuple with the input type
        as a single element is returned. If a sequence of types was input, then
        a tuple with the same length as the input sequence of types is returned.

    Raises
    ------
    TypeError
        If `type_input` is not a type or sequence of types. If `type_input_subclass`
        is not None then an error is also raised if any of the type(s) is not
        a subclass of the specified type.
    """
    if none_default is None:
        none_default = collections.abc.Sequence

    seq_output: tuple[type, ...]
    if type_input is None:
        seq_output = (none_default,)
    # if a sequence of types received as type_input and all types are
    # allowed subclasses of types, then convert to tuple of types
    elif isinstance(type_input, collections.abc.Sequence) and all(
        (isinstance(e, type) or inspect.isclass(type_input))
        and (type_input_subclass is None or issubclass(e, type_input_subclass))
        for e in type_input
    ):
        seq_output = tuple(type_input)
    elif (isinstance(type_input, type) or inspect.isclass(type_input)) and (
        type_input_subclass is None or issubclass(type_input, type_input_subclass)
    ):
        seq_output = (type_input,)
    else:
        raise TypeError(
            f"`{type_input_error_name}` should be a type or sequence of types."
        )

    return seq_output
