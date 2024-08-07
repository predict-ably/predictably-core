#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
# Many elements of this code were developed in scikit-learn. These elements
# are copyrighted by the scikit-learn developers, BSD-3-Clause License. For
# conditions see https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
"""Implement the ability to clone BaseObjects.

This logic is designed to also work with scikit-learn and related classes.
"""

from __future__ import annotations

import collections
import copy
import inspect
import sys
from typing import Sequence

if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias

from predictably_core.core._base import BaseObject

__author__: list[str] = ["RNKuhns"]
__all__: list[str] = ["_clone_parametrized", "clone"]

CLONABLE_OBJECTS: TypeAlias = (
    BaseObject | Sequence[BaseObject] | set[BaseObject] | dict[str, BaseObject]
)


def clone(obj: CLONABLE_OBJECTS, *, safe: bool = True):
    """Construct a new unfitted object with the same parameters.

    Clone does a deep copy of the object without actually copying attached data.
    It returns a new object with the same parameters that hasn't had additional
    state changes made.

    The clone is dispatched to the object if it implements a sklearn or predictably
    clone dunder (i.e., `BaseObject.__sklearn_clone__` or
    `BaseObject.__predictably_clone__`).

    Parameters
    ----------
    obj : object | sequence[object] | set[object] | dict[str, object]
        The object(s) to be cloned.
    safe : bool, default=True
        For objects that aren't BaseObjects, determines Whether to perform
        "safe" copy or use deepcopy.

        - If safe is False, clone will use deepcopy for objects that don't follow
          the BaseObject specification.
        - If safe is True, then an error is raised.

    Returns
    -------
    object
        The deep copy of the input.

    Notes
    -----
    When BaseObject has a `random_state` parameter, the behavior differs depending
    on the value set on the `random_state` parameter. If the `random_state`
    parameter is an integer an *exact clone* is returned -- the clone and the object
    will use the same exact random state. Otherwise, a *statistical clone* is
    returned -- the clone might return different results when using its random state.

    Examples
    --------
    >>> from predictably_core.core import clone, BaseEstimator
    >>> class YourEstimator(BaseEstimator):
    ...
    ...     def fit(self, x, y):
    ...         self._is_fitted = True
    ...         return self
    >>> X = [[-1, 0], [0, 1], [0, -1], [1, 0]]
    >>> y = [0, 0, 1, 1]
    >>> estimator = YourEstimator()
    >>> estimator.is_fitted
    False
    >>> estimator.fit(X, y)
    YourEstimator()
    >>> cloned_estimator = clone(estimator)
    >>> estimator.is_fitted
    True
    >>> cloned_estimator.is_fitted
    False
    >>> estimator is cloned_estimator
    False
    """
    obj_type = type(obj)
    if obj_type in (tuple, list, set, frozenset) or (
        isinstance(obj, collections.abc.Sequence) and not isinstance(obj, str)
    ):
        return obj_type(clone(o) for o in obj)
    elif obj_type is dict:
        return {k: clone(v, safe=safe) for k, v in obj.items()}

    is_class = inspect.isclass(obj)
    if hasattr(obj, "__predictably_clone__") and not is_class:
        return obj.__predictably_clone__()
    elif hasattr(obj, "__sklearn_clone__") and not is_class:
        return obj.__sklearn_clone__()
    return _clone_parametrized(obj, safe=safe)


def _clone_parametrized(obj: CLONABLE_OBJECTS, *, safe: bool = True):
    """Implement default logic to clone "parametrized" BaseObjects.

    Parametrized objects include BaseObjects and related classes that follow
    the specification, including scikit-learn BaseEstimators.

    Parameters
    ----------
    obj : object | sequence[object] | set[object] | dict[str, object]
        The object(s) to be cloned.
    safe : bool, default=True
        For objects that aren't BaseObjects, determines Whether to perform
        "safe" copy or use deepcopy.

        - If safe is False, clone will use deepcopy for objects that don't follow
          the BaseObject specification.
        - If safe is True, then an error is raised.

    Returns
    -------
    object
        The deep copy of the input.
    """
    obj_type = type(obj)
    if obj_type is dict:
        return {k: _clone_parametrized(v, safe=safe) for k, v in obj.items()}
    elif obj_type in (list, tuple, set, frozenset):
        return obj_type([_clone_parametrized(e, safe=safe) for e in obj])
    elif not hasattr(obj, "get_params") or isinstance(obj, type):
        if not safe:
            return copy.deepcopy(obj)
        else:
            if isinstance(obj, type):
                raise TypeError(
                    "Cannot clone object. "
                    + "You should provide an instance instead of a class."
                )
            else:
                raise TypeError(
                    f"Cannot clone object {obj!r} of type {type(obj)}: "
                    "it does not seem to implement a 'get_params' method."
                )

    klass = obj.__class__
    new_object_params = obj.get_params(deep=False)
    for name, param in new_object_params.items():
        new_object_params[name] = clone(param, safe=False)

    new_object = klass(**new_object_params)
    # Handle metadata request/routing
    if hasattr(obj, "_metadata_request"):
        new_object._metadata_request = copy.deepcopy(obj._metadata_request)

    params_set = new_object.get_params(deep=False)

    # quick sanity check of the parameters of the clone
    unequal_params = [
        name
        for name in new_object_params
        if new_object_params[name] is not params_set[name]
    ]
    if unequal_params:
        raise RuntimeError(
            f"Cannot clone object {obj!r}, as the constructor "
            f"either does not set or modifies parameter {name}."
        )

    # _sklearn_output_config is used by `set_output` to configure the output
    # container of an estimator in scikit-learn classes.
    if hasattr(obj, "_sklearn_output_config"):
        new_object._sklearn_output_config = copy.deepcopy(obj._sklearn_output_config)

    # Handles cloning of predictably tags and configs
    for attr_ in ("_tags", "_tags_dynamic", "_config", "_config_dynamic"):
        if hasattr(obj, attr_):
            setattr(new_object, attr_, getattr(obj, attr_))
    return new_object
