#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
from __future__ import annotations

import pytest

from predictably_core.core._pprint._object_html_repr import _VisualBlock

__author__: list[str] = ["RNKuhns"]


@pytest.fixture
def single_visual_block():
    return _VisualBlock("single", "obj1", names="name1", name_details="details1")


@pytest.fixture
def parallel_visual_block():
    return _VisualBlock(
        "parallel",
        ["obj1", "obj2"],
        names=["name1", "name2"],
        name_details=["details1", "details2"],
    )


@pytest.fixture
def serial_visual_block():
    return _VisualBlock(
        "serial",
        ["obj1", "obj2"],
        names=["name1", "name2"],
        name_details=["details1", "details2"],
    )


def test_visual_block_initialization_single(single_visual_block):
    assert single_visual_block.kind == "single"
    assert single_visual_block.objs == "obj1"
    assert single_visual_block.names == "name1"
    assert single_visual_block.name_details == "details1"
    assert single_visual_block.dash_wrapped is True


def test_visual_block_initialization_parallel(parallel_visual_block):
    assert parallel_visual_block.kind == "parallel"
    assert parallel_visual_block.objs == ["obj1", "obj2"]
    assert parallel_visual_block.names == ["name1", "name2"]
    assert parallel_visual_block.name_details == ["details1", "details2"]
    assert parallel_visual_block.dash_wrapped is True


def test_visual_block_initialization_serial(serial_visual_block):
    assert serial_visual_block.kind == "serial"
    assert serial_visual_block.objs == ["obj1", "obj2"]
    assert serial_visual_block.names == ["name1", "name2"]
    assert serial_visual_block.name_details == ["details1", "details2"]
    assert serial_visual_block.dash_wrapped is True


def test_visual_block_dash_wrapped_default():
    visual_block = _VisualBlock(
        "serial",
        ["obj1", "obj2"],
        names=["name1", "name2"],
        name_details=["details1", "details2"],
    )
    assert visual_block.dash_wrapped is True


def test_visual_block_dash_wrapped_false():
    visual_block = _VisualBlock(
        "serial",
        ["obj1", "obj2"],
        names=["name1", "name2"],
        name_details=["details1", "details2"],
        dash_wrapped=False,
    )
    assert visual_block.dash_wrapped is False


def test_sk_visual_block_method(
    single_visual_block, parallel_visual_block, serial_visual_block
):
    assert single_visual_block._sk_visual_block_() is single_visual_block
    assert parallel_visual_block._sk_visual_block_() is parallel_visual_block
    assert serial_visual_block._sk_visual_block_() is serial_visual_block


def test_sk_visual_block_serial_names_none():
    visual_block = _VisualBlock(
        "serial",
        ["obj1", "obj2"],
        names=None,
        name_details=None,
    )
    assert visual_block.names == (None,) * len(visual_block.objs)
    assert visual_block.name_details == (None,) * len(visual_block.objs)


def test_sk_visual_block_parallel_names_none():
    visual_block = _VisualBlock(
        "parallel",
        ["obj1", "obj2"],
        names=None,
        name_details=None,
    )
    assert visual_block.names == (None,) * len(visual_block.objs)
    assert visual_block.name_details == (None,) * len(visual_block.objs)
