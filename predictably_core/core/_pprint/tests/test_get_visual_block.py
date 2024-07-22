#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
from __future__ import annotations

from predictably_core.core._pprint._object_html_repr import (
    _get_visual_block,
    _VisualBlock,
)

__author__: list[str] = ["RNKuhns"]


class MockBaseObjectWithVisualBlock:
    def _sk_visual_block_(self):
        return "mock_visual_block"


class MockBaseObjectWithParams:
    def get_params(self):
        return {"param1": "value1", "param2": "value2"}


class MockBaseObjectWithNestedParams:
    def get_params(self):
        return {"param1": MockBaseObjectWithParams(), "param2": "value2"}


class MockBaseObjectWithoutParams:
    pass


def test_get_visual_block_with_visual_block():
    """
    Test _get_visual_block with an object that has _sk_visual_block_ attribute.

    This test verifies that the function returns the result of the object's
    _sk_visual_block_ method when the attribute exists.

    Asserts:
        The function returns the expected visual block from the
        _sk_visual_block_ method.
    """
    base_object = MockBaseObjectWithVisualBlock()
    result = _get_visual_block(base_object)
    assert result == "mock_visual_block"


def test_get_visual_block_with_string():
    """
    Test _get_visual_block with a string input.

    This test verifies that the function correctly handles string inputs and
    returns an appropriate _VisualBlock.

    Asserts:
        The function returns a _VisualBlock with the correct attributes.
    """
    base_object = "test_string"
    result = _get_visual_block(base_object)
    assert isinstance(result, _VisualBlock)
    assert result.kind == "single"
    assert result.objs == "test_string"
    assert result.names == base_object
    assert result.name_details == base_object


def test_get_visual_block_with_none():
    """
    Test _get_visual_block with None input.

    This test verifies that the function correctly handles None inputs and
    returns an appropriate _VisualBlock.

    Asserts:
        The function returns a _VisualBlock with 'None' as names and name_details.
    """
    base_object = None
    result = _get_visual_block(base_object)
    assert isinstance(result, _VisualBlock)
    assert result.kind == "single"
    assert result.objs is None
    assert result.names == "None"
    assert result.name_details == "None"


def test_get_visual_block_with_meta_object():
    """
    Test _get_visual_block with a meta object.

    This test verifies that the function correctly identifies and handles
    meta objects by returning a _VisualBlock with 'parallel' block type.

    Asserts:
        The function returns a _VisualBlock with the correct block type and content.
    """
    base_object = MockBaseObjectWithNestedParams()
    result = _get_visual_block(base_object)
    assert isinstance(result, _VisualBlock)
    assert result.kind == "parallel"
    assert len(result.objs) == 1
    assert isinstance(result.objs[0], MockBaseObjectWithParams)


def test_get_visual_block_with_regular_object():
    """
    Test _get_visual_block with a regular object.

    This test verifies that the function correctly handles regular objects and
    returns an appropriate _VisualBlock.

    Asserts:
        The function returns a _VisualBlock with the correct attributes.
    """
    base_object = MockBaseObjectWithoutParams()
    result = _get_visual_block(base_object)
    assert isinstance(result, _VisualBlock)
    assert result.kind == "single"
    assert result.objs == base_object
    assert result.names == base_object.__class__.__name__
    assert result.name_details == str(base_object)
