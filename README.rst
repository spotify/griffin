griffin: RAML reference implementation in Python
======================================================

.. image:: https://img.shields.io/pypi/v/griffin.svg?style=flat-square
   :target: https://pypi.python.org/pypi/griffin/
   :alt: Latest Version

.. image:: https://img.shields.io/travis/spotify/griffin.svg?style=flat-square
   :target: https://travis-ci.org/spotify/griffin
   :alt: CI status

.. image:: https://img.shields.io/pypi/status/griffin.svg?style=flat-square
    :target: https://pypi.python.org/pypi/griffin/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/l/griffin.svg?style=flat-square
   :target: https://github.com/spotify/griffin/blob/master/LICENSE
   :alt: License

.. image:: https://img.shields.io/coveralls/spotify/griffin/master.svg?style=flat-square
   :target: https://coveralls.io/r/spotify/griffin?branch=master
   :alt: Current coverage

.. image:: https://img.shields.io/pypi/pyversions/griffin.svg?style=flat-square
    :target: https://pypi.python.org/pypi/griffin/
    :alt: Supported Python versions

.. begin

.. warning::

    This is an ALPHA! Be prepared for shit to break!

Requirements and Installation
=============================

User Setup
----------

The latest version (currently alpha only) can be found on PyPI_, and you can install via pip_::

   $ pip install griffin --pre

The ``--pre`` is needed to download since it's still in alpha.

Continue onto `usage`_ to get started on using ``griffin``.

Supported Python/Systems
^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::
  currently runs with Python 2.7 - but will get up to 3.3+ and PyPy

Both Linux and OS X are supported.



Developer Setup
---------------

If you'd like to contribute or develop upon ``griffin``, be sure to read `How to Contribute`_
first.

System requirements:
^^^^^^^^^^^^^^^^^^^^

- C Compiler (gcc/clang/etc.)
- If on Linux - you'll need to install Python headers (e.g. ``apt-get install python-dev``)
- Python 2.6, 2.7, 3.3+, or PyPy
- virtualenv_

Here's how to set your machine up::

    $ git clone git@github.com:spotify/griffin
    $ cd griffin
    $ virtualenv env
    $ source env/bin/activate
    (env) $ pip install -r dev-requirements.txt


Run Tests
^^^^^^^^^

If you'd like to run tests for all supported Python versions, you must have all Python versions
installed on your system.  I suggest pyenv_ to help with that.

To run all tests::

    (env) $ tox

To run a specific test setup (options include: ``py26``, ``py27``, ``py33``, ``py34``, ``pypy``,
``flake8``, ``verbose``, ``manifest``, ``docs``, ``setup``, ``setupcov``)::

    (env) $ tox -e py26

To run tests without tox::

    (env) $ py.test
    (env) $ py.test --cov griffin --cov-report term-missing


Build Docs
^^^^^^^^^^

Documentation is build with Sphinx_, written in rST, uses the `Read the Docs`_ theme with
a slightly customized CSS, and is hosted on `Read the Docs site`_.

To rebuild docs locally, within the parent ``griffin`` directory::

    (env) $ tox -e docs

or::

    (env) $ sphinx-build -b docs/ docs/_build


or::

    (env) $ cd docs
    (env) $ make html

Then within ``griffin/docs/_build`` you can open the index.html page in your browser.


Still have issues?
^^^^^^^^^^^^^^^^^^

Feel free to drop by ``#ramlfications`` on Freenode (`webchat`_) (no dedicated IRC channel - yet) \
or ping via `Twitter`_. "roguelynn" on IRC is the maintainer, a.k.a `econchick`_ on GitHub, \
and based in San Fran.


.. _pip: https://pip.pypa.io/en/latest/installing.html#install-pip
.. _PyPI: https://pypi.python.org/project/griffin/
.. _virtualenv: https://virtualenv.pypa.io/en/latest/
.. _pyenv: https://github.com/yyuu/pyenv
.. _Sphinx: http://sphinx-doc.org/
.. _`Read the Docs`: https://github.com/snide/sphinx_rtd_theme
.. _`Read the Docs site`: https://griffin.readthedocs.org
.. _`usage`: http://griffin.readthedocs.org/en/latest/usage.html
.. _`How to Contribute`: http://griffin.readthedocs.org/en/latest/contributing.html
.. _`webchat`: http://webchat.freenode.net?channels=%23ramlfications&uio=ND10cnVlJjk9dHJ1ZQb4
.. _`econchick`: https://github.com/econchick
.. _`Twitter`: https://twitter.com/roguelynn
