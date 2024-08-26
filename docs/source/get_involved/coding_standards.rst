.. _code_standards:

================
Coding standards
================

.. _code_style:

Coding style
============

``predictably`` follows standard Python code style conventions, including the
`PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ coding guidelines.

Code formatting and linting
---------------------------

``predictably`` uses a variety of tools to enforce code formatting conventions,
including:

* `black <https://black.readthedocs.io/en/stable/>`_ with configuration in
  ``pyproject.toml``
* `flake8 <https://flake8.pycqa.org/en/latest/>`__ with configurations in ``setup.cfg``
* `isort <https://pycqa.github.io/isort/>`_ with configuration in ``pyproject.toml``
* `pydocstyle <http://www.pydocstyle.org/en/stable/>`_ with configuration in
  ``pyproject.toml``
* `doc8 <https://github.com/PyCQA/doc8>`_ with configuration in ``pyproject.toml``
* `bandit <https://bandit.readthedocs.io/en/latest/>`_ with configuration in
  ``pyproject.toml``
* ``numpydoc`` to enforce numpy `docstring standard
  <https://numpydoc.readthedocs.io/en/latest/index.html>`_ ,
* ``predictably`` specific conventions described in our
  :ref:`documentation conventions <developer_guide_documentation>`.

All of these conventions (except for predictably's specific documentation conventions
are automatically run on Pull Requests using ``predictably``'s :ref:`ci` workflows.

Setting up local code quality checks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When starting your development in your own local clone of
the repository, you should enable ``pre-commit`` locally so the code formatting
and linting tools are run prior to committing your code locally.

Using pre-commit locally
^^^^^^^^^^^^^^^^^^^^^^^^

To set up pre-commit, follow ``predictably``'s
:ref:`development installation <dev_install>` instructions. Then navigate to
the directory of your local clone of your forked repository and run
:code:`pre-commit install`.

Once installed, pre-commit will automatically run all ``predictably`` code
quality checks on the files you changed whenever you make a new commit.

You can find all of ``predictably``'s pre-commit configurations in
`.pre-commit-config.yaml
<https://github.com/predict-ably/predictably/blob/main/.pre-commit-config.yaml>`_.

.. note::

   To exclude a line of code from being checked by flake8, you can add a ``# noqa``
   (no quality assurance) comment at the end of that line. However, this is
   generally discouraged unless no other options for passing the code quality
   checking are possible. In this case, provide a comment indicating the
   reasoning above the line.

   There are similar ways to exclude lines from the other code quality tools. But,
   the same logic of discouraging this approach unless no other solution for
   passing the code quality check exists.

Integrating with your local developer IDE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Local developer IDEs often provide integration with with common code quality
checks, but require you to set them up in the IDE specific ways.

Visual Studio Code allows you to run code quality checks including
``black``, ``flake8``, ``isort``, ``pydocstyle`` and/or ``numpydoc`` on save.
However, they need to be activated individually in the VS Code preferences (
or set in your local ``settings.json`` file). If you want to easily Install all
the linters in your environment use the hint in the
:ref:`development installation <dev_install>` instructions and run
:code:`pip install --editable .[dev,test,linters]`.

In Visual Studio Code, we also recommend to add ``"editor.ruler": [79, 88]``
to your local ``settings.json`` to display the max line length.

``predictably`` specific code formatting conventions
----------------------------------------------------

-  Check out our :ref:`glossary`.
-  Avoid multiple statements on one line. Prefer a line return after a
   control flow statement (``if``/``for``).
-  Use absolute imports for references inside ``predictably``.
-  Don’t use ``import *`` in the source code. It is considered
   harmful by the official Python recommendations. It makes the code
   harder to read as the origin of symbols is no longer explicitly
   referenced, but most important, it prevents using a static analysis
   tool like pyflakes to automatically find bugs.
