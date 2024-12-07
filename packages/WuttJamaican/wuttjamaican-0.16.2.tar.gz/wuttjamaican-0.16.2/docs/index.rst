
WuttJamaican
============

This package aims to provide a "base layer" for apps regardless of
platform or environment (console, web, GUI).

It comes from patterns developed within the `Rattail Project`_, and
roughly corresponds with the "base and data layers" as described in
:doc:`rattail-manual:index`.

.. _Rattail Project: https://rattailproject.org/

Good documentation and 100% `test coverage`_ are priorities for this
project.

.. _test coverage: https://buildbot.rattailproject.org/coverage/wuttjamaican/


Features
--------

* flexible configuration, using config files and/or DB settings table
* flexible architecture, abstracting various portions of the overall app
* flexible command line interface, using `Typer`_
* flexible database support, using `SQLAlchemy`_

.. _Typer: https://typer.tiangolo.com
.. _SQLAlchemy: https://www.sqlalchemy.org

See also these projects which build on WuttJamaican:

* :doc:`wutta-continuum:index`
* `WuttaWeb <https://rattailproject.org/docs/wuttaweb/>`_


Contents
--------

.. toctree::
   :maxdepth: 3

   glossary
   narr/index
   api/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
