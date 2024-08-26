.. _governance:

==========
Governance
==========

Overview
========

``predictably_core`` is a consensus-based project that is part of the ``predictably``
community. Anyone with an interest in the project can join the community, contribute
to the project, and participate in the governance process. The information below
explains the different roles in the community and how those roles work together
to make decisions.

.. _gov_coc:

Code of Conduct
===============

Contributors are expected to follow the ``predictably_core`` code of conduct.
The ``predictably_core`` project believes that everyone should be able to participate
in our community without fear of intimidation, bullying, harassment or discrimination.
All contributors are expected to show respect and courtesy to other members of
the community at all times.

While contributing to the project, we recognize that there will be times that
individuals don't agree. Disagreement is *understandable*, particularly when
working on projects with people from different backgrounds. What's important is that
we still treat each other with respect and courtesy when we don't agree.

It is also important to recognize that our different backgrounds provide different
viewpoints, and also impact how we interact and communicate with others. This
can lead to a disconnect between the intentions of those we interact with and how
the interaction feels to us. As always, respectful communication is key and it
is often possible to work together to overcome different communication styles.

But when that's not possible or an interaction is based on intimidation, bullying,
harassment, or discrimination, you should report a Code of Conduct incident
by reaching out to predictably.ai@gmail.com.

Roles
=====

There are 3 roles in ``predictably_core`` community:

- :ref:`Contributors <contribs>`
- :ref:`Core developers <core-devs>`
- :ref:`Steering Committee Members <steering_committee>`

.. _contribs:

Contributors
------------

Anyone is welcome to contribute to the project. Contributions can take many
forms (not only code) as detailed in the :ref:`contributing guide <how_to_contrib>`

For more details on how we acknowledge contributions,
see the :ref:`acknowledging contributions <acknowledging>` section below.

All of our contributors are listed under the `contributors <contributors.md>`_
section of our documentation.

.. _core-devs:

Core developers
---------------

The :ref:`core developmer team <team>`  helps manage the project by:

- engaging with the contributor community
- managing issues and Pull Requests
- reviewing others contributions in accordance with the project
  :ref:`reviewers guide <rev_guide>`
- approving and merging Pull Requests
- participating in the project's :ref:`roadmap` and decision making process
- nominating new core developers and steering committee members

Any core developer nominee must receive affirmative votes from two-thirds of
existing core developers over the course of a one week voting period.

Core developers can remain in their role for as long as they like as long as they
continue to perform the role's duties. Core developers who no longer want to
perform the role's duties can resign at any time, while core developers that become
inactive for a 12-month period will move to a "former" core developer status.
Core developers are expected promote a collaborative and inclusive environment
when working on the project; core developers who fail to live up to this standard
can also be removed by a 60% vote of the :ref:`steering committee <steering_committee>`.

.. _steering_committee:

Steering Committee
------------------

Steering Committee (SC) :ref:`team members <team>` are core developers with
additional rights and responsibilities for maintaining the project, including:

- providing thought leadership and technical direction
- strategic planning, roadmapping and project management
- managing community infrastructure (e.g., Github repository, etc)
- fostering collaborations with external organisations
- avoiding deadlocks and ensuring a smooth functioning of the project

SC nominees must be nominated by an existing core developer and receive
affirmative votes from two-thirds of core developers and a simple majority
(50% if there are an even number) of existing SC members.

Like core developers, SC members who continue to engage with the project
can serve as long as they'd like. However, SC members who do not actively engage
in their SC responsibilities are expected to resign. In the event, a SC member
who no longer engages in their responsibilities does not resign, the remaining
SC members and core developers can vote to remove them (same voting rules
as removal of core developer by steering committee).

.. _decisions:

Decision making
===============

The ``predictably_core`` community tries to take viewpoints and feedback from all
community members into account when making decisions in order to arrive at
consensus decisions.

To accomplish this, this section outlines the decision-making process used
by the project.

Where we make decisions
-----------------------

Most of the project's decisions and voting takes place on the project’s `issue
tracker <https://github.com/predict-ably/predictably-core/issues>`__,
`pull requests <https://github.com/predict-ably/predictably-core/pulls>`__ or an
:ref:`enhancement proposal <gov_bep>`. However, some sensitive discussions and
all appointment votes occur on private chats.

Core developers are expected to express their consensus (or veto) in the medium
where a given decision takes place. For changes included in the Project's issues
and Pull Requests, this is through comments or Github's built-in review process.

Types of decisions
------------------

The consensus based decision-making process for major types of project
decisions are summarized below.

.. list-table::
   :header-rows: 1

   * - Type of change
     - Decision making process
   * - Code additions or changes
     - :ref:`Lazy consensus <lazy>`
   * - Documentation changes
     - :ref:`Lazy consensus <lazy>`
   * - Changes to the API design, hard dependencies, or supported versions
     - :ref:`Lazy consensus <lazy>` based on an :ref:`PCEP <gov_pcep>`
   * - Changes to governance
     - :ref:`Lazy consensus <lazy>` based on an :ref:`PCEP <gov_pcep>`
   * - Appointment to core developer or steering committee status
     - Anonymous voting on slack


How we make decisions
---------------------

.. _lazy:

Lazy consensus
^^^^^^^^^^^^^^

Changes are approved "lazily" when after *reasonable* amount of time
the change receives approval from at least one core developer
and no rejections from any core developers.

This is approach is designed to make it easier to add new features and make changes
to the project as it develops. To make sure things run smoothly,
:ref:`core developers <core-devs>` should make sure that the *reasonable* time
other community members have to provide feedback on the changes is commensurate
to the scope of the change. For changes to the API or other larger changes,
core developers should actively solicit feedback from their peers.

.. _gov_pcep:

``predictably_core`` enhancement proposals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Project design decisions have a more detailed approval process,
commensurate with their broader impact on the project. Any changes
to the project's core API design, hard dependencies or supported versions
should first be presented in a ``predictably_core`` enhancement proposal (PCEP).

See the developer guide for more information on creating a :ref:`PCEP <bep>`.

Resolving conflicts
^^^^^^^^^^^^^^^^^^^

When consensus can't be found lazily, the project's core developers will vote
to decide how to proceed on an issue. Any core developers can call for a vote
on a topic. A topic must receive two-thirds of core developer votes cast
(abstentions are allowed) via comments on the relevant issue or
Pull Request over a one week voting period.

In the event a proposed change does not gather the necessary votes, then:

- The core developer who triggered the vote can choose to drop the issue
- The proposed changes can be escalated to the SC, who will seek to learn more
  about the team member viewpoints, before bringing the topic up for a simple
  majority vote of SC members.

.. _acknowledging:

Acknowledging contributions
===========================

The ``predictably_core`` project values all kinds of contributions and the
development team is committed to recognising each of them fairly.

The project follows the `all-contributors <https://allcontributors.org>`_
specification to recognise all contributors, including those that don’t
contribute code. Please see our list of `all contributors <contributors.md>`_.

Please let us know or open a PR with the appropriate changes to
`predictably-core/.all-contributorsrc
<https://github.com/predict-ably/predictably-core/blob/main/.all-contributorsrc>`_
if we have missed anything.

.. note::

  ``predictably_core`` is an open-source project. All code is contributed
  under `our open-source
  license <https://github.com/predict-ably/predictably-core/blob/main/LICENSE>`_.
  Contributors acknowledge that they have rights to make their contribution
  (code or otherwise) available under this license.

References
==========

Our governance model is inspired by various existing governance
structures. In particular, we'd like to acknowledge:

* `scikit-learn's governance model <https://scikit-learn.org/stable/governance.html>`_
