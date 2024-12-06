
App Database
============

The :term:`app database` is used at minimum to contain the
:term:`settings table`.

There is not yet support within WuttJamaican for the creation or setup
of the app database.  So for now you're on your own with that.

See also :doc:`/narr/config/table`.

Note that while any database supported by SQLAlchemy may be used, docs
will generally assume PostgreSQL is being used.


Configuring the Connection
--------------------------

Once you have a database ready, add to your :term:`config file` the
details, for example:

.. code-block:: ini

   [wutta.db]
   default.url = postgresql://wutta:wuttapass@localhost/wuttadb


Multiple Databases
------------------

Some scenarios may require multiple app databases.  A notable example
would be a multi-store retail environment, where each store runs a
separate app but a "host" (master) node has connections to all store
databases.

Using that example, the host config might look like:

.. code-block:: ini

   [wutta.db]
   # nb. host itself is referred to as 'default'
   keys = default, store001, store002, store003

   default.url = postgresql://wutta:wuttapos@localhost/wutta-host

   store001.url = postgresql://wutta:wuttapos@store001/wutta-store
   store002.url = postgresql://wutta:wuttapos@store002/wutta-store
   store003.url = postgresql://wutta:wuttapos@store003/wutta-store
