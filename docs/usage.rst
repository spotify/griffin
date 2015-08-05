========
Usage
========

To use ``griffin``:

.. code-block:: bash

    $ griffin build -r path/to/api.raml

With the above example, new directories & HTML files should now live in \
``output``.

To view them, you can simply run the following command within ``output``:

.. code-block:: bash

    $ python -m SimpleHTTPServer 8080


then navigate your browser to ``localhost:8080``.


.. note::

    Make sure the port in the above command matches your config file (if \
    you have one).  The default will be ``8080``.


For more information about the ``griffin build`` command, continue to :doc:`api`.
