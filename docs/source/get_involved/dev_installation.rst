.. _dev_install:

==============================
Development Installation Guide
==============================

If you plan on contributing to ``predictably_core`` you'll want a development
installation. Follow the instructions below to install the latest development
version of ``predictably_core``.

1. Fork the ``predictably_core`` `Github repository`_
2. Create a local clone of your fork
3. Link your local clone to the original ``predictably_core`` `Github repository`_
4. Sync the main branch of your local clone
5. Create a new virtual environment via ``conda`` and activate it.
6. Complete an "editable" installation of ``predictably_core``
7. Initialize ``pre-commit`` so that ``predictably_core``'s static code quality
   analysis runs before any contributions you make can be committed to your
   local clone.

Detailed instructions for each step are provided below.


Step 1: Fork the Github repository
==================================

Fork the ``predictably-core`` `Github repository`_  by clicking on the 'Fork' button
near the top right of the page. This creates a copy of the code under your
GitHub user account. For more details on how to fork a repository see this Github
`help article <https://help.github.com/articles/fork-a-repo/>`_.

Step 2: Clone Your Fork of the Github repository
================================================

The ``predictably_core`` `Github repository`_ should be cloned to a local directory.

To install the latest version using the ``git`` command line, use the following steps:

1. Use your command line tool to navigate to the directory where you want to clone
   ``predictably_core``
2. Clone the repository:
   :code:`git clone https://github.com/predict-ably/predictably-core.git`
3. Move into the root directory of the package's local clone:
   :code:`cd predictably-core`
4. Make sure you are on the main branch: :code:`git checkout main`
5. Make sure your local version is up-to-date: :code:`git pull`

See Github's `repository clone documentation`_ for additional details.

.. hint::

    If you want to checkout an earlier version of ``predictably_core`` you can use the
    following git command line after cloning to run: :code:`git checkout <VERSION>`

    Where ``<VERSION>`` is a valid version string that can be found by inspecting the
    repository's ``git`` tags, by running ``git tag``.

    You can also download a specific release version from the Github repository's
    zip archive of
    `releases <https://github.com/predict-ably/predictably-core/releases>`_.

Step 3: Link Your Local Clone to the Original Github repository
===============================================================

Your fork will be automatically set as the "origin" for your local clone. But you
will need to configure your local clone so that the original ``predictably_core``
`Github repository`_ is set as the "upstream" remote.

To do this, first check that your fork is listed as the "origin" for you local clone:

.. code:: bash

   git remote -v
   > origin    https://github.com/<username>/predictably-core.git (fetch)
   > origin    https://github.com/<username>/predictably-core.git (push)

Then configure your local clone to add the original repository as its upstream remote:

.. code:: bash

   git remote add upstream https://github.com/predict-ably/predictably-core.git

Finally, you'll want to verify that the original repository has been successfully
set as the "upstream" remote and your fork remains the "origin" remote:

.. code:: bash

   git remote -v
   > origin    https://github.com/<username>/predictably-core.git (fetch)
   > origin    https://github.com/<username>/predictably-core.git (push)
   > upstream  https://github.com/predict-ably/predictably-core.git (fetch)
   > upstream  https://github.com/predict-ably/predictably-core.git (push)


Step 4: Sync the Main Branch of Your Local Clone
================================================
In the previous step you set the original repository as your "upstream" remote.
You'll want to make sure the main branch of your local clone is synced with
the original repository (upstream remote).

`Sync`_ the ``main`` branch of your fork with the upstream repository by running:

.. code:: bash

   git fetch upstream
   git checkout main
   git merge upstream/main


.. hint::

    You can use these same instructions to sync another branch by replacing
    the "main" branch with the name of the other branch you want to sync.

Step 5: Create a new virtual environment
=========================================

Setting up a new virtual environment before building ``predictably_core`` ensures that
conflicting package versions are not installed in the same environment.
You can choose your favorite env manager for this but the example below shows the
steps to create an environment using ``conda``:

1. Use your command line tool to first confirm ``conda`` is present on your
   system: :code:`conda --version`
2. Create a new virtual environment named ``predictably-core-dev`` with python version
   ``3.8`` or greater: :code:`conda create -n predictably-core-dev python=3.12`
3. Activate this newly created environment: :code:`conda activate predictably-core-dev`

Step 6: Complete an Editable Install
====================================

When contributing to the project, you will want to install ``predictably_core`` locally,
along with additional development dependencies. You'll be best served by installing
``predictably_core`` in an "editable" mode so that the the package updates each
time the local source code is changed.

However, ``conda develop`` is not really maintained (see `conda develop Github issue`_).
The workaround is to use ``pip``'s ability to install a package in `editable mode`_
within your ``conda`` environment. But there can be some issues with ``pip`` installed
dependencies in your ``conda`` environment in some cases. With this in mind, you have
two options:

1. Pre-install the ``predictably_core`` dependencies, as well as the
   packages used to develop ``predictably_core`` in your environment using ``conda``.
2. Allow ``pip`` to install the dependencies in your ``conda`` environment while
   it installs ``predictably_core`` in `editable mode`_.

Follow the instructions for your chosen approach to complete the editable installation.

.. tab-set::

    .. tab-item:: Pre-Installing Dependencies Using conda

        Assuming you've already navigated to the root directory of your local copy of
        the ``predictably_core`` project, you can use ``conda`` to pre-install
        dependencies, then have ``pip`` complete the editable install as follows:

        1. Navigate into the "build_tools" directory: :code:`cd ./build_tools`
        2. Install the dependencies in your ``conda`` environment:\n
           :code:`conda env update -n predictably-core-dev --file predictably-core-dev.yaml`
        3. Navigate back your local ``precitably_core`` project root: :code:`cd ..`
        4. Install ``predictably_core`` using ``pip`` without installing
           dependencies:\n :code:`pip install --no-build-isolation --no-deps -e .`

    .. tab-item:: Allow pip to Install Dependencies

        If you are okay with ``pip`` installing the package's dependencies and
        the developer dependencies, then you can complete the installation in
        fewer steps. Assuming you have already navigated to the root of your local
        copy of the ``predictably_core`` project directory this can be done by running:

        .. code-block:: bash

           pip install --editable .[dev,test,docs]

        Including the "[dev,test,docs]" modifier makes sure that the additional
        developer, test, and documentation dependencies specified in the
        ``predictably_core`` pyproject.toml file are also installed.

.. hint::

    In either installation approach, the ``.`` may be replaced
    with a full or relative path to your local clone's root directory.

.. hint::

    Some integrated development environments (IDEs) have built-in extensions
    that run many of the static code quality tools that the development
    dependency ``pre-commit`` manages to ensure the quality of the code
    you contribute to your project. This is helpful because it allows
    some of the code quality tools to automatically apply their formatting
    or linting as you develop. But in some cases (like older versions
    of VS Code) you have to have the static code quality tools installed
    in your development environment. If you want to easily install all the
    linters used by ``predictably_core`` in your development environment use:

    - :code:`pip install --editable .[dev,test,docs,linters]` when allowing ``pip``
      to install your dependencies.
    - Adding a step between steps 3 and 4 in the Pre-Installing Dependencies Using
      Conda workflow to install the linter dependencies:
      :code:`conda env update -n predictably-core-dev --file predictably-core-lint.yaml`

Step 7: Initialize ``pre-commit`` Routine
=========================================

``predictably_core``'s development workflow uses `pre-commit`_ to automatically run
static code quality routines before each commit to your local repository. This
ensures that everyone's contributions meet the expected formatting and code quality
standards.

These validations are also run in ``predictably_core`` Github repository, but by
enabling them in your local copy of the package, it ensures you can push code
that meets the packages coding norms, speeding up the code review process.

``pre-commit`` is installed as one of the developer dependencies. Since ``pre-commit``
is already in your environment, to initialize it you can run:

.. code-block:: bash

    pre-commit install

.. _Github repository: https://github.com/predict-ably/predictably-core
.. _repository clone documentation: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
.. _editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs # noqa
.. _conda develop Github issue: https://github.com/conda/conda-build/issues/4251
.. _pre-commit: https://pre-commit.com/
.. _sync: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork # noqa
