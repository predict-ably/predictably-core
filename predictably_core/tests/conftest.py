"""Common functionality for skbase unit tests."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, ClassVar

from predictably_core.core._base import BaseEstimator, BaseObject

__all__: list[str] = ["Child", "Parent"]
__author__: list[str] = ["RNKuhns"]

PREDICTABLY_BASE_CLASSES = (BaseObject, BaseEstimator)


# Fixture class for testing tag system
class Parent(BaseObject):
    """Parent class to test BaseObject's usage."""

    _tags: ClassVar[dict[str, Any]] = {"A": "1", "B": 2, "C": 1234, "3": "D"}

    def __init__(self, a: str = "something", b: int = 7, c: int | None = None) -> None:
        self.a = a
        self.b = b
        self.c = c

    def some_method(self):
        """To be implemented by child class."""
        pass


# Fixture class for testing tag system, child overrides tags
class Child(Parent):
    """Child class that is child of FixtureClassParent."""

    _tags: ClassVar[dict[str, Any]] = {"A": 42, "3": "E"}
    __author__: ClassVar[list[str]] = ["Someone", "Someone Else"]

    def some_method(self):
        """Child class' implementation."""
        pass

    def some_other_method(self):
        """To be implemented in the child class."""
        pass


class CompositionDummy(BaseObject):
    """Potentially composite object, for testing."""

    def __init__(self, foo: Any = 11, bar: Any = 84) -> None:
        self.foo = foo
        self.bar = bar
        self.foo_ = deepcopy(foo)

    @classmethod
    def get_test_params(cls, parameter_set="default"):
        """Return testing parameter settings for the estimator.

        Parameters
        ----------
        parameter_set : str, default="default"
            Name of the set of test parameters to return, for use in tests. If no
            special parameters are defined for a value, will return `"default"` set.

        Returns
        -------
        params : dict or list of dict, default = {}
            Parameters to create testing instances of the class
            Each dict are parameters to construct an "interesting" test instance, i.e.,
            `MyClass(**params)` or `MyClass(**params[i])` creates a valid test instance.
            `create_test_instance` uses the first (or only) dictionary in `params`
        """
        params1 = {"foo": 42}
        params2 = {"foo": CompositionDummy(126)}
        return [params1, params2]
