"""Utility functions for use through `predictably`-style packages."""  # numpydoc ignore=ES01

from __future__ import annotations

import collections
import re
from typing import Any, Mapping, Optional, Union

__author__: list[str] = ["RNKuhns"]
__all__: list[str] = ["compare_mappings", "remove_type_text", "update_dict_at"]


def remove_type_text(input_: Union[str, type]) -> str:
    """Remove <class >  or ForwardRf() wrapper from printed type str.

    If the input doesn't have the wrapper <class > or ForwardRef() text it
    is returned unchanged.

    Parameters
    ----------
    input_ : str | type
        The input to remove <class > wrapper when printing class.

    Returns
    -------
    str
        The text version of the class without the <class > wrapper.

    Examples
    --------
    >>> from predictably_core.utils import remove_type_text
    >>> remove_type_text(int)
    'int'
    >>> remove_type_text("<class 'int'>")
    'int'
    >>> remove_type_text("int")
    'int'
    >>> remove_type_text("ForwardRef('pd.DataFrame')")
    'pd.DataFrame'
    """
    if not isinstance(input_, str):
        input_ = str(input_)

    m = re.match("^<class '(.*)'>$", input_)

    if m:
        return m[1]

    else:
        m_forward_ref = re.match(r"^ForwardRef\('(.*)'\)", input_)
        if m_forward_ref:
            return m_forward_ref[1]
        else:
            return input_


def compare_mappings(
    map_: Mapping[Any, Any],
    other_map: Mapping[Any, Any],
    values: bool = True,
    ordered: bool = True,
) -> bool:
    """Compare if two mappings are equal.

    Equality is interpretted as having the same keys, and optionally having the
    same values and ordering.

    Parameters
    ----------
    map_ : Mapping[Any, Any]
        The mapping to compare to.
    other_map: Mapping[Any, Any]
        The mapping to compare to `map_`.
    values : bool, default=True
        Whether to require the mappings to have the same values.
    ordered : bool, default=True
        Whether to require the mappings to have the same order.

    Returns
    -------
    bool
        Whether two mappings are "equal".

    Examples
    --------
    >>> from predictably_core.utils import compare_mappings
    >>> some_map = {"a": 1, "b": 2}
    >>> other_map = {"b": 2, "a": 1}

    The built-in dictionary comparison does not require ordering

    >>> some_map == other_map
    True
    >>> compare_mappings(some_map, other_map, ordered=False)
    True

    Setting the ordered parameter to True enables ordered comparisons.

    >>> compare_mappings(some_map, other_map, ordered=True)
    False

    It is also possible to just check the equality of the keys.

    >>> another_map = {"a": 3, "b": 4}
    >>> compare_mappings(some_map, another_map)  # default is values=True
    False
    >>> compare_mappings(some_map, another_map, values=False)
    True

    As expected mappings of different lengths always return False.

    >>> yet_another_map = {"a": 1}
    >>> compare_mappings(some_map, yet_another_map)
    False

    Comparisons to mappings where the "is" operator returns True will return.

    >>> compare_mappings(some_map, some_map)
    True
    >>> still_another_map = some_map
    >>> compare_mappings(some_map, still_another_map)
    True
    """
    if not (
        isinstance(map_, collections.abc.Mapping)
        and isinstance(other_map, collections.abc.Mapping)
    ):
        raise ValueError(
            "`map_` and `other_map` must both be dictionaries."
            f"\n But `map_` has type {type(map_)} and `other_map` "
            f"type {type(other_map)}."
        )
    # If the 2 mappings are the same they are equal
    if other_map is map_:
        return True
    # Unequal length mappings can't be equal so exit quickly
    elif len(map_) != len(other_map):
        return False
    if values:
        if ordered:
            match_ = all(
                kv1 == kv2 for kv1, kv2 in zip(map_.items(), other_map.items())
            )
        else:
            match_ = set(map_) == set(other_map) and set(map_.values()) == set(
                other_map.values()
            )
    else:
        if ordered:
            match_ = all(k1 == k2 for k1, k2 in zip(map_, other_map))
        else:
            match_ = set(map_) == set(other_map)
    return match_


def update_dict_at(
    input_dict: dict[Any, Any],
    new_dict: dict[Any, Any],
    at: Optional[int] = None,
    keep_new: bool = True,
) -> dict[Any, Any]:
    """Update a dictionary with a new dictionary at a given 'position'.

    Provides additional functionality above usual dictionary `update` method
    by allowing the "update" to occur at a particular position in the dictionary
    rather than the end.

    Unlike the usual dictionary update, the function returns the updated value.

    Parameters
    ----------
    input_dict : dict[Any, Any]
        The dictionary to "update".
    new_dict : dict[Any, Any]
        The dictionary to use to update `input_dict`.
    at : int | None, default=None
        The "position" the update should occur at.

        - If None, then this updates the values starting at the end of `input_dict`.
        - If a positive integer is provided then the update is performed at the
          index position determined from the start of `input_dict`. Positive `at`
          values greater than the length of `input_dict` cause the update to occur
          at the end of the `input_dict`.
        - If a negative integer is provided then the update is performed at the
          index position determined from the end of `input_dict`. Negative `at`
          values whose magnitude is greater than the length of `input_dict`
          cause the update to occur at the beginning of the `input_dict`.

    keep_new : bool, default=True
        Whether to keep the values from `new_dict` when updating keys that exist
        after the `at` position.

    Returns
    -------
    dict[Any, Any]
        The updated dictionary.

    Examples
    --------
    >>> from predictably_core.utils import update_dict_at
    >>> starting = {"a": 1, "b": 2, "c": 3, "d": 4}
    >>> new = {"e": 5, "f": 6}
    >>> new2 = {"g": 7, "a": -1}

    When the `at` parameter is not specified the update comes at the end like usual.

    >>> update_dict_at(starting, new)
    {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
    >>> update_dict_at(starting, new2)
    {'a': -1, 'b': 2, 'c': 3, 'd': 4, 'g': 7}

    When `at` is specified the update starts at that index.

    >>> update_dict_at(starting, new, at=2)
    {'a': 1, 'b': 2, 'e': 5, 'f': 6, 'c': 3, 'd': 4}

    By default the new values of keys that come after the `at` position are kept.

    >>> new3 = {"e": 5, "f": 6, "d":-1}
    >>> update_dict_at(starting, new3, at=2)
    {'a': 1, 'b': 2, 'e': 5, 'f': 6, 'd': -1, 'c': 3}

    Setting `keep_new` to False changes this behavior.

    >>> update_dict_at(starting, new3, at=2, keep_new=False)
    {'a': 1, 'b': 2, 'e': 5, 'f': 6, 'd': 4, 'c': 3}
    """
    if not (isinstance(input_dict, dict) and isinstance(new_dict, dict)):
        raise ValueError(
            "`input_dict` and `new_dict` must both be dictionaries."
            f"\n But `input_dict` has type {type(input_dict)} and `new_dict` "
            f"type {type(new_dict)}."
        )
    keys = tuple(input_dict)
    if at is None:
        at = len(input_dict)
    if not isinstance(at, int):
        raise ValueError(f"`at` must be an int or None, but found {at}.")
    # Step 1: Get keys up until "at" position
    output_ = {k: v for k, v in input_dict.items() if k in keys[:at]}
    # Step 2: Add new keys
    output_.update(new_dict)
    # Step 3: Add remaining values from original dict
    remaining = {
        k: v
        for k, v in input_dict.items()
        if k in keys[at:] and not (keep_new and k in new_dict)
    }
    output_.update(remaining)
    return output_
