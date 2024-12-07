"""
Installation
============

Getting the code
----------------

.. code:: bash

    $ pip install version_control

Prerequisites
-------------

Add ``'version_control'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        'version_control',
    ]


URLconf
-------

Add the Django Version Control's URLs to your project's URLconf as follows::

    from django.conf import settings
    from django.urls import include, url

    urlpatterns = [
        path(r'^version_control/', include('version_control.urls')),
    ]

Application
===========

Models
------

.. automodule:: version_control.models
    :members:
    :show-inheritance:

Views
-----

.. automodule:: version_control.views
    :members:
    :show-inheritance:

Templates
---------

.. program-output:: tree ../../version_control/templates/
"""
__version__ = "0.0.6"
