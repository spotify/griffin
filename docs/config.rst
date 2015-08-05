Configuration
=============

You may use a ``yaml`` file to help configure the generation of your \
documentation.  You'll notice without certain fields within your config,
you'll see some attributes titled ``MISSING``.  So it may be a good idea \
to have a config file.

When running the ``build`` command on the command line, ``griffin`` will \
automatically look for a ``griffin.yaml`` file within the directory that \
``build`` is run.

You may also provide the ``build`` command with a path to a different \
config file, via ``-c`` or ``--config``.  See :doc:`api` for more details.

HTML ``<head>`` & Metadata
--------------------------

=================   ===========================================  =======================  ==========================
variable name       what                                         used for                 default
-----------------   -------------------------------------------  -----------------------  --------------------------
``title``           ``str``                                      Site title               ``MISSING``
``base_url``        ``str``                                      Relative URL for assets  ``http://localhost:8080``
``description``     ``str``                                      Site description         ``MISSING``
``author``          ``str``                                      Site Author name         ``MISSING``
``canonical_url``   URL that site will be deployed to            Canonical URL            ``MISSING``
``favicon``         path to an image relative to ``static_dir``  Favicon                  default theme img
=================   ===========================================  =======================  ==========================


Theming
-------

===============   ===========================================  =======================  ==========================
variable name     what                                         used for                 default
---------------   -------------------------------------------  -----------------------  --------------------------
``brand_image``   path to an image relative to ``static_dir``  Navbar Brand image       default theme img
``theme_path``    path to an image relative to ``static_dir``  Location of own theme    built-in themes
``theme_name``    name of them                                 Directory name of theme  ``default``
===============   ===========================================  =======================  ==========================


Directory Locations
-------------------

=================   =================   ======================  =============
variable name       what                used for                default
-----------------   -----------------   ----------------------  -------------
``template_dir``    path to directory   Your own templates      ``templates``
``static_dir``      path to directory   Your own static assets  ``assets``
``output_dir``      path to directory   Final HTML output       ``output``
=================   =================   ======================  =============
