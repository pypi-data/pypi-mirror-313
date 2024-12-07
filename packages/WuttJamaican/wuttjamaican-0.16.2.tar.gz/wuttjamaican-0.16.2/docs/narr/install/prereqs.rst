
Prerequisites
=============

Wuttjamaican requires Python, and optionally a database of some sort.


Python
------

Currently at least Python 3.6 is required, however:

As of writing only Python 3.8 and newer are supported by the official
Python team, so that is strongly recommended.  It is likely that will
soon become the minimum requirement for WuttJamaican as well.

Also note, Python 3.11 is the newest version being tested so far.

See also https://endoflife.date/python


Database
--------

There is not yet much logic in WuttJamaican which pertains to the
:term:`app database` so we will not document much about that here
either.

For now just know that in a production environment, PostgreSQL is
recommended for the DB backend.  So install that if you want to be
certain of a good experience.

But technically speaking, anything supported by `SQLAlchemy`_ should
work.  See also :doc:`/narr/config/table`.

.. _SQLAlchemy: https://www.sqlalchemy.org
