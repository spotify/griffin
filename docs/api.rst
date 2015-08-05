API Definition
==============

.. automodule:: griffin

CLI
---

.. option:: build -r RAMLFILE

    Command-line function to build HTML documentation off of \
    a given RAML file.

    .. program:: build
    .. option:: -o OUTPUT, --output OUTPUT

        Specify where to output the built HTML files. If not given, \
        then ``output`` from the giving config file will be used. If not \
        defined in output, then a directory named ``output`` will be \
        created in the relative location that the command is ran.

    .. program:: build
    .. option:: -c CONFIGFILE, --config CONFIGFILE

        A ``yaml`` configuration file for the documentation \
        generator.  See :doc:`config` for more information.

        If no config file is provided, ``griffin`` will look for a file \
        called ``griffin.yaml`` by default within the same directory that \
        the ``build`` command is run.

    .. program:: build
    .. option:: -R RAMLCONFIGFILE, --ramlconfig RAMLCONFIGFILE

        A ``ini`` configuration file for parsing RAML.  See the `ramlfications \
        documentation \
        <https://ramlfications.readthedocs.org/en/latest/config.html>`_ \
        for more information.

    .. program:: build
    .. option:: -q, --quiet

        Suppress output.

.. autofunction:: griffin.cli.build


Core
----

.. py:class:: griffin.core.APIContext

    Context object of the parsed API.

    .. py:attribute:: api

        The API parsed by `ramlfications <https://ramlfications.readthedocs.org/en/latest>`_.

    .. py:attribute:: metadata

        Metadata about the API.

    .. py:attribute:: groupings

        A ``dict`` of groups of endpoints, defined by their parent nodes.  For example,::

            /foo
                displayName: Foo
                description: a foo endpoint
                get:
                /{id}
                    displayName: A single Foo
                    description: A particular Foo
                    get:

        There would be a ``foo`` grouping, with the ``foo`` and the \
        ``foo/{id}`` endpoints.


    .. py:attribute:: endpoints

        A ``list`` of all parsed endpoints.

.. autofunction:: griffin.core.create_context
