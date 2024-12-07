.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   ad hoc script
     Python script (text) file used for ad-hoc automation etc.  See
     also :doc:`narr/cli/scripts`.

   app
     Depending on context, may refer to the software application
     overall, or the :term:`app name`, or the :term:`app handler`.

   app database
     The main :term:`database` used by the :term:`app`.  There is
     normally just one database (for simple apps) which uses
     PostgreSQL for the backend.  The app database contains the
     :term:`settings table`.

   app dir
     Folder containing app-specific config files, log files, etc.
     Usually this is named ``app`` and is located at the root of the
     virtual environment.

     Can be retrieved via
     :meth:`~wuttjamaican.app.AppHandler.get_appdir()`.

   app enum
      Python module whose namespace contains all the "enum" values
      used by the :term:`app`.  Available on the :term:`app handler`
      as :attr:`~wuttjamaican.app.AppHandler.enum`.

   app handler
     Python object representing the core :term:`handler` for the
     :term:`app`.  There is normally just one "global" app handler;
     see also :doc:`narr/handlers/app`.

   app model
      Python module whose namespace contains all the :term:`data
      models<data model>` used by the :term:`app`.

   app name
     Code-friendly name for the underlying app/config system
     (e.g. ``wutta_poser``).

     This must usually be specified as part of the call to
     :func:`~wuttjamaican.conf.make_config()` and is then available on
     the :term:`config object`
     :attr:`~wuttjamaican.conf.WuttaConfig.appname` and the :term:`app
     handler` :attr:`~wuttjamaican.app.AppHandler.appname`.

     See also the human-friendly :term:`app title`.

   app provider
     A :term:`provider` which pertains to the :term:`app handler`.
     See :doc:`narr/providers/app`.

   app title
     Human-friendly name for the :term:`app` (e.g. "Wutta Poser").

     See also the code-friendly :term:`app name`.

   auth handler
      A :term:`handler` responsible for user authentication and
      authorization (login, permissions) and related things.

      See also :class:`~wuttjamaican.auth.AuthHandler`.

   command
     A top-level command line interface for the app.  Note that
     top-level commands don't usually "do" anything per se, and are
     mostly a way to group :term:`subcommands<subcommand>`.  See also
     :doc:`narr/cli/index`.

   config
     Depending on context, may refer to any of: :term:`config file`,
     :term:`config object`, :term:`config setting`.  See also
     :doc:`narr/config/index`.

   config extension
      A registered extension for the :term:`config object`.  What
      happens is, a config object is created and then extended by each
      of the registered config extensions.

      The intention is that all config extensions will have been
      applied before the :term:`app handler` is created.

   config file
     A file which contains :term:`config settings<config setting>`.
     See also :doc:`narr/config/files`.

   config object
     Python object representing the full set of :term:`config
     settings<config setting>` for the :term:`app`.  Usually it gets
     some of the settings from :term:`config files<config file>`, but
     it may also get some from the :term:`settings table`.  See also
     :doc:`narr/config/object`.

   config setting
     The value of a setting as obtained from a :term:`config object`.
     Depending on context, sometimes this refers specifically to
     values obtained from the :term:`settings table` as opposed to
     :term:`config file`.  See also :doc:`narr/config/settings`.

   data model
     Usually, a Python class which maps to a :term:`database` table.

   database
     Generally refers to a relational database which may be queried
     using SQL.  More specifically, one supported by `SQLAlchemy`_.

     .. _SQLAlchemy: https://www.sqlalchemy.org

     Most :term:`apps<app>` will have at least one :term:`app
     database`.

   db session
     The "session" is a SQLAlchemy abstraction for an open database
     connection, essentially.

     In practice this generally refers to a
     :class:`~wuttjamaican.db.sess.Session` instance.

   email handler
      The :term:`handler` responsible for sending email on behalf of
      the :term:`app`.

      Default is :class:`~wuttjamaican.email.handler.EmailHandler`.

   entry point
     This refers to a "setuptools-style" entry point specifically,
     which is a mechanism used to register "plugins" and the like.
     This lets the app / config discover features dynamically.  Most
     notably used to register :term:`commands<command>` and
     :term:`subcommands<subcommand>`.

     For more info see the `Python Packaging User Guide`_.

     .. _Python Packaging User Guide: https://packaging.python.org/en/latest/specifications/entry-points/

   handler
     Similar to a "plugin" concept but only *one* handler may be used
     for a given purpose.  See also :doc:`narr/handlers/index`.

   install handler
      The :term:`handler` responsible for installing a new instance of
      the :term:`app`.

      Default is :class:`~wuttjamaican.install.InstallHandler`.

   package
     Generally refers to a proper Python package, i.e. a collection of
     modules etc. which is installed via ``pip``.  See also
     :doc:`narr/install/pkg`.

   provider
     Python object which "provides" extra functionality to some
     portion of the :term:`app`.  Similar to a "plugin" concept; see
     :doc:`narr/providers/index`.

   settings table
     Table in the :term:`app database` which is used to store
     :term:`config settings<config setting>`.  See also
     :doc:`narr/config/table`.

   subcommand
     A top-level :term:`command` may expose one or more subcommands,
     for the overall command line interface.  Subcommands are usually
     the real workhorse; each can perform a different function with a
     custom arg set.  See also :doc:`narr/cli/index`.

   virtual environment
     This term comes from the broader Python world and refers to an
     isolated way to install :term:`packages<package>`.  See also
     :doc:`narr/install/venv`.
