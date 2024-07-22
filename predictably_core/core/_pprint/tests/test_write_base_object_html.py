#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
from __future__ import annotations

import io

import pytest

# Import the functions to be tested
import predictably_core.core._pprint._object_html_repr as ohr
from predictably_core.core._pprint._object_html_repr import (
    _VisualBlock,
    _write_base_object_html,
)
from predictably_core.core._pprint.tests.conftest import (
    MockBaseObjectWithNestedParams,
)

__author__: list[str] = ["RNKuhns"]


# Mock the functions that _write_base_object_html depends on
@pytest.fixture
def mock_get_visual_block(monkeypatch):
    def mock_return(value):
        if isinstance(value, list):
            return _VisualBlock(
                "parallel",
                value,
                names=["Object1", "Object2"],
                name_details=["Details1", "Details2"],
            )
        elif isinstance(value, tuple):
            return _VisualBlock(
                "serial",
                value,
                names=["Object1", "Object2"],
                name_details=["Details1", "Details2"],
            )
        elif isinstance(value, str):
            return _VisualBlock("single", value, names=value, name_details=value)
        elif value is None:
            return _VisualBlock("single", None, names="None", name_details="None")
        elif isinstance(value, MockBaseObjectWithNestedParams):
            return _VisualBlock("parallel", [value.get_params()["param1"]], names=None)
        return _VisualBlock(
            "single", value, names=value.__class__.__name__, name_details=str(value)
        )

    monkeypatch.setattr(ohr, "_get_visual_block", mock_return)


def test_write_base_object_html_single(mock_get_visual_block):
    """
    Test _write_base_object_html with a single base object.

    This test verifies that the function correctly handles single base objects
    and writes the appropriate HTML.

    Asserts:
        The correct HTML is written for a single base object.
    """
    out = io.StringIO()
    base_object = "test_object"
    _write_base_object_html(
        out, base_object, "Label", "Label Details", first_call=False
    )
    result = out.getvalue()
    assert "class='sk-item'" in result
    assert 'class="sk-estimator sk-toggleable"' in result


def test_write_base_object_html_parallel(mock_get_visual_block):
    """
    Test _write_base_object_html with parallel base objects.

    This test verifies that the function correctly handles parallel base objects
    and writes the appropriate HTML.

    Asserts:
        The correct HTML is written for parallel base objects.
    """
    out = io.StringIO()
    base_object = ["Object1", "Object2"]
    _write_base_object_html(out, base_object, "Label", "Label Details", first_call=True)
    result = out.getvalue()
    assert 'class="sk-parallel"' in result
    assert 'class="sk-parallel-item"' in result


def test_write_base_object_html_2(mock_get_visual_block):
    """
    Test _write_base_object_html with nested base objects.

    This test verifies that the function correctly handles nestesd base objects
    and writes the appropriate HTML.

    Asserts:
        The correct HTML is written for nested base objects.
    """
    out = io.StringIO()
    _write_base_object_html(out, MockBaseObjectWithNestedParams(), "Label", "Label")
    result = out.getvalue()
    assert 'class="sk-parallel"' in result
    assert 'class="sk-parallel-item"' in result


def test_write_base_object_html_serial(mock_get_visual_block):
    """
    Test _write_base_object_html with serial base objects.

    This test verifies that the function correctly handles serial base objects
    and writes the appropriate HTML.

    Asserts:
        The correct HTML is written for serial base objects.
    """
    out = io.StringIO()
    base_object = ("Object1", "Object2")
    _write_base_object_html(out, base_object, "Label", "Label Details", first_call=True)
    result = out.getvalue()
    assert 'class="sk-serial"' in result


def test_write_base_object_html_none(mock_get_visual_block):
    """
    Test _write_base_object_html with None base object.

    This test verifies that the function correctly handles None base objects
    and writes the appropriate HTML.

    Asserts:
        The correct HTML is written for None base objects.
    """
    out = io.StringIO()
    base_object = None
    _write_base_object_html(out, base_object, "Label", "Label Details", first_call=True)
    result = out.getvalue()
    assert "class='sk-item'" in result


def test_write_base_object_html_first_call(mock_get_visual_block):
    """
    Test _write_base_object_html with the first_call parameter set to True.

    This test verifies that the function correctly handles the first call
    and writes the appropriate HTML.

    Asserts:
        The correct HTML is written when first_call is True.
    """
    out = io.StringIO()
    base_object = "test_object"
    _write_base_object_html(out, base_object, "Label", "Label Details", first_call=True)
    result = out.getvalue()
    assert 'type="checkbox" checked' in result, result
    assert "class='sk-item'" in result, result
    assert 'class="sk-estimator sk-toggleable"' in result, result
