#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
from __future__ import annotations

import io

from predictably_core.core._pprint._pprint import _BaseObjectPrettyPrinter, _safe_repr
from predictably_core.core._pprint.tests.conftest import (
    MockObject,
    MockObjectManyParams,
)

__author__: list[str] = ["RNKuhns"]


def test_base_object_pretty_printer_single_line():
    """
    Test pretty printing of a BaseObject on a single line.

    This test verifies that a BaseObject is correctly formatted on a single line
    when it has a small number of parameters.

    Asserts:
        The output stream contains the expected formatted string.
    """
    obj = MockObject(param1=10, param2=20)
    stream = io.StringIO()
    printer = _BaseObjectPrettyPrinter(stream=stream)

    printer.pprint(obj)
    output = stream.getvalue()
    expected = "MockObject(param1=10, param2=20)"
    assert output.strip() == expected

    obj = MockObject()  # unchanged from defaults
    stream = io.StringIO()
    printer = _BaseObjectPrettyPrinter(stream=stream, changed_only=False)

    printer.pprint(obj)
    output = stream.getvalue()
    expected = "MockObject(param1=1, param2=2, param3=None)"
    assert output.strip() == expected


def test_base_object_pretty_printer_multiline():
    """
    Test pretty printing of a BaseObject that results in multiline output.

    This test verifies that a BaseObject is formatted over multiple lines
    when it has a larger number of parameters.

    Asserts:
        The output stream contains the expected formatted string with multiple lines.
    """
    obj = MockObjectManyParams(
        param1=11,
        param2=22,
        param3=33,
        param4=44,
        param5=55,
        param6=500,
        param7=MockObject(),
    )
    out = io.StringIO()
    printer = _BaseObjectPrettyPrinter(
        indent_at_name=False, n_max_elements_to_show=2, stream=out
    )
    printer.pprint(obj)
    output = out.getvalue()

    expected_start = "MockObjectManyParams(('param1', 11),\n ('param2', 22), ...)\n"
    assert output.startswith(expected_start)
    assert output.strip().endswith(")")


def test_safe_repr_dict():
    """
    Test safe representation of a dictionary.

    This test verifies that the _safe_repr function correctly works with nested
    BaseObjects like objects.

    Asserts:
        The function output includes the expected dictionary representation
        with ellipsis.
    """
    obj = MockObject(param1=2, param2=3, param3=MockObject(param1=MockObject()))
    context = {}
    repr_str, _, _ = _safe_repr(obj, context, maxlevels=2, level=0, changed_only=True)
    expected = "MockObject(param1=2, param2=3, param3=MockObject(param1={...}))"
    assert repr_str == expected

    repr_str, _, _ = _safe_repr(obj, context, maxlevels=2, level=0, changed_only=False)
    param3 = "param3=MockObject(param1={...}, param2=2, param3=None)"
    expected = f"MockObject(param1=2, param2=3, {param3})"
    assert repr_str == expected


def test_safe_repr_base_object_changed_params():
    """
    Test safe representation of a BaseObject.

    This test verifies that the _safe_repr function formats a BaseObject correctly,
    including handling of changed parameters.

    Asserts:
        The function output contains the expected representation of the BaseObject.
    """
    obj = MockObject(param1=10, param3="changed")
    context = {}
    repr_str, _, _ = _safe_repr(obj, context, maxlevels=2, level=0, changed_only=True)
    expected = "MockObject(param1=10, param3='changed')"
    assert repr_str == expected

    context = {}
    repr_str, _, _ = _safe_repr(obj, context, maxlevels=2, level=0, changed_only=False)
    expected = "MockObject(param1=10, param2=2, param3='changed')"
    assert repr_str == expected
