.. _full_install:

============
Installation
============

``predictably_core`` currently supports:

- environments with python version 3.8, 3.9, 3.10, 3.11 or 3.12
- Common linux, Mac OS, and Windows operating systems

Checkout the full list of pre-compiled wheels on `PyPI`_.

Install a Release from PyPi or conda-forge
==========================================

Most users will be interested in installing a released version of ``predictably_core``.
These can be installed from PyPi using ``pip`` or using ``conda`` to install the
package from the conda-forge channel by using one of the code snippets below.

.. tab-set::

    .. tab-item:: PyPi

        .. code-block:: shell

           pip install -U predictably-core

    .. tab-item:: Conda

        .. note::

            We are still working on creating releases of ``predictably_core``

Install the Development Version from Github
===========================================

You can always use ``pip`` to install the latest version of ``predictably_core`` with
any new features and bug-fixes directly from the `Github repository`_:

.. code-block:: shell

   pip uninstall predictably-core
   pip install -U git+https://github.com/predictably/predictably-core.git@main


Developer Installation
======================

If you plan to contribute to ``predictably_core`` you'll want to follow our
:ref:`development installation instructions <dev_install>` that are included in
our :ref:`development guide <dev_guide>`.

.. _Github repository: https://github.com/predict-ably/predictably-core
.. _PyPi: https://pypi.org/simple/predictably-core/
