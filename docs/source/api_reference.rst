.. _api_ref:

===
API
===

This is the API reference for ``predictably_core``. For additional details on using
the functionality provided by the API see the :ref:`user_guide`. See the
:ref:`glossary` for common terms used throughout the package.

.. automodule:: predictably_core
    :no-members:
    :no-inherited-members:

Configure ``predictably_core``
==============================

.. automodule:: predictably_core.config
    :no-members:
    :no-inherited-members:

.. currentmodule:: predictably_core.config

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: function.rst

    get_config
    set_config
    reset_config
    config_context

.. _obj_core:

Core
====

.. automodule:: predictably_core.core
    :no-members:
    :no-inherited-members:

.. currentmodule:: predictably_core.core

Base Classes
------------

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: class.rst

    BaseObject
    BaseEstimator

Tools for Working with Base Classes
-----------------------------------

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: function.rst

    clone

.. _obj_validation:

Validation
==========

.. automodule:: predictably_core.validate
    :no-members:
    :no-inherited-members:

.. currentmodule:: predictably_core.validate

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: function.rst

    check_mapping
    check_path
    check_sequence
    check_type
    is_iterable
    is_mapping
    is_sequence

Utilities
=========

.. automodule:: predictably_core.utils
    :no-members:
    :no-inherited-members:

.. currentmodule:: predictably_core.utils

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: function.rst

    compare_mappings
    format_sequence_to_str
    remove_type_text
    scalar_to_sequence
    single_element_sequence_to_scalar
    update_dict_at
