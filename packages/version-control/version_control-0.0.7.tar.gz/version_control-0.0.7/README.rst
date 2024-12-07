.. image:: https://img.shields.io/pypi/l/version_control.svg
   :target: https://raw.githubusercontent.com/kuter/django-version-control/master/LICENSE

.. image:: https://img.shields.io/pypi/v/version_control.svg
    :target: https://pypi.python.org/pypi/version_control/
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/kuter/django-version-control.svg?branch=master
    :target: https://travis-ci.org/kuter/django-version-control

.. image:: https://coveralls.io/repos/github/kuter/django-version-control/badge.svg?branch=master
    :target: https://coveralls.io/github/kuter/django-version-control?branch=master

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black


======================
Django Version Control
======================
Third-party app created with https://github.com/kuter/django-plugin-template-cookiecutter

Quick start
-----------

1. Install version_control:

.. code:: python

   $ pip install version_control

2. Add "version_control" to your INSTALLED_APPS setting like this:

.. code:: python

    INSTALLED_APPS = [
        ...
        "version_control",
    ]

3. Enable "version_control" in your settings module as follows:

.. code:: python

    MIDDLEWARE = [
        "version_control.middleware.VersionControlMiddleware"
    ]

4. Install third-party modules

For projects running under git source control::

    $ pip install GitPython

For mercurial projects::

    $ pip install hglib  # python 3.x
    $ pip install python-hglib  # python 2.7.x
