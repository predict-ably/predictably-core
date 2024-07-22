"""Configurations for `predictably_core.core._pprint` tests.

This includes configurations used in multiple test files.
"""

from __future__ import annotations

__all__: list[str] = [
    "MockBaseObjectWithNestedParams",
    "MockBaseObjectWithParams",
    "MockBaseObjectWithVisualBlock",
    "MockBaseObjectWithoutParams",
]
__author__: list[str] = ["RNKuhns"]


class BaseObject:
    """Base class for mock objects used in testing."""

    def get_params(self, deep=True):
        """Mock method to get parameters. Should be overridden by subclasses."""
        return {}


class MockObject(BaseObject):
    """Mock object for testing with default and non-default parameters."""

    def __init__(self, param1=1, param2=2, param3=None):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

    def get_params(self, deep=False):
        """Override method to return the object's parameters."""
        return {"param1": self.param1, "param2": self.param2, "param3": self.param3}


class MockBaseObjectWithVisualBlock:
    """Mock class implementing visual block.

    Used in tests to verify classes that implement _sk_visual_block_
    have their implementation used.
    """

    def _sk_visual_block_(self):
        """Test implementation of _sk_visual_block_.

        Used to test usage of classes with their own implementation.
        """
        return "mock_visual_block"


class MockBaseObjectWithParams:
    """Mock class for testing classes that implement get_params.

    Designed to test cases where there aren't nested objects.
    """

    def get_params(self):
        """Mock implementation of get_params.

        Used for testing purposes.
        """
        return {"param1": "value1", "param2": "value2"}


class MockBaseObjectWithNestedParams:
    """Mock class for testing classes with nested based objects.

    This is used to test pretty-printing information for classes implementing
    `get_params` with nested objects.
    """

    def get_params(self):
        """Mock implementation of get_params.

        Used for testing purposes.
        """
        return {"param1": MockBaseObjectWithParams(), "param2": "value2"}


class MockBaseObjectWithoutParams:
    """Mock class for testing param-less class."""

    pass
