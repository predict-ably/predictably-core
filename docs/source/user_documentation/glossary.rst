.. _glossary:

========================
Glossary of Common Terms
========================

The glossary below defines common terms and API elements used throughout
``predictably_core``.

.. glossary::
    :sorted:

    Framework
        A collection of related and reusable software design templates that
        practitioners can copy and fill in. Frameworks emphasize design reuse.
        They capture common software design decisions within a given application domain
        and distill them into reusable design templates. This reduces the design
        decision they must take, allowing them to focus on application specifics.
        Not only can practitioners write software faster as a result, but
        applications will have a similar structure. Frameworks often offer
        additional functionality like :term:`toolboxes <toolbox>`. Compare with
        :term:`toolbox` and :term:`application`.

    Toolbox
        A collection of related and reusable functionality that practitioners
        can import to write applications. Toolboxes emphasize code reuse.
        Compare with :term:`framework` and :term:`application`.

    Application
        A single-purpose piece of code that practitioners write to solve a
        particular applied problem. Compare with :term:`toolbox` and :term:`framework`.

    Python module
        According to Python's documentation a module is *"a file containing Python
        definitions and statements"*. Python modules are files whose name is the
        module name and the suffix is ".py". For more information see Python's
        `documentation <https://docs.python.org/3/tutorial/modules.html#>`_

    Python namespace
        According to Python's documentation a namespace is *"a mapping from names
        to objects"*. For more information see Python's
        `documentation <https://docs.python.org/3/tutorial/classes.html#tut-scopes>`_

    Python package
        Python packages are a way to structure a collection of
        :term:`Python modules <Python module>` into a single "namespace". Commonly
        this is accomplished by having a directory that contains an ``__init__.py``
        file and one or more Python modules. The name of the directory, then becomes
        the "package" namespace for the sub-modules it contains. For more information
        see Python's
        `documentation <https://docs.python.org/3/tutorial/modules.html#packages>`_
