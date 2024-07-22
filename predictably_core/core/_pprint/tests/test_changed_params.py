#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
from __future__ import annotations

import numpy as np

from predictably_core.core._pprint._pprint import _changed_params
from predictably_core.core._pprint.tests.conftest import BaseObject, MockObject
from predictably_core.validate._types import _is_scalar_nan

__author__: list[str] = ["RNKuhns"]


def test_changed_params_no_changes():
    """
    Test _changed_params with an object having only default parameters.

    This test verifies that the function returns an empty dictionary when
    the base object has only default parameter values.

    Asserts:
        The function returns an empty dictionary.
    """
    obj = MockObject()
    result = _changed_params(obj)
    assert result == {}


def test_changed_params_some_changes():
    """
    Test _changed_params with an object having some non-default parameters.

    This test verifies that the function correctly identifies and returns
    the non-default parameter values.

    Asserts:
        The function returns a dictionary with the changed parameters.
    """
    obj = MockObject(param1=10, param3="changed")
    result = _changed_params(obj)
    expected = {"param1": 10, "param3": "changed"}
    assert result == expected


def test_changed_params_all_changes():
    """
    Test _changed_params with an object having all non-default parameters.

    This test verifies that the function correctly identifies and returns
    all the non-default parameter values.

    Asserts:
        The function returns a dictionary with all the changed parameters.
    """
    obj = MockObject(param1=10, param2=20, param3="changed")
    result = _changed_params(obj)
    expected = {"param1": 10, "param2": 20, "param3": "changed"}
    assert result == expected


def test_changed_params_no_default():
    """
    Test _changed_params with a parameter that has no default value.

    This test verifies that the function correctly identifies and returns
    parameters with no default value.

    Asserts:
        The function returns a dictionary with the parameter that has no default value.
    """

    class NoDefaultParamObject(BaseObject):
        def __init__(self, param1):
            self.param1 = param1

        def get_params(self, deep=False):
            return {"param1": self.param1}

    obj = NoDefaultParamObject(param1=10)
    result = _changed_params(obj)
    expected = {"param1": 10}
    assert result == expected


def test_changed_params_nan_values():
    """
    Test _changed_params with parameters having NaN values.

    This test verifies that the function correctly identifies and returns
    parameters with NaN values as non-default.

    Asserts:
        The function returns a dictionary with the parameters having NaN values.
    """
    obj = MockObject(param1=np.nan)
    result = _changed_params(obj)
    expected = {"param1": np.nan}
    assert all(k in result and _is_scalar_nan(result[k]) for k in expected)
