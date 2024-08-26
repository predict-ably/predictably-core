.. _git_workflow:

Git and GitHub workflow
=======================

.. note::

   If your not familiar with ``git`` you may want to start by reviewing
   `Git's documentation <https://git-scm.com/doc>`_ and then trying
   out the workflow. If you get stuck, chat with us on `Slack`_.

The preferred workflow for contributing to ``predictably_core``'s repository is
to complete a developer installation, then create a new feature branch and
follow a standard git workflow.

You can complete the workflow by following the steps below:

1.  Follow ``predictably_core``'s :ref:`development installation <dev_install>`
    instructions.

2.  Make sure the ``main`` branch of your fork is `Synced <sync>`_ with the
    upstream repository you set in your development installation.

    You completed this step as part of the :ref:`development installation <dev_install>`
    instructions, but in case you completed those at a different time, it is a
    good practice to make sure your ``main`` branch is still synced with the
    original ``predictably_core`` `Github repository`_

    .. code:: bash

       git fetch upstream
       git checkout main
       git merge upstream/main

    .. hint::

        You can use these same instructions to sync another branch by replacing
        the "main" branch with the name of the other branch you want to sync.

3.  Create a new ``feature`` branch from the ``main`` branch to hold
    your changes:

    .. code:: bash

       git checkout main
       git checkout -b <name-of-feature-branch>

    .. note::

        Contributions that don't isolate their changes to a ``feature`` branch
        will not be accepted. It's good practice to never work on the ``main`` branch.
        Always use a ``feature`` branch and name the ``feature`` branch after
        your contribution.

4.  Develop your contribution on your feature branch. Add changed files
    using ``git add`` and then ``git commit`` files to record your
    changes in Git:

    .. code:: bash

       git add <modified_files>
       git commit -m "Your short commit message"

5.  When finished, push the changes to your fork with:

    .. code:: bash

       git push --set-upstream origin my-feature-branch

6.  Follow
    `these instructions
    <https://help.github.com/articles/creating-a-pull-request-from-a-fork>`_
    to create a pull request from your fork. If your work is still work in progress,
    make sure to open a draft pull request.

    .. note::

        We recommend opening a pull request early, so that other contributors
        become aware of your work and can give you feedback early on.

7.  To add more changes related to this feature, simply repeat steps 4 and 5.

    When iterating step 5, you can leave off the command to set the upstream for
    your branch, since you already completed that. This means you'll iterate those
    steps by running:

    .. code:: bash

       git add <modified_files>
       git commit -m "Your short commit message"
       git push my-feature-branch

    .. note::

        Pull requests are updated automatically if you push new changes to the
        same branch. This will trigger ``predictably_core``'s
        :ref:`continuous integration <ci>` routine to re-run automatically.

.. _Github repository: https://github.com/predict-ably/predictably-core
.. _Slack: https://join.slack.com/t/predict-ably/shared_invite/zt-21ezi33ip-WGJCUBCWc5yVrr6FOsARaw  # noqa
.. _sync: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork # noqa
