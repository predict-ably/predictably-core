#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
from __future__ import annotations

import html
import io

from predictably_core.core._pprint._object_html_repr import _write_label_html

__author__: list[str] = ["RNKuhns"]


def test_write_label_html_no_name_details():
    """
    Test _write_label_html with no name details.

    This test verifies that the function correctly outputs the HTML structure
    when no name details are provided.

    Asserts:
        The generated HTML string matches the expected output without name details.
    """
    out = io.StringIO()
    _write_label_html(out, "TestName", None)
    result = out.getvalue()
    expected = "<div class='sk-label-container'>"
    expected += '<div class="sk-label sk-toggleable">'
    expected += "<label>TestName</label></div></div>"
    assert result == expected


def test_write_label_html_with_name_details_checked():
    """
    Test _write_label_html with name details and checked.

    This test verifies that the function correctly outputs the HTML structure
    when name details are provided and the checkbox is checked.

    Asserts:
        The generated HTML string contains the expected elements and attributes.
    """
    out = io.StringIO()
    name = "TestName"
    name_details = "Details"
    _write_label_html(out, name, name_details, checked=True)
    result = out.getvalue()

    # Since est_id is dynamically generated in func, we need to adjust the assertion to
    # account for it. So we check things that should be in result not the exact result
    assert "class='sk-label-container'" in result
    assert 'class="sk-label sk-toggleable"' in result
    assert 'class="sk-toggleable__control sk-hidden--visually"' in result
    assert 'type="checkbox" checked' in result
    assert "class='sk-toggleable__label sk-toggleable__label-arrow'" in result
    assert "<label for=" in result
    assert 'class="sk-toggleable__content"' in result
    assert f"<pre>{html.escape(str(name_details))}</pre>" in result


def test_write_label_html_with_name_details_not_checked():
    """
    Test _write_label_html with name details and not checked.

    This test verifies that the function correctly outputs the HTML structure
    when name details are provided and the checkbox is not checked.

    Asserts:
        The generated HTML string contains the expected elements and attributes.
    """
    out = io.StringIO()
    name = "TestName"
    name_details = "Details"
    _write_label_html(out, name, name_details, checked=False)
    result = out.getvalue()

    # Since est_id is dynamically generated in func, we need to adjust the assertion to
    # account for it. So we check things that should be in result not the exact result
    assert "class='sk-label-container'" in result
    assert 'class="sk-label sk-toggleable"' in result
    assert 'class="sk-toggleable__control sk-hidden--visually"' in result
    assert 'type="checkbox"' in result
    assert "class='sk-toggleable__label sk-toggleable__label-arrow'" in result
    assert "<label for=" in result
    assert 'class="sk-toggleable__content"' in result
    assert f"<pre>{html.escape(str(name_details))}</pre>" in result

    # Verify that checkbox not checked
    assert 'type="checkbox" checked' not in result


def test_write_label_html_custom_classes():
    """
    Test _write_label_html with custom classes.

    This test verifies that the function correctly outputs the HTML structure
    when custom outer and inner classes are provided.

    Asserts:
        The generated HTML string contains the custom classes and expected elements.
    """
    out = io.StringIO()
    name = "TestName"
    name_details = "Details"
    outer_class = "custom-outer-class"
    inner_class = "custom-inner-class"
    _write_label_html(out, name, name_details, outer_class, inner_class)
    result = out.getvalue()

    # Since est_id is dynamically generated in func, we need to adjust the assertion to
    # account for it. So we check things that should be in result not the exact result
    assert f"class={outer_class!r}" in result
    assert f'class="{inner_class} sk-toggleable"' in result
    assert 'class="sk-toggleable__control sk-hidden--visually"' in result
    assert 'type="checkbox"' in result
    assert "<label for=" in result
    assert "class='sk-toggleable__label sk-toggleable__label-arrow'" in result
    assert '<div class="sk-toggleable__content"><pre>' in result
    assert f"<pre>{html.escape(str(name_details))}</pre>" in result
