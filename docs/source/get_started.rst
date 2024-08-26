.. _getting_started:

===========
Get Started
===========

The following information is designed to get users up and running with
``predictably_core`` quickly. Links to additional details are provided
in each of the subsections below.

Installation
============

``predictably_core`` currently supports:

- environments with python version 3.8, 3.9, 3.10, 3.11 or 3.12
- Common linux, Mac OS, and Windows operating systems

Users can install ``predictably_core`` from PyPi using ``pip`` or using ``conda``
to install the package from the conda-forge channel by using one of the code
snippets below.

.. tab-set::

    .. tab-item:: PyPi

        .. code-block:: bash

           pip install -U predictably-core

    .. tab-item:: Conda

        .. note::

            We are still working on creating releases of ``predictably_core``
            on ``conda``. If you would like to help, please open a pull request.

For additional details see our :ref:`full installation guide <full_install>`.

Key Concepts
============

``predictably_core``'s goal is to provide a :term:`framework` for building
packages that follow `scikit-learn`_, and `sktime`_ style design patterns.

It takes inspiration from `skbase`_, but in some cases has made different design
choices.

``predictably_core`` provides base classes (:class:`BaseObject`
and :class:`BaseEstimator`) with interfaces for:

- `scikit-learn`_ style parameter getting and setting
- using :term:`tags <tag>` to record characteristics of the class that can
  be used to alter the classes code or how it interacts with other functionality

``predictably_core`` also contains additional functionality to make it easy to
:term:`Python packages <Python package>` that provide build :term:`toolboxes <toolbox>`
on top of the ``predictably_core`` design interface. This functionality includes:

- retrieving information on ``BaseObject``-s
- performing type validations, including validating ``BaseObject``-s or
  collections of ``BaseObject``-s

Quickstart
==========
The code snippets below are designed to introduce ``predictably_core``'s
functionality. For more detailed information see the :ref:`user_guide` and
:ref:`api_ref` in ``predictably_core``'s :ref:`user_documentation`.

Create a New Class Built on Top of ``BaseObject``
-------------------------------------------------

.. code-block:: pycon

    >>> from predictably_core.core import BaseObject
    >>> class SomeClass(BaseObject):
    ...     """Some class docstring."""
    ...     def __init__(self, some_param: int = 7):
    ...         self.some_param = some_param
    ...
    >>> some_class = SomeClass()
    >>> some_class
    SomeClass(some_param=7)
    >>> some_class.get_params()
    {'some_param': 7}


Define a New Class Using ``BaseObject`` and ``attrs``
-----------------------------------------------------

.. blacken-docs:off
.. code-block:: pycon

    >>> import attrs
    >>> from predictably_core.core import BaseObject
    # To use predictably_core's repr functionality make sure to disable attrs
    # standard repr functionality
    >>> @attrs.define(kw_only=True, repr=False)
    >>> class SomeClass(BaseObject):
    ...     """Some class docstring."""
    ...     some_param: int = 7
    >>> some_class = SomeClass()
    >>> some_class
    SomeClass(some_param=7)
    >>> some_class.get_params()
    {'some_param': 7}
.. blacken-docs:on

.. _scikit-learn: https://scikit-learn.org/stable/index.html
.. _sktime: https://www.sktime.net/en/stable/index.html
.. _skbase: https://skbase.readthedocs.io/en/latest/index.html
